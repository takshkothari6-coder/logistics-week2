"""Week 3 - Advanced Data Analysis and Visualization in Logistics.
Reproducible simulated urban last-mile delivery analysis."""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

np.random.seed(2026)
n = 1500
dates = pd.date_range("2026-01-01", periods=120, freq="D")
df = pd.DataFrame({
    "date": np.random.choice(dates, n),
    "zone": np.random.choice(["North", "South", "East", "West", "Central"], n),
    "shipments": np.random.poisson(20, n) + 2,
    "distance_km": np.round(np.random.gamma(2.3, 5.2, n), 1),
    "traffic": np.random.choice(["Low", "Medium", "High"], n, p=[.35, .45, .20]),
    "transport_mode": np.random.choice(["Van", "Truck", "Two-Wheeler"], n, p=[.45, .25, .30])
})
traffic_factor = df.traffic.map({"Low":1.0,"Medium":1.18,"High":1.45})
mode_factor = df.transport_mode.map({"Van":1.0,"Truck":1.12,"Two-Wheeler":.88})
df["delivery_time_min"] = np.maximum(15 + 2*df.distance_km + .72*df.shipments + np.random.normal(0,10,n)*traffic_factor, 8)
df["transport_cost"] = np.maximum(40 + 3*df.distance_km + .85*df.shipments + .50*df.delivery_time_min*mode_factor + np.random.normal(0,15,n), 10).round(2)
df["on_time"] = ((df.delivery_time_min <= 75) & (np.random.rand(n) > .06)).astype(int)

# Data-quality checks
print("Dataset shape:", df.shape)
print("Missing values:\n", df.isna().sum())
print("Duplicate rows:", df.duplicated().sum())

# Descriptive statistics
numeric = ["shipments","distance_km","delivery_time_min","transport_cost"]
print("\nDescriptive statistics:\n", df[numeric].describe())

# KPI calculations
shipment_volume = int(df.shipments.sum())
avg_time = df.delivery_time_min.mean()
median_time = df.delivery_time_min.median()
on_time_rate = df.on_time.mean()*100
avg_cost = df.transport_cost.mean()
cost_per_shipment = df.transport_cost.sum()/shipment_volume
print("\nLOGISTICS KPIs")
print("Total shipment volume:", shipment_volume)
print("Average delivery time:", round(avg_time,2), "minutes")
print("Median delivery time:", round(median_time,2), "minutes")
print("On-time delivery rate:", round(on_time_rate,2), "%")
print("Average transport cost:", round(avg_cost,2))
print("Cost per shipment:", round(cost_per_shipment,2))

# Group analysis
daily = df.groupby("date").shipments.sum().sort_index()
zone = df.groupby("zone").agg(
    shipments=("shipments","sum"),
    avg_delivery=("delivery_time_min","mean"),
    avg_cost=("transport_cost","mean"),
    on_time_rate=("on_time","mean")
).sort_values("avg_cost", ascending=False)
print("\nZone performance:\n", zone)

# 1. Time-series visualization
plt.figure(figsize=(8,4)); plt.plot(daily.index,daily.values)
plt.title("Daily Shipment Volume"); plt.xlabel("Date"); plt.ylabel("Shipments")
plt.tight_layout(); plt.savefig("01_daily_shipment_volume.png",dpi=150); plt.show()

# 2. Distribution
plt.figure(figsize=(8,4)); plt.hist(df.delivery_time_min,bins=32)
plt.axvline(avg_time,linestyle="--",label=f"Mean={avg_time:.1f}")
plt.axvline(median_time,linestyle=":",label=f"Median={median_time:.1f}")
plt.title("Delivery Time Distribution"); plt.xlabel("Minutes"); plt.ylabel("Frequency"); plt.legend()
plt.tight_layout(); plt.savefig("02_delivery_time_distribution.png",dpi=150); plt.show()

# 3. Zone comparison
plt.figure(figsize=(8,4)); plt.bar(zone.index,zone.avg_cost)
plt.title("Average Transportation Cost by Zone"); plt.xlabel("Zone"); plt.ylabel("Average Cost")
plt.tight_layout(); plt.savefig("03_zone_cost.png",dpi=150); plt.show()

# 4. Relationship analysis
plt.figure(figsize=(8,4))
for traffic in ["Low","Medium","High"]:
    q=df[df.traffic==traffic]; plt.scatter(q.distance_km,q.delivery_time_min,alpha=.30,label=traffic)
plt.title("Distance vs Delivery Time"); plt.xlabel("Distance (km)"); plt.ylabel("Delivery Time (min)"); plt.legend()
plt.tight_layout(); plt.savefig("04_distance_vs_time.png",dpi=150); plt.show()

# 5. Category comparison
plt.figure(figsize=(7,4)); plt.boxplot([df.loc[df.traffic==x,"delivery_time_min"] for x in ["Low","Medium","High"]],tick_labels=["Low","Medium","High"])
plt.title("Delivery Time by Traffic Level"); plt.xlabel("Traffic"); plt.ylabel("Minutes")
plt.tight_layout(); plt.savefig("05_traffic_boxplot.png",dpi=150); plt.show()

# 6. Correlation analysis
corr=df[["shipments","distance_km","delivery_time_min","transport_cost","on_time"]].corr()
plt.figure(figsize=(7,5)); plt.imshow(corr.values,aspect="auto"); plt.colorbar(label="Correlation")
plt.xticks(range(len(corr)),corr.columns,rotation=45,ha="right"); plt.yticks(range(len(corr)),corr.columns)
for i in range(len(corr)):
    for j in range(len(corr)): plt.text(j,i,f"{corr.iloc[i,j]:.2f}",ha="center",va="center")
plt.title("Correlation Matrix"); plt.tight_layout(); plt.savefig("06_correlation_matrix.png",dpi=150); plt.show()

# 7. Transport-mode comparison
mode=df.groupby("transport_mode").transport_cost.mean()
plt.figure(figsize=(7,4)); plt.bar(mode.index,mode.values)
plt.title("Average Transportation Cost by Transport Mode"); plt.xlabel("Transport Mode"); plt.ylabel("Average Cost")
plt.tight_layout(); plt.savefig("07_mode_cost.png",dpi=150); plt.show()

df.to_csv("week3_logistics_simulated_dataset.csv",index=False)
print("\nAnalysis complete. Dataset and seven chart files generated.")
