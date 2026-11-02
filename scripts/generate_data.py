"""
Generates the synthetic dataset for the News Subscriber Analysis project.

The data describes a fictional digital news publisher, "The Metro Ledger":
its sections, writers, articles, paying subscribers, and a year of
subscriber reading activity (2025).

Run:  python scripts/generate_data.py
Output: data/02_insert_data.sql  (INSERT statements for MySQL)
        data/csv/*.csv           (same data as CSV files)

The random seed is fixed, so the output is identical every time.
"""

import csv
import math
import os
import random
from datetime import date, datetime, timedelta

random.seed(2025)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT, "data")
CSV_DIR = os.path.join(DATA_DIR, "csv")
os.makedirs(CSV_DIR, exist_ok=True)

YEAR_START = date(2025, 1, 1)
YEAR_END = date(2025, 12, 31)

# ---------------------------------------------------------------------------
# Sections (popularity = relative share of reading)
# ---------------------------------------------------------------------------
SECTIONS = [
    # id, name, popularity, avg words
    (1, "Politics", 22, 1300),
    (2, "World", 16, 1200),
    (3, "Business", 12, 1100),
    (4, "Technology", 10, 1000),
    (5, "Opinion", 9, 950),
    (6, "Sports", 8, 800),
    (7, "Arts & Culture", 6, 1000),
    (8, "Science", 5, 1150),
    (9, "Cooking", 7, 700),
    (10, "New York", 5, 900),
]
SECTION_POP = {s[0]: s[2] for s in SECTIONS}
SECTION_WORDS = {s[0]: s[3] for s in SECTIONS}

FIRST = ["Maya", "Daniel", "Priya", "Lucas", "Amara", "Ethan", "Sofia", "Omar",
         "Grace", "Leo", "Nadia", "Ryan", "Elena", "Kofi", "Hannah", "Marcus",
         "Lina", "Jonah", "Isabel", "Theo", "Rania", "Samuel", "Chloe", "Adrian",
         "Yuki", "Victor", "Zara", "Owen", "Mira", "Caleb"]
LAST = ["Alvarez", "Brooks", "Chen", "Dawson", "Ellis", "Farouk", "Garcia",
        "Hughes", "Ibrahim", "Jensen", "Kim", "Lambert", "Moreno", "Nakamura",
        "Okafor", "Patel", "Quinn", "Rossi", "Silva", "Turner", "Usman",
        "Vance", "Walsh", "Young", "Zhang", "Bennett", "Haddad", "Kowalski"]

TITLE_PARTS = {
    1: (["Senators", "City Council Members", "Governors", "House Leaders", "Voters", "Campaigns"],
        ["Debate New Budget Plan", "Face Pressure Over Housing Bill", "Shift Strategy Before Midterms",
         "Clash Over Tax Proposal", "Weigh Election Reform", "Signal Compromise on Spending"]),
    2: (["European Leaders", "Trade Ministers", "Aid Groups", "Coastal Nations", "Regional Allies", "UN Envoys"],
        ["Meet Amid Rising Tensions", "Agree on New Climate Targets", "Warn of Food Shortages",
         "Push for Ceasefire Talks", "Sign Landmark Trade Pact", "Respond to Refugee Crisis"]),
    3: (["Retailers", "Small Businesses", "Tech Giants", "Airlines", "Banks", "Automakers"],
        ["Report Stronger-Than-Expected Profits", "Brace for Slower Holiday Sales", "Cut Jobs as Costs Rise",
         "Bet Big on Electric Future", "Face New Interest Rate Reality", "Rethink Office Return Plans"]),
    4: (["AI Startups", "Smartphone Makers", "Social Platforms", "Chip Companies", "Cybersecurity Teams", "Streaming Services"],
        ["Race to Build Smarter Assistants", "Face New Privacy Rules", "Struggle to Keep Users",
         "Unveil Next-Generation Devices", "Prepare for Major Outage Risks", "Raise Prices Again"]),
    5: (["Why We", "The Case for", "What Leaders Miss About", "It Is Time to Rethink", "The Hidden Cost of", "In Defense of"],
        ["Public Transit", "Remote Work", "Local News", "Affordable Housing", "Screen Time", "Small Cities"]),
    6: (["The Yankees", "The Knicks", "Rookie Quarterbacks", "Tennis Stars", "Marathon Runners", "Liberty Players"],
        ["Clinch a Thrilling Win", "Struggle Through Losing Streak", "Look Ahead to Playoffs",
         "Break a Season Record", "Return From Injury", "Make a Bold Trade"]),
    7: (["Broadway Shows", "New Novels", "Indie Filmmakers", "City Museums", "Jazz Musicians", "Young Painters"],
        ["Capture the City's Mood", "Draw Record Crowds", "Revive a Forgotten Classic",
         "Tell Stories of Migration", "Divide the Critics", "Find a New Audience"]),
    8: (["Astronomers", "Climate Scientists", "Researchers", "Marine Biologists", "Doctors", "Engineers"],
        ["Discover Surprising Signal", "Map a Warming Ocean", "Test a New Vaccine Approach",
         "Track Vanishing Species", "Rethink Sleep and Memory", "Build Cleaner Batteries"]),
    9: (["Weeknight", "One-Pan", "Easy", "Crispy", "Slow-Cooker", "Five-Ingredient"],
        ["Lemon Chicken", "Vegetable Curry", "Pasta With Greens", "Salmon Bowls", "Lentil Soup", "Apple Cake"]),
    10: (["Subway Riders", "Brooklyn Residents", "Queens Restaurants", "City Schools", "Bronx Tenants", "Manhattan Shops"],
         ["Adjust to Fare Changes", "Fight Rising Rents", "Celebrate a Neighborhood Revival",
          "Prepare for Winter Storm", "Push for Safer Streets", "Adapt to New Rules"]),
}

