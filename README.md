# Week 3 – Advanced Data Analysis and Visualization in Logistics

## Project
**Urban Last-Mile Delivery: Exploratory Data Analysis and Visualization**

This project demonstrates a complete logistics EDA workflow using a reproducible simulated dataset. It calculates KPIs, performs descriptive and relationship analysis, creates seven visualizations, identifies operational bottlenecks, and provides business recommendations.

## Dataset
- 1,500 observations
- 120-day operating period
- 5 service zones
- Shipment volume
- Distance in kilometres
- Traffic level
- Transport mode
- Delivery time
- Transportation cost
- On-time delivery indicator

## KPIs
1. Total shipment volume
2. Average delivery time
3. Median delivery time
4. On-time delivery rate
5. Average transportation cost
6. Cost per shipment

## Analysis Performed
- Data structure and quality checks
- Missing-value and duplicate checks
- Descriptive statistics
- KPI calculation
- Daily shipment trend analysis
- Delivery-time distribution
- Zone-level cost comparison
- Distance versus delivery-time relationship
- Traffic-level comparison
- Correlation analysis
- Transport-mode cost comparison

## Visualizations
1. Daily shipment volume
2. Delivery-time distribution
3. Average transportation cost by zone
4. Distance versus delivery time
5. Delivery time by traffic level
6. Correlation matrix
7. Average transportation cost by transport mode

## Future Data Science Applications
Regression, time-series forecasting, clustering, classification and vehicle-routing optimization are discussed as next steps after real operational data becomes available.

## How to Run
```bash
pip install numpy pandas matplotlib
python week3_logistics_analysis.py
```

The script generates the simulated dataset and chart outputs automatically.

## Limitations
The dataset is simulated for academic purposes. Real-world deployment would require order-level records, depot locations, vehicle capacities, customer time windows, fuel/energy costs, weather and road-network travel times.