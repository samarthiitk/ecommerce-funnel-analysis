# =========================================
# SQL ANALYSIS PIPELINE (POSTGRES)
# =========================================

import os
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values

# =========================
# LOAD DATA
# =========================
data = pd.read_csv("final_data.csv")

# =========================
# CONNECT TO POSTGRESQL
# =========================
conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password = os.getenv("DB_PASSWORD")   
)

cursor = conn.cursor()
print("Connected to PostgreSQL")

# =========================
# CREATE TABLE
# =========================
cursor.execute("""
DROP TABLE IF EXISTS events_data;
""")

cursor.execute("""
CREATE TABLE events_data (
    event_id INT,
    user_id INT,
    event_type TEXT,
    timestamp TIMESTAMP,
    signup_date DATE,
    country TEXT,
    device TEXT,
    variant TEXT
);
""")

conn.commit()

# =========================
# BULK INSERT (FAST)
# =========================
data_tuples = [tuple(x) for x in data.to_numpy()]

execute_values(
    cursor,
    """
    INSERT INTO events_data (
        event_id, user_id, event_type, timestamp,
        signup_date, country, device, variant
    ) VALUES %s
    """,
    data_tuples
)

conn.commit()
print("Data inserted into PostgreSQL")

# =========================
# SQL FUNNEL ANALYSIS
# =========================
query = """
SELECT 
    event_type,
    COUNT(DISTINCT user_id) AS users
FROM events_data
GROUP BY event_type
ORDER BY users DESC;
"""

cursor.execute(query)
result = cursor.fetchall()

print("\nSQL Funnel:")
for row in result:
    print(row)




# =========================================
# SQL CONVERSION RATES FUNNEL
# =========================================    

query = """
WITH funnel AS (
    SELECT 
        event_type,
        COUNT(DISTINCT user_id) AS users
    FROM events_data
    GROUP BY event_type
),
values_table AS (
    SELECT
        MAX(CASE WHEN event_type = 'visit' THEN users END) AS visit,
        MAX(CASE WHEN event_type = 'view' THEN users END) AS view,
        MAX(CASE WHEN event_type = 'add_to_cart' THEN users END) AS cart,
        MAX(CASE WHEN event_type = 'purchase' THEN users END) AS purchase
    FROM funnel
)
SELECT
    visit,
    view,
    cart,
    purchase,
    ROUND(view::decimal / visit, 2) AS visit_to_view,
    ROUND(cart::decimal / view, 2) AS view_to_cart,
    ROUND(purchase::decimal / cart, 2) AS cart_to_purchase
FROM values_table;
"""

cursor.execute(query)
result = cursor.fetchall()

print("\nSQL Conversion Funnel:")
for row in result:
    print(row)

# =========================================
# A/B TESTING - CONVERSION BY VARIANT
# =========================================    

query = """
WITH purchases AS (
    SELECT 
        variant,
        COUNT(DISTINCT user_id) AS purchasers
    FROM events_data
    WHERE event_type = 'purchase'
    GROUP BY variant
),
users AS (
    SELECT 
        variant,
        COUNT(DISTINCT user_id) AS total_users
    FROM events_data
    GROUP BY variant
)
SELECT 
    u.variant,
    u.total_users,
    COALESCE(p.purchasers, 0) AS purchasers,
    ROUND(COALESCE(p.purchasers, 0)::decimal / u.total_users, 3) AS conversion_rate
FROM users u
LEFT JOIN purchases p ON u.variant = p.variant;
"""

cursor.execute(query)
result = cursor.fetchall()

print("\nSQL A/B Test Results:")
for row in result:
    print(row)

# =========================
# CLOSE CONNECTION
# =========================
cursor.close()
conn.close()
print("\nConnection closed")