ARTICLE_TYPES = ["News", "Analysis", "Feature", "Live Update"]

# ---------------------------------------------------------------------------
# Authors
# ---------------------------------------------------------------------------
authors = []
author_id = 1
used_names = set()
authors_by_section = {}
for sid, *_ in SECTIONS:
    for _ in range(random.randint(3, 5)):
        while True:
            name = f"{random.choice(FIRST)} {random.choice(LAST)}"
            if name not in used_names:
                used_names.add(name)
                break
        hire = date(2010, 1, 1) + timedelta(days=random.randint(0, 5300))
        authors.append((author_id, name, sid, hire))
        authors_by_section.setdefault(sid, []).append(author_id)
        author_id += 1

# ---------------------------------------------------------------------------
# Articles: published from mid-Dec 2024 through Dec 2025
# ---------------------------------------------------------------------------
articles = []
articles_by_day = {}
article_id = 1
d = date(2024, 12, 15)
while d <= YEAR_END:
    weekend = d.weekday() >= 5
    for sid, name, pop, words in SECTIONS:
        # more articles for popular sections; Cooking publishes more at weekends
        rate = pop / 22 * (0.9 if weekend else 1.3)
        if sid == 9 and weekend:
            rate *= 2.5
        n = int(rate) + (1 if random.random() < rate - int(rate) else 0)
        for _ in range(n):
            if sid == 5:
                atype = "Opinion"
            elif sid == 9:
                atype = "Recipe"
            else:
                atype = random.choices(ARTICLE_TYPES, weights=[55, 20, 15, 10])[0]
            wc = int(random.gauss(words, words * 0.3))
            if atype == "Feature":
                wc = int(wc * 1.8)
            if atype == "Live Update":
                wc = int(wc * 0.6)
            wc = max(250, min(wc, 4500))
            subj, pred = TITLE_PARTS[sid]
            title = f"{random.choice(subj)} {random.choice(pred)}"
            paywalled = 0 if (atype == "Live Update" or random.random() < 0.12) else 1
            aid = random.choice(authors_by_section[sid])
            articles.append((article_id, title, sid, aid, d, atype, wc, paywalled))
            articles_by_day.setdefault(d, []).append((article_id, sid, atype, wc))
            article_id += 1
    d += timedelta(days=1)

