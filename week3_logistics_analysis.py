# Week 3 - Advanced Data Analysis and Visualization in Logistics
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

np.random.seed(42)
n = 1200

df = pd.DataFrame({
    "date": np.random.choice(pd.date_range("2026-01-01", periods=90), n),
    "zone": np.random.choice(["North", "South", "East", "West", "Central"], n),
    "shipments": np.random.poisson(18, n) + 2,
    "distance_km": np.round(np.random.gamma(2.2, 5.5, n), 1),
    "traffic": np.random.choice(["Low", "Medium", "High"], n, p=[.35, .45, .20])
})

traffic_factor = df["traffic"].map({"Low": 1.0, "Medium": 1.18, "High": 1.42})

df["delivery_time_min"] = np.maximum(
    18 + 2.1 * df["distance_km"] + 0.75 * df["shipments"]
    + np.random.normal(0, 12, n) * traffic_factor, 8
)

df["transport_cost"] = np.round(
    55 + 3.1 * df["distance_km"] + 0.9 * df["shipments"]
    + 0.55 * df["delivery_time_min"]
    + np.random.normal(0, 18, n), 2
)

df["on_time"] = (
    (df["delivery_time_min"] <= 75) &
    (np.random.rand(n) > 0.07)
).astype(int)

# Descriptive statistics
print(df.describe())

# Correlation analysis
print(df[["shipments", "distance_km", "delivery_time_min",
         "transport_cost", "on_time"]].corr())

# Daily shipment trend
daily = df.groupby("date")["shipments"].sum()
plt.figure(figsize=(9, 4))
plt.plot(daily.index, daily.values)
plt.title("Daily Shipment Volume")
plt.xlabel("Date")
plt.ylabel("Shipments")
plt.tight_layout()
plt.show()

# Delivery-time distribution
plt.figure(figsize=(8, 4))
plt.hist(df["delivery_time_min"], bins=30)
plt.title("Distribution of Delivery Time")
plt.xlabel("Minutes")
plt.ylabel("Frequency")
plt.tight_layout()
plt.show()

# Transportation cost by zone
zone_cost = df.groupby("zone")["transport_cost"].mean().sort_values()
plt.figure(figsize=(8, 4))
plt.barh(zone_cost.index, zone_cost.values)
plt.title("Average Transportation Cost by Zone")
plt.xlabel("Average Cost")
plt.tight_layout()
plt.show()

# Distance vs delivery time
plt.figure(figsize=(8, 4))
for traffic in ["Low", "Medium", "High"]:
    q = df[df["traffic"] == traffic]
    plt.scatter(q["distance_km"], q["delivery_time_min"], alpha=0.35, label=traffic)
plt.title("Distance vs Delivery Time")
plt.xlabel("Distance (km)")
plt.ylabel("Delivery Time (min)")
plt.legend()
plt.tight_layout()
plt.show()

# Delivery time by traffic
plt.figure(figsize=(7, 4))
groups = [df.loc[df["traffic"] == x, "delivery_time_min"]
          for x in ["Low", "Medium", "High"]]
plt.boxplot(groups, tick_labels=["Low", "Medium", "High"])
plt.title("Delivery Time by Traffic Level")
plt.xlabel("Traffic")
plt.ylabel("Minutes")
plt.tight_layout()
plt.show()
