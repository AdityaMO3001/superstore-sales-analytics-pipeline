# Import required libraries
import pandas as pd  # For data manipulation and analysis
from datetime import datetime  # For timestamp handling
import os  # For file and directory operations

# === Step 1: Data Pipeline Configuration ===
# Define input and output file paths
input_path = "superstore-sales-dataset-2.xlsx"  # Raw data source
output_path = "cleaned_sales_data.csv"  # Processed data output

# Validate input file existence
if not os.path.exists(input_path):
    raise FileNotFoundError("❌ Dataset not found. Please upload the latest Excel file.")

# === Step 2: Data Loading ===
# Read the raw data from Excel file, specifically from the "Database" sheet
df = pd.read_excel(input_path, sheet_name="Database")

# === Step 3: Data Cleaning ===
# Remove rows with missing values in critical columns
df = df.dropna(subset=["Order Date", "Sales"])
# Convert Order Date to datetime format, handling any invalid dates
df["Order Date"] = pd.to_datetime(df["Order Date"], errors='coerce')
# Remove any rows where date conversion failed
df = df[df["Order Date"].notnull()]

# === Step 4: Feature Engineering ===
# Extract temporal features from Order Date
df["Year"] = df["Order Date"].dt.year  # Extract year
df["Month"] = df["Order Date"].dt.strftime("%b")  # Extract month abbreviation
df["Quarter"] = df["Order Date"].dt.to_period("Q")  # Extract quarter

# === Step 5: Data Aggregation ===
# Calculate monthly total sales
monthly_sales = df.groupby(pd.Grouper(key="Order Date", freq="ME"))[["Sales"]].sum().reset_index()
# Rename columns for clarity
monthly_sales.columns = ["Month", "Total Sales"]

# === Step 6: Data Export ===
# Save the processed dataset
df.to_csv("cleaned_sales_data.csv", index=False)
# Save the monthly summary
monthly_sales.to_csv("monthly_sales_summary.csv", index=False)

# === Step 7: Pipeline Logging ===
# Record pipeline execution timestamp for tracking
with open("pipeline_log.txt", "a") as f:
    f.write(f"Data pipeline updated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

# Print success message
print("✅ Data pipeline successfully executed.")