# ---------------------------------------------------------------------------
# Subscribers
# ---------------------------------------------------------------------------
PLANS = ["Basic Digital", "All Access", "Cooking Only", "Games Only"]
PLAN_W = [45, 30, 15, 10]
CHANNELS = ["Organic Search", "Social Media", "Newsletter", "Promo Offer", "Referral"]
CHANNEL_W = [25, 20, 18, 27, 10]
REGIONS = ["New York", "California", "Texas", "Other US", "International"]
REGION_W = [24, 14, 8, 38, 16]
AGES = ["18-24", "25-34", "35-44", "45-54", "55-64", "65+"]
AGE_W = [10, 22, 21, 18, 16, 13]

# yearly churn probability by plan, adjusted by channel and billing cycle
PLAN_CHURN = {"Basic Digital": 0.30, "All Access": 0.14, "Cooking Only": 0.24, "Games Only": 0.27}
CHANNEL_CHURN = {"Organic Search": 0.85, "Social Media": 1.1, "Newsletter": 0.75,
                 "Promo Offer": 1.75, "Referral": 0.7}

subscribers = []
N_SUBS = 3000
signup_start = date(2024, 1, 1)
signup_days = (date(2025, 12, 31) - signup_start).days
for sub_id in range(1, N_SUBS + 1):
    # signups grow over time (more recent signups)
    signup = signup_start + timedelta(days=int(signup_days * (random.random() ** 0.75)))
    plan = random.choices(PLANS, weights=PLAN_W)[0]
    channel = random.choices(CHANNELS, weights=CHANNEL_W)[0]
    cycle = random.choices(["Monthly", "Annual"], weights=[62, 38])[0]
    if channel == "Promo Offer":
        cycle = random.choices(["Monthly", "Annual"], weights=[85, 15])[0]
    region = random.choices(REGIONS, weights=REGION_W)[0]
    age = random.choices(AGES, weights=AGE_W)[0]
    p = PLAN_CHURN[plan] * CHANNEL_CHURN[channel] * (1.2 if cycle == "Monthly" else 0.6)
    # longer exposure window -> more chance to have cancelled by end of 2025
    exposure = (YEAR_END - signup).days / 365
    p_total = 1 - (1 - min(p, 0.9)) ** max(exposure, 0.15)
    status, cancel = "Active", None
    if random.random() < p_total:
        status = "Cancelled"
        # cancel somewhere after signup; at least 2025-01-05 so cancels fall in our window
        earliest = max(signup + timedelta(days=20), date(2025, 1, 5))
        if earliest < YEAR_END:
            cancel = earliest + timedelta(days=random.randint(0, (YEAR_END - earliest).days))
        else:
            status = "Active"
    subscribers.append([sub_id, signup, plan, cycle, channel, region, age, status, cancel])

# ---------------------------------------------------------------------------
# Article views (reading activity during 2025)
# ---------------------------------------------------------------------------
DEVICES = ["Mobile App", "Desktop", "Mobile Web", "Tablet"]
views = []
view_id = 1

PLAN_SECTION_BOOST = {
    "Cooking Only": {9: 12},
    "Games Only": {6: 2, 7: 2},
}

