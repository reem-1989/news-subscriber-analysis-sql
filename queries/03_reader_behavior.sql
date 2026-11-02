-- =====================================================================
-- 03 — Reader behaviour
-- When, where and on what devices do subscribers read?
-- =====================================================================
USE news_analytics;

-- Q12. Device mix: how do people read, and how engaged are they on each device?
SELECT
    device,
    COUNT(*)                                     AS views,
    ROUND(100 * COUNT(*) / (SELECT COUNT(*) FROM article_views), 1) AS pct_of_views,
    ROUND(AVG(minutes_read), 1)                  AS avg_minutes_read,
    ROUND(100 * AVG(finished_article), 1)        AS completion_rate_pct
FROM article_views
GROUP BY device
ORDER BY views DESC;

-- Q13. What time of day do people read? (best time to publish/send alerts)
SELECT
    HOUR(view_datetime) AS hour_of_day,
    COUNT(*)            AS views
FROM article_views
GROUP BY hour_of_day
ORDER BY hour_of_day;

-- Q14. Weekday vs weekend: which sections gain or lose share at weekends?
SELECT
    s.section_name,
    ROUND(100 * SUM(CASE WHEN DAYOFWEEK(v.view_datetime) IN (1, 7) THEN 1 ELSE 0 END)
               / COUNT(*), 1) AS pct_of_views_on_weekend
FROM article_views v
JOIN articles a ON a.article_id = v.article_id
JOIN sections s ON s.section_id = a.section_id
GROUP BY s.section_name
ORDER BY pct_of_views_on_weekend DESC;
-- Note: weekends are 2 of 7 days (28.6%). Sections above that lean towards weekends.

-- Q15. Monthly reading trend in 2025.
SELECT
    DATE_FORMAT(view_datetime, '%Y-%m') AS month,
    COUNT(*)                            AS views,
    COUNT(DISTINCT subscriber_id)       AS active_readers,
    ROUND(COUNT(*) / COUNT(DISTINCT subscriber_id), 1) AS views_per_reader
FROM article_views
GROUP BY month
ORDER BY month;

-- Q16. Reading habits by age group.
SELECT
    sub.age_group,
    COUNT(DISTINCT sub.subscriber_id)                         AS readers,
    ROUND(COUNT(v.view_id) / COUNT(DISTINCT sub.subscriber_id), 1) AS views_per_reader,
    ROUND(100 * SUM(CASE WHEN v.device IN ('Mobile App', 'Mobile Web') THEN 1 ELSE 0 END)
               / COUNT(v.view_id), 1)                         AS pct_on_mobile
FROM subscribers sub
JOIN article_views v ON v.subscriber_id = sub.subscriber_id
GROUP BY sub.age_group
ORDER BY sub.age_group;
