# News Subscriber Analysis (SQL)

Analysing reading behaviour and subscription churn for a digital news publisher using MySQL.

**Tools:** MySQL · SQL (JOINs, aggregation, CASE, subqueries, date functions) · Python (data generation)

---

## The business problem

Digital news publishers depend on subscriptions. To grow, a newsroom needs to know:

1. **What content do subscribers value?** Which sections and formats get read and finished?
2. **How and when do people read?** Devices, time of day, weekday vs weekend.
3. **Who cancels, and can we see it coming?** Which plans and marketing channels bring loyal subscribers, and does reading activity predict churn?

This project answers 23 business questions with SQL for a fictional publisher, **The Metro Ledger**, covering a full year of activity (2025).

> **About the data:** The dataset is synthetic. It was generated with a Python script (`scripts/generate_data.py`) so it would mirror the structure of a real subscription news business while containing no real customer data. The seed is fixed, so anyone can recreate the exact same data.

---

## Database schema

| Table | Rows | Description |
|---|---:|---|
| `sections` | 10 | Newsroom desks (Politics, World, Cooking, …) |
| `authors` | 45 | Journalists, each assigned to one section |
| `articles` | 2,116 | Every article: section, author, format, word count, paywall flag |
| `subscribers` | 3,000 | Plan, billing cycle, acquisition channel, region, age group, status, cancel date |
| `article_views` | 55,065 | One row per article opened by a subscriber: time, device, minutes read, finished or not |

```
sections ──< authors ──< articles ──< article_views >── subscribers
sections ──< articles
```

`──<` means one-to-many (for example, one article has many views).

---

## Project structure

```
news-subscriber-analysis-sql/
├── README.md
├── data/
│   ├── 01_create_schema.sql       # creates the database and tables
│   ├── 02_insert_data.sql         # loads all the data
│   └── csv/                       # same data as CSV files
├── queries/
│   ├── 01_data_exploration.sql    # row counts, date ranges, data-quality checks
│   ├── 02_content_performance.sql # sections, formats, top articles, article length
│   ├── 03_reader_behavior.sql     # devices, time of day, weekends, trends, age groups
│   └── 04_subscriptions_and_churn.sql  # churn by plan/channel, engagement vs churn, at-risk list
└── scripts/
    └── generate_data.py           # recreates the dataset
```

---

## Key findings

### 1. Content performance

| Section | Share of views | Completion rate |
|---|---:|---:|
| Politics | 35.9% | 63.5% |
| World | 18.4% | 66.8% |
| Business | 11.9% | 66.9% |
| Cooking | 9.6% | 71.3% |
| Opinion | 5.6% | **77.5%** |

- **Politics and World drive over half of all reading** (54%).
- **Opinion is read less but finished most often** (77.5%). Readers who choose an opinion piece commit to it.
- **Live Updates get the most views per article** (40 per article vs 25 for standard news), so breaking-news formats deliver strong reach for the effort.
- **Length matters:** completion falls from 75% for short pieces (<600 words) to 50% for very long ones (2,000+ words). Long features still earn the most reading time per view (7.6 min), so they suit readers who arrive with time to spare.

### 2. Reader behaviour

- **Mobile App is the main reading channel** (47% of views). **Mobile Web has the lowest completion rate** (57.5% vs about 69% on the app), which points to a poorer reading experience in the mobile browser.
- **Reading peaks at 7–9 am and 7–9 pm.** These are the best windows for newsletters and push alerts.
- **Cooking is a weekend product:** 44% of its views happen on Saturday and Sunday, against an expected 29% if reading were spread evenly across the week.
- Subscribers aged **55+ read the most** (about 22–23 articles each in 2025 vs about 18 for under-35s).

### 3. Subscriptions and churn

| Group | Churn rate |
|---|---:|
| All Access plan | 12.3% |
| Basic Digital plan | 27.3% |
| Promo Offer sign-ups | **35.8%** |
| Referral sign-ups | 12.2% |
| Annual, non-promo | 8.8% |
| Monthly, from a promo | **39.4%** |

- **Bundled All Access subscribers churn less than half as often** as Basic Digital subscribers.
- **Promotional offers bring volume but not loyalty.** Promo sign-ups cancel about 3 times more often than referral or organic sign-ups, and monthly promo subscribers churn at 39%.
- **Engagement is the strongest warning sign:**

| Reading level | Churn rate |
|---|---:|
| Never read | 42.6% |
| Light (<1 read/month) | 41.7% |
| Regular (1–4 reads/month) | 14.9% |
| Heavy (4+ reads/month) | **1.9%** |

- **213 active subscribers had not read anything in the last two months of 2025.** Query Q22 produces this list so a retention team can contact them.

---

## Recommendations

1. **Target re-engagement at light readers.** Use the at-risk list (Q22) to send personalised newsletters from each reader's favourite section before their renewal date.
2. **Move promo subscribers to annual plans or the All Access bundle.** Annual billing roughly halves churn in every group.
3. **Improve the mobile web reading experience,** or nudge mobile web readers toward the app, where completion is about 11 points higher.
4. **Schedule pushes and newsletters for 7–9 am and 7–9 pm,** and promote Cooking content on weekends.
5. **Use more Live Update formats on big news days,** since they deliver the highest views per article.

---

## How to run it

1. Install **MySQL** (5.7 or 8.x) and a client such as **MySQL Workbench**.
2. Open and run `data/01_create_schema.sql`. This creates the `news_analytics` database.
3. Open and run `data/02_insert_data.sql`. This loads the data, which takes a few seconds.
4. Run the files in `queries/` in order. Each question is labelled `Q1` … `Q23`.

To recreate the dataset from scratch, run `python scripts/generate_data.py` (Python 3, no extra packages needed).

---

## SQL skills demonstrated

- Multi-table `JOIN`s and `LEFT JOIN` to find missing matches (unread articles, inactive subscribers)
- Aggregation with `GROUP BY` / `HAVING`
- Conditional logic with `CASE WHEN` (length buckets, engagement levels, weekend flags)
- Subqueries in `SELECT`, `FROM` and `WHERE` (`NOT IN`)
- Date functions: `DATE_FORMAT`, `HOUR`, `DAYOFWEEK`, `DATEDIFF`
- NULL handling with `IS NULL` and `COALESCE`
- Data-quality checks before analysis

---

## AI assistance

This project was built with help from AI (Claude, by Anthropic). AI helped with:

- Writing the Python script that generates the synthetic dataset
- Drafting the database schema and the SQL queries
- Writing and editing this README

My part was choosing the business questions, running the queries in MySQL, checking the results, and interpreting the findings and recommendations. I can explain every query in this repository.
