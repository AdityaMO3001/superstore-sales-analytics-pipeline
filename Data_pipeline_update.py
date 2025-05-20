# Import libraries
import pandas as pd
from datetime import datetime
import os

# Step 1: Configuration
input_path = "superstore-sales-dataset-2.xlsx"
output_path = "cleaned_sales_data.csv"

# Check if input file exists
if not os.path.exists(input_path):
    raise FileNotFoundError("❌ Dataset not found. Please upload the latest Excel file.")

# Step 2: Load Data
df = pd.read_excel(input_path, sheet_name="Database")

# Step 3: Clean Data
df = df.dropna(subset=["Order Date", "Sales"])
df["Order Date"] = pd.to_datetime(df["Order Date"], errors='coerce')
df = df[df["Order Date"].notnull()]

# Step 4: Feature Engineering
df["Year"] = df["Order Date"].dt.year
df["Month"] = df["Order Date"].dt.strftime("%b")
df["Quarter"] = df["Order Date"].dt.to_period("Q")

# Step 5: Aggregate Data
monthly_sales = df.groupby(pd.Grouper(key="Order Date", freq="ME"))[["Sales"]].sum().reset_index()
monthly_sales.columns = ["Month", "Total Sales"]

# Step 6: Export Data
df.to_csv("cleaned_sales_data.csv", index=False)
monthly_sales.to_csv("monthly_sales_summary.csv", index=False)

# Step 7: Log Execution
with open("pipeline_log.txt", "a") as f:
    f.write(f"Data pipeline updated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

print("✅ Data pipeline successfully executed.")
