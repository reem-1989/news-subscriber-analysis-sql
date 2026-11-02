-- =====================================================================
-- News Subscriber Analysis — database schema
-- A fictional digital news publisher, "The Metro Ledger"
-- Works with MySQL 5.7, MySQL 8.x and MariaDB
-- =====================================================================

DROP DATABASE IF EXISTS news_analytics;
CREATE DATABASE news_analytics CHARACTER SET utf8mb4;
USE news_analytics;

-- Newsroom sections (Politics, World, Cooking, ...)
CREATE TABLE sections (
    section_id    INT PRIMARY KEY,
    section_name  VARCHAR(50) NOT NULL
);

-- Journalists; each writes for one section
CREATE TABLE authors (
    author_id     INT PRIMARY KEY,
    author_name   VARCHAR(100) NOT NULL,
    section_id    INT NOT NULL,
    hire_date     DATE,
    FOREIGN KEY (section_id) REFERENCES sections(section_id)
);

-- Every published article
CREATE TABLE articles (
    article_id    INT PRIMARY KEY,
    title         VARCHAR(200) NOT NULL,
    section_id    INT NOT NULL,
    author_id     INT NOT NULL,
    publish_date  DATE NOT NULL,
    article_type  VARCHAR(20) NOT NULL,   -- News, Analysis, Feature, Live Update, Opinion, Recipe
    word_count    INT NOT NULL,
    is_paywalled  TINYINT(1) NOT NULL,    -- 1 = subscribers only
    FOREIGN KEY (section_id) REFERENCES sections(section_id),
    FOREIGN KEY (author_id)  REFERENCES authors(author_id)
);

-- Paying digital subscribers
CREATE TABLE subscribers (
    subscriber_id        INT PRIMARY KEY,
    signup_date          DATE NOT NULL,
    plan_type            VARCHAR(20) NOT NULL,  -- Basic Digital, All Access, Cooking Only, Games Only
    billing_cycle        VARCHAR(10) NOT NULL,  -- Monthly, Annual
    acquisition_channel  VARCHAR(20) NOT NULL,  -- how they found us
    region               VARCHAR(20) NOT NULL,
    age_group            VARCHAR(10) NOT NULL,
    status               VARCHAR(10) NOT NULL,  -- Active, Cancelled
    cancel_date          DATE NULL              -- NULL while still active
);

-- One row each time a subscriber opens an article (calendar year 2025)
CREATE TABLE article_views (
    view_id           INT PRIMARY KEY,
    article_id        INT NOT NULL,
    subscriber_id     INT NOT NULL,
    view_datetime     DATETIME NOT NULL,
    device            VARCHAR(20) NOT NULL,   -- Mobile App, Desktop, Mobile Web, Tablet
    minutes_read      DECIMAL(5,1) NOT NULL,
    finished_article  TINYINT(1) NOT NULL,    -- 1 = scrolled to the end
    FOREIGN KEY (article_id)    REFERENCES articles(article_id),
    FOREIGN KEY (subscriber_id) REFERENCES subscribers(subscriber_id)
);

-- Indexes for the columns we filter and join on most
CREATE INDEX idx_views_article    ON article_views(article_id);
CREATE INDEX idx_views_subscriber ON article_views(subscriber_id);
CREATE INDEX idx_views_datetime   ON article_views(view_datetime);
CREATE INDEX idx_articles_date    ON articles(publish_date);
