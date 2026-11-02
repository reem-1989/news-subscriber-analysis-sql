-- =====================================================================
-- 01 — Data exploration
-- Get to know the tables before analysing them.
-- =====================================================================
USE news_analytics;

-- Q1. How many rows does each table have?
SELECT 'sections' AS table_name, COUNT(*) AS row_count FROM sections
UNION ALL SELECT 'authors',       COUNT(*) FROM authors
UNION ALL SELECT 'articles',      COUNT(*) FROM articles
UNION ALL SELECT 'subscribers',   COUNT(*) FROM subscribers
UNION ALL SELECT 'article_views', COUNT(*) FROM article_views;

-- Q2. What period does the data cover?
SELECT
    MIN(publish_date)  AS first_article,
    MAX(publish_date)  AS last_article
FROM articles;

SELECT
    MIN(view_datetime) AS first_view,
    MAX(view_datetime) AS last_view
FROM article_views;

-- Q3. Data quality: are there missing values where there shouldn't be?
-- cancel_date should be NULL only for active subscribers.
SELECT
    status,
    COUNT(*)                                        AS subscribers,
    SUM(CASE WHEN cancel_date IS NULL THEN 1 ELSE 0 END) AS missing_cancel_date
FROM subscribers
GROUP BY status;

-- Q4. Data quality: does any view happen before the article was published?
-- (Should return 0.)
SELECT COUNT(*) AS views_before_publish
FROM article_views v
JOIN articles a ON a.article_id = v.article_id
WHERE DATE(v.view_datetime) < a.publish_date;

-- Q5. A quick look at a few articles with their section and author names.
SELECT
    a.article_id,
    a.title,
    s.section_name,
    au.author_name,
    a.publish_date,
    a.article_type,
    a.word_count
FROM articles a
JOIN sections s  ON s.section_id = a.section_id
JOIN authors  au ON au.author_id = a.author_id
ORDER BY a.publish_date DESC
LIMIT 10;
