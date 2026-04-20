# E-commerce Funnel Analysis (End-to-End Project)

## Overview
This project simulates user behavior on an e-commerce platform and performs end-to-end data analysis using Python and PostgreSQL.

The goal is to understand user drop-off across the funnel and evaluate the performance of A/B test variants.

---

## What This Project Covers

- Synthetic data generation (users, events, experiments)
- ETL pipeline (merging datasets into a final dataset)
- Funnel analysis (Python & SQL)
- Conversion rate calculation
- Device-level analysis
- A/B testing (conversion comparison)
- Statistical testing using Z-test
- Basic data visualization (funnel + A/B graph)

---

## Data Description

### 1. Users Data
- user_id
- signup_date
- country (India, USA, UK)
- device (Mobile, Desktop)

### 2. Events Data
Simulated user journey:
- visit
- view
- add_to_cart
- purchase

Events are probabilistic:
- 70% users → view
- 50% of those → add_to_cart
- 50% of those → purchase

### 3. Experiment Data
- Each user assigned randomly to:
  - Variant A
  - Variant B

---

## ETL Pipeline

- Generated separate datasets (users, events, experiments)
- Merged them into a single dataset:

  final_data.csv


  
- Combined features:
  - user info
  - event behavior
  - experiment variant

---

## Funnel Analysis

User journey:
Visit → View → Add to Cart → Purchase


### Conversion Rates
- Visit → View: ~66%
- View → Cart: ~44%
- Cart → Purchase: ~52%

### Key Insight
- Largest drop-off occurs between **View → Add to Cart**

---

## Device-Level Analysis

- Funnel calculated separately for:
  - Mobile users
  - Desktop users

### Insight
- User behavior differs across devices, indicating potential UX differences

---

## A/B Testing

### Conversion Rates
- Variant A: ~18.8%
- Variant B: ~10.6%

### Insight
- Variant A performs better than Variant B

---

## Statistical Testing (Z-Test)

- Used two-proportion Z-test to validate A/B results

### Result
- Determines whether the difference between variants is statistically significant

### Interpretation
- Even if Variant A has higher conversion, statistical testing is required before making decisions

---

## SQL Analysis (PostgreSQL)

- Loaded final dataset into PostgreSQL
- Created table: `events_data`
- Performed:
  - Funnel analysis
  - Conversion rate calculations
  - A/B testing using SQL

### Purpose
- Demonstrates ability to perform the same analysis using SQL

---

## Visualizations

- Funnel graph (user drop-off across stages)
- A/B test bar chart (conversion comparison)

---

## Project Structure
├── data.py # Data generation + ETL
├── analysis_sql.py # SQL pipeline using PostgreSQL
├── analysis_python.py # Python analysis + visualization + stats
├── users.csv
├── events.csv
├── experiments.csv
├── final_data.csv



---

## Tools Used

- Python (Pandas, NumPy)
- PostgreSQL
- SQL
- Matplotlib
- Statsmodels (Z-test)

---

## Key Learnings

- Building an end-to-end data pipeline
- Understanding funnel drop-offs
- Performing A/B testing correctly
- Importance of statistical validation
- Writing analytical logic in both Python and SQL

---

---

## 📊 Business Insights & Recommendations

### 1. Funnel Drop-off Problem
- The biggest drop occurs between **View → Add to Cart (~44%)**
- This suggests users are interested in products but not convinced to purchase

**Possible reasons:**
- Pricing concerns
- Lack of product information
- Poor UI/UX on product page

**Recommendation:**
- Improve product page (better images, reviews, pricing clarity)
- Add urgency signals (discounts, limited stock)

---

### 2. Strong Purchase Intent Once Added to Cart
- Cart → Purchase conversion is relatively high (~52%)

**Insight:**
- Once users commit to cart, they are likely to purchase

**Recommendation:**
- Focus optimization efforts earlier in funnel (View → Cart stage)

---

### 3. A/B Testing Insight
- Variant A shows higher conversion (~18.8%) vs Variant B (~10.6%)

However:

- Statistical test performed (Z-test)
- Result: Difference is **not statistically significant** (based on p-value)

**Interpretation:**
- Observed difference may be due to randomness
- Cannot confidently declare Variant A as better

**Recommendation:**
- Run experiment with larger sample size
- Avoid making product decisions based on current data

---

### 4. Device-Level Behavior
- Mobile and Desktop users show different funnel patterns

**Insight:**
- User experience may differ across devices

**Recommendation:**
- Optimize mobile UX separately
- Investigate drop-offs by device in more detail

---

## ❓ Additional Business Questions

This analysis can be extended by exploring:

- Which country has highest conversion rates?
- Do newer users behave differently from older users?
- Does time of activity impact conversion?
- Which device contributes most to revenue?
- Where should product improvements be prioritized?

---


## Author
Samarth Singh  
GitHub: https://github.com/samarthiitk
