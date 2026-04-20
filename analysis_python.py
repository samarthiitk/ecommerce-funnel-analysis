import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from statsmodels.stats.proportion import proportions_ztest

data = pd.read_csv("final_data.csv")

random.seed(45)
np.random.seed(45)

# =========================
# Funnel Analysis
# =========================

funnel = data.groupby("event_type")["user_id"].nunique().reset_index()
funnel.columns = ["event_type", "users"]

print(funnel)   

# =========================
# Extract values
# =========================

visit = funnel[funnel["event_type"] == "visit"]["users"].values[0]
view = funnel[funnel["event_type"] == "view"]["users"].values[0]
cart = funnel[funnel["event_type"] == "add_to_cart"]["users"].values[0]
purchase = funnel[funnel["event_type"] == "purchase"]["users"].values[0]

# =========================
# Conversion rates
# =========================

visit_to_view = view / visit
view_to_cart = cart / view
cart_to_purchase = purchase / cart

print("\nConversion Rates:")
print(f"Visit → View: {visit_to_view:.2f}")
print(f"View → Cart: {view_to_cart:.2f}")
print(f"Cart → Purchase: {cart_to_purchase:.2f}")


# =========================
# FUNNEL GRAPH
# =========================

import matplotlib.pyplot as plt

stages = ["visit", "view", "add_to_cart", "purchase"]
values = [visit, view, cart, purchase]

plt.plot(stages, values, marker='o')
plt.title("User Funnel")
plt.xlabel("Stage")
plt.ylabel("Users")
plt.show()

# =========================
# Funnel by device
# =========================

funnel_device = data.groupby(["device", "event_type"])["user_id"].nunique().reset_index()

print("\nFunnel by Device:")
print(funnel_device)

# =========================
# A/B Testing - Conversion by variant
# =========================

ab_test = data[data["event_type"] == "purchase"].groupby("variant")["user_id"].nunique().reset_index()

total_users = data.groupby("variant")["user_id"].nunique().reset_index()
total_users.columns = ["variant", "total_users"]

ab_test = ab_test.merge(total_users, on="variant")
ab_test["conversion_rate"] = ab_test["user_id"] / ab_test["total_users"]

print("\nA/B Test Results:")
print(ab_test)

# =========================
# A/B TEST GRAPH
# =========================

ab_test.plot(x="variant", y="conversion_rate", kind="bar")
plt.title("Conversion Rate by Variant")
plt.ylabel("Conversion Rate")
plt.show()

# =========================
# STATISTICAL TEST (Z-TEST)
# =========================

success = ab_test["user_id"].values      # purchasers
nobs = ab_test["total_users"].values     # total users

z_stat, p_value = proportions_ztest(success, nobs)

print("\nStatistical Test:")
print("Z-stat:", round(z_stat, 3))
print("P-value:", round(p_value, 4))

if p_value < 0.05:
    print("Result: Significant difference between A and B")
else:
    print("Result: No significant difference")
