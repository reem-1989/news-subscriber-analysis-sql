-- =====================================================================
-- 04 — Subscriptions and churn
-- Who cancels, and can reading behaviour warn us in advance?
-- =====================================================================
USE news_analytics;

-- Q17. Subscriber base by plan: size and cancellation (churn) rate.
SELECT
    plan_type,
    COUNT(*)                                               AS subscribers,
    SUM(CASE WHEN status = 'Cancelled' THEN 1 ELSE 0 END)  AS cancelled,
    ROUND(100 * AVG(status = 'Cancelled'), 1)              AS churn_rate_pct
FROM subscribers
GROUP BY plan_type
ORDER BY churn_rate_pct;

-- Q18. Churn by acquisition channel: which marketing channels bring loyal subscribers?
SELECT
    acquisition_channel,
    COUNT(*)                                   AS subscribers,
    ROUND(100 * AVG(status = 'Cancelled'), 1)  AS churn_rate_pct
FROM subscribers
GROUP BY acquisition_channel
ORDER BY churn_rate_pct DESC;

-- Q19. Monthly vs annual billing — and how that interacts with promo offers.
SELECT
    billing_cycle,
    CASE WHEN acquisition_channel = 'Promo Offer' THEN 'Promo' ELSE 'Non-promo' END AS came_from_promo,
    COUNT(*)                                   AS subscribers,
    ROUND(100 * AVG(status = 'Cancelled'), 1)  AS churn_rate_pct
FROM subscribers
GROUP BY billing_cycle, came_from_promo
ORDER BY billing_cycle, came_from_promo;

-- Q20. New sign-ups and cancellations per month in 2025.
SELECT
    m.month,
    COALESCE(s.new_signups, 0)    AS new_signups,
    COALESCE(c.cancellations, 0)  AS cancellations,
    COALESCE(s.new_signups, 0) - COALESCE(c.cancellations, 0) AS net_change
FROM (
    SELECT DISTINCT DATE_FORMAT(view_datetime, '%Y-%m') AS month
    FROM article_views
) m
LEFT JOIN (
    SELECT DATE_FORMAT(signup_date, '%Y-%m') AS month, COUNT(*) AS new_signups
    FROM subscribers
    GROUP BY month
) s ON s.month = m.month
LEFT JOIN (
    SELECT DATE_FORMAT(cancel_date, '%Y-%m') AS month, COUNT(*) AS cancellations
    FROM subscribers
    WHERE cancel_date IS NOT NULL
    GROUP BY month
) c ON c.month = m.month
ORDER BY m.month;

-- Q21. Do engaged readers cancel less?
-- Step 1 (subquery): reads per month for each subscriber during their 2025 time with us.
-- Step 2: group subscribers into engagement levels and compare churn.
SELECT
    engagement_level,
    COUNT(*)                                   AS subscribers,
    ROUND(100 * AVG(status = 'Cancelled'), 1)  AS churn_rate_pct
FROM (
    SELECT
        sub.subscriber_id,
        sub.status,
        CASE
            WHEN COUNT(v.view_id) = 0 THEN '1. Never read'
            WHEN COUNT(v.view_id) / GREATEST(1,
                 DATEDIFF(COALESCE(sub.cancel_date, '2025-12-31'),
                          GREATEST(sub.signup_date, '2025-01-01')) / 30) < 1
                 THEN '2. Light (<1 read/month)'
            WHEN COUNT(v.view_id) / GREATEST(1,
                 DATEDIFF(COALESCE(sub.cancel_date, '2025-12-31'),
                          GREATEST(sub.signup_date, '2025-01-01')) / 30) < 4
                 THEN '3. Regular (1-4 reads/month)'
            ELSE '4. Heavy (4+ reads/month)'
        END AS engagement_level
    FROM subscribers sub
    LEFT JOIN article_views v ON v.subscriber_id = sub.subscriber_id
    WHERE COALESCE(sub.cancel_date, '2025-12-31') >= '2025-01-01'
    GROUP BY sub.subscriber_id, sub.status, sub.signup_date, sub.cancel_date
) AS reader_engagement
GROUP BY engagement_level
ORDER BY engagement_level;

-- Q22. At-risk list for the retention team:
-- active subscribers with no reading at all in the last 60 days of 2025.
SELECT
    sub.subscriber_id,
    sub.plan_type,
    sub.billing_cycle,
    sub.signup_date,
    MAX(v.view_datetime) AS last_read
FROM subscribers sub
LEFT JOIN article_views v ON v.subscriber_id = sub.subscriber_id
WHERE sub.status = 'Active'
  AND sub.signup_date < '2025-11-01'
GROUP BY sub.subscriber_id, sub.plan_type, sub.billing_cycle, sub.signup_date
HAVING last_read IS NULL OR last_read < '2025-11-01'
ORDER BY last_read;

-- Q23. How many subscribers is that, by plan? (summary of Q22 for a manager)
SELECT
    plan_type,
    COUNT(*) AS at_risk_subscribers
FROM subscribers sub
WHERE sub.status = 'Active'
  AND sub.signup_date < '2025-11-01'
  AND sub.subscriber_id NOT IN (
        SELECT subscriber_id
        FROM article_views
        WHERE view_datetime >= '2025-11-01'
  )
GROUP BY plan_type
ORDER BY at_risk_subscribers DESC;
