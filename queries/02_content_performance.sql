-- =====================================================================
-- 02 — Content performance
-- Which sections, formats and articles do subscribers read most,
-- and which ones do they actually finish?
-- =====================================================================
USE news_analytics;

-- Q6. Readership by section: views, share of all views, and completion rate.
SELECT
    s.section_name,
    COUNT(*)                                             AS total_views,
    ROUND(100 * COUNT(*) / (SELECT COUNT(*) FROM article_views), 1) AS pct_of_views,
    ROUND(AVG(v.minutes_read), 1)                        AS avg_minutes_read,
    ROUND(100 * AVG(v.finished_article), 1)              AS completion_rate_pct
FROM article_views v
JOIN articles a ON a.article_id = v.article_id
JOIN sections s ON s.section_id = a.section_id
GROUP BY s.section_name
ORDER BY total_views DESC;

-- Q7. Which article formats get read the most per article published?
-- (A section can look big just because it publishes a lot.)
SELECT
    a.article_type,
    COUNT(DISTINCT a.article_id)                          AS articles_published,
    COUNT(v.view_id)                                      AS total_views,
    ROUND(COUNT(v.view_id) / COUNT(DISTINCT a.article_id), 1) AS views_per_article,
    ROUND(100 * AVG(v.finished_article), 1)               AS completion_rate_pct
FROM articles a
LEFT JOIN article_views v ON v.article_id = a.article_id
GROUP BY a.article_type
ORDER BY views_per_article DESC;

-- Q8. Top 10 most-read articles of 2025.
SELECT
    a.title,
    s.section_name,
    au.author_name,
    a.publish_date,
    COUNT(*) AS views
FROM article_views v
JOIN articles a  ON a.article_id = v.article_id
JOIN sections s  ON s.section_id = a.section_id
JOIN authors  au ON au.author_id = a.author_id
GROUP BY a.article_id, a.title, s.section_name, au.author_name, a.publish_date
ORDER BY views DESC
LIMIT 10;

-- Q9. Does article length affect whether people finish reading?
-- Group articles into length buckets with CASE.
SELECT
    CASE
        WHEN a.word_count < 600  THEN '1. Short (<600 words)'
        WHEN a.word_count < 1200 THEN '2. Medium (600-1199)'
        WHEN a.word_count < 2000 THEN '3. Long (1200-1999)'
        ELSE                          '4. Very long (2000+)'
    END                                       AS length_bucket,
    COUNT(*)                                  AS views,
    ROUND(AVG(v.minutes_read), 1)             AS avg_minutes_read,
    ROUND(100 * AVG(v.finished_article), 1)   AS completion_rate_pct
FROM article_views v
JOIN articles a ON a.article_id = v.article_id
GROUP BY length_bucket
ORDER BY length_bucket;

-- Q10. Author leaderboard: writers with the most total reading time
-- (minimum 20 articles, so one viral story doesn't dominate).
SELECT
    au.author_name,
    s.section_name,
    COUNT(DISTINCT a.article_id)        AS articles,
    COUNT(v.view_id)                    AS views,
    ROUND(SUM(v.minutes_read) / 60, 0)  AS total_hours_read
FROM authors au
JOIN sections s       ON s.section_id = au.section_id
JOIN articles a       ON a.author_id = au.author_id
LEFT JOIN article_views v ON v.article_id = a.article_id
GROUP BY au.author_id, au.author_name, s.section_name
HAVING COUNT(DISTINCT a.article_id) >= 20
ORDER BY total_hours_read DESC
LIMIT 10;

-- Q11. Articles that nobody read (possible wasted effort or poor promotion).
SELECT
    s.section_name,
    COUNT(*) AS unread_articles
FROM articles a
JOIN sections s ON s.section_id = a.section_id
LEFT JOIN article_views v ON v.article_id = a.article_id
WHERE v.view_id IS NULL
  AND a.publish_date BETWEEN '2025-01-01' AND '2025-12-31'
GROUP BY s.section_name
ORDER BY unread_articles DESC;
