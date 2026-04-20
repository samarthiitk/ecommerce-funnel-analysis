import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random


random.seed(45)
np.random.seed(45)

# =========================
# USERS DATA
# =========================
num_users = 100

users = pd.DataFrame({
    "user_id": range(1, num_users + 1),
    "signup_date": [datetime(2024,1,1) + timedelta(days=random.randint(0, 30)) for _ in range(num_users)],
    "country": np.random.choice(["India", "USA", "UK"], num_users),
    "device": np.random.choice(["Mobile", "Desktop"], num_users)
})

users.to_csv("users.csv", index=False)


# =========================
# EVENTS DATA
# =========================
events_list = []
event_id = 1

for user in users["user_id"]:
    
    timestamp = datetime(2024, 2, 1) + timedelta(minutes=random.randint(0, 10000))
    events_list.append([event_id, user, "visit", timestamp])
    event_id += 1

    if random.random() < 0.7:
        timestamp = datetime(2024, 2, 1) + timedelta(minutes=random.randint(0, 10000))
        events_list.append([event_id, user, "view", timestamp])
        event_id += 1

        if random.random() < 0.5:
            timestamp = datetime(2024, 2, 1) + timedelta(minutes=random.randint(0, 10000))
            events_list.append([event_id, user, "add_to_cart", timestamp])
            event_id += 1

            if random.random() < 0.5:
                timestamp = datetime(2024, 2, 1) + timedelta(minutes=random.randint(0, 10000))
                events_list.append([event_id, user, "purchase", timestamp])
                event_id += 1

events = pd.DataFrame(events_list, columns=["event_id", "user_id", "event_type", "timestamp"])
events.to_csv("events.csv", index=False)


# =========================
# EXPERIMENTS DATA
# =========================
experiments = pd.DataFrame({
    "user_id": users["user_id"],
    "variant": np.random.choice(["A", "B"], len(users))
})

experiments.to_csv("experiments.csv", index=False)

print("All CSV files created successfully")

# Load data
#users = pd.read_csv("users.csv")
#events = pd.read_csv("events.csv")
#experiments = pd.read_csv("experiments.csv")

# Merge: events + users
data = events.merge(users, on="user_id", how="left")

# Merge: add experiment info
data = data.merge(experiments, on="user_id", how="left")

#===================
# Save final dataset
#===================
data.to_csv("final_data.csv", index=False)

print("final_data.csv created")
