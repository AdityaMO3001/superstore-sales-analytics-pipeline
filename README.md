# Superstore Sales Analytics Pipeline

## �� Problem Statement
Retail businesses often struggle with fragmented data, manual reporting processes, and limited visibility into sales trends. This hampers strategic planning, demand forecasting, and inventory management. The need for a scalable, automated, and insight-driven solution is more critical than ever.

## 💡 Solution
This project is a Data Analytics solution that builds an end-to-end pipeline for transforming raw sales data into actionable business insights. It automates data cleaning, feature engineering, trend aggregation, and generates executive-ready PDF reports. The pipeline also includes time-based forecasting using Facebook's Prophet — used here as a decision-support tool, not as part of a data science model lifecycle.

## 🛠️ Key Features
- Cleans and preprocesses raw Excel sales data
- Aggregates sales trends by month, quarter, and year
- Identifies best/worst-performing periods
- Generates 6-month forward-looking forecasts with 95% confidence intervals
- Produces a stakeholder-facing PDF report with charts and strategic recommendations

## 📊 Dataset Overview
The project uses the Superstore Sales Dataset, a widely-used retail dataset that includes multi-year records of order dates, sales revenue, product categories, and regions. It reflects realistic retail scenarios and supports monthly trend analysis.

## 🔄 Data Analytics Pipeline
- `Data_pipeline_update.py`: Cleans the data, validates dates and critical fields, and extracts time-based features for analysis.
- `Forecasting_monthly_sales.py`: Performs monthly aggregation, applies forecasting for the next 6 months, and creates a professional PDF report with insights and recommendations.

## 📈 Output
A downloadable PDF report is generated with:
- 📊 Monthly sales trends
- 🔮 Future forecast visualizations
- 🧠 Summary of total/average sales, growth trends, and planning recommendations
- ✅ Actionable next steps for stakeholders (inventory optimization, sales strategy, etc.)

## 💼 Business Value
- ⏱️ Cuts manual analysis time by over 90%
- 📉 Reduces ad-hoc reporting burden
- 🧭 Enables proactive planning through data-driven forecasting
- 📌 Designed for stakeholder decision-making — not just technical reporting