for sub in subscribers:
    sub_id, signup, plan, cycle, channel, region, age, status, cancel = sub
    start = max(signup, YEAR_START)
    end = cancel if cancel else YEAR_END
    if start > end:
        continue
    active_days = (end - start).days + 1

    # ~7% of subscribers never read anything (a "dormant" group)
    dormant_p = 0.05 + (0.12 if status == "Cancelled" else 0)
    if random.random() < dormant_p:
        continue

    # reads per active day
    base = {"All Access": 0.11, "Basic Digital": 0.075, "Cooking Only": 0.04, "Games Only": 0.018}[plan]
    if status == "Cancelled":
        base *= 0.45
    if age in ("55-64", "65+"):
        base *= 1.2
    rate = base * random.lognormvariate(0, 0.6)
    n_views = max(1, int(active_days * rate))
    n_views = min(n_views, 150)

    # each reader prefers a device
    fav_device = random.choices(DEVICES, weights=[50, 25, 17, 8])[0]
    boost = PLAN_SECTION_BOOST.get(plan, {})

    for _ in range(n_views):
        vday = start + timedelta(days=random.randint(0, active_days - 1))
        # pick an article published in the last 7 days
        candidates = []
        for back in range(0, 7):
            candidates.extend(articles_by_day.get(vday - timedelta(days=back), []))
        if not candidates:
            continue
        weekend = vday.weekday() >= 5
        weights = []
        for (aid, sid, atype, wc) in candidates:
            w = SECTION_POP[sid] * boost.get(sid, 1)
            if sid == 9 and weekend:
                w *= 2.5
            if atype == "Live Update":
                w *= 1.6
            weights.append(w)
        aid, sid, atype, wc = random.choices(candidates, weights=weights)[0]

        # time of day: morning and evening peaks
        hour = random.choices(range(24), weights=[1, 1, 1, 1, 1, 2, 5, 9, 10, 7, 5, 5,
                                                   6, 5, 4, 4, 4, 5, 6, 7, 8, 7, 4, 2])[0]
        minute = random.randint(0, 59)
        vdt = datetime(vday.year, vday.month, vday.day, hour, minute, random.randint(0, 59))

        if random.random() < 0.75:
            device = fav_device
        else:
            device = random.choices(DEVICES, weights=[50, 25, 17, 8])[0]
        if 9 <= hour <= 17 and not weekend and random.random() < 0.3:
            device = "Desktop"

        # reading time: ~230 words/min if finished; long pieces finished less often
        finish_p = 0.82 - (wc / 4500) * 0.55
        if sid in (5, 8):
            finish_p += 0.08
        if device == "Mobile Web":
            finish_p -= 0.1
        finished = 1 if random.random() < finish_p else 0
        full_minutes = wc / 230
        if finished:
            minutes = full_minutes * random.uniform(0.85, 1.25)
        else:
            minutes = full_minutes * random.uniform(0.1, 0.6)
        minutes = round(max(0.2, minutes), 1)

        views.append((view_id, aid, sub_id, vdt, device, minutes, finished))
        view_id += 1

# sort views by time and renumber, so view_id follows time order
views.sort(key=lambda v: v[3])
views = [(i + 1,) + v[1:] for i, v in enumerate(views)]

# ---------------------------------------------------------------------------
# Write output
# ---------------------------------------------------------------------------
def sql_val(v):
    if v is None:
        return "NULL"
    if isinstance(v, (int, float)):
        return str(v)
    if isinstance(v, datetime):
        return f"'{v:%Y-%m-%d %H:%M:%S}'"
    if isinstance(v, date):
        return f"'{v:%Y-%m-%d}'"
    return "'" + str(v).replace("\\", "\\\\").replace("'", "''") + "'"


def write_inserts(f, table, cols, rows, batch=1000):
    f.write(f"\n-- {table}: {len(rows)} rows\n")
    for i in range(0, len(rows), batch):
        chunk = rows[i:i + batch]
        f.write(f"INSERT INTO {table} ({', '.join(cols)}) VALUES\n")
        f.write(",\n".join("(" + ", ".join(sql_val(v) for v in r) + ")" for r in chunk))
        f.write(";\n")


def write_csv(table, cols, rows):
    with open(os.path.join(CSV_DIR, f"{table}.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(cols)
        for r in rows:
            w.writerow(["" if v is None else v for v in r])


TABLES = [
    ("sections", ["section_id", "section_name"], [(s[0], s[1]) for s in SECTIONS]),
    ("authors", ["author_id", "author_name", "section_id", "hire_date"], authors),
    ("articles", ["article_id", "title", "section_id", "author_id", "publish_date",
                  "article_type", "word_count", "is_paywalled"], articles),
    ("subscribers", ["subscriber_id", "signup_date", "plan_type", "billing_cycle",
                     "acquisition_channel", "region", "age_group", "status", "cancel_date"],
     [tuple(s) for s in subscribers]),
    ("article_views", ["view_id", "article_id", "subscriber_id", "view_datetime",
                       "device", "minutes_read", "finished_article"], views),
]

with open(os.path.join(DATA_DIR, "02_insert_data.sql"), "w", encoding="utf-8") as f:
    f.write("-- Data for the News Subscriber Analysis project (generated by scripts/generate_data.py)\n")
    f.write("-- Run 01_create_schema.sql first.\n\nUSE news_analytics;\n")
    for table, cols, rows in TABLES:
        write_inserts(f, table, cols, rows)
        write_csv(table, cols, rows)

for table, cols, rows in TABLES:
    print(f"{table:15s} {len(rows):>7,} rows")
