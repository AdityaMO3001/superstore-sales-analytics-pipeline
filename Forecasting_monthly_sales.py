# Import required libraries
import pandas as pd  # For data manipulation and analysis
from prophet import Prophet  # Facebook's time series forecasting library
import matplotlib.pyplot as plt  # For creating visualizations
from matplotlib.backends.backend_pdf import PdfPages  # For generating PDF reports
from datetime import datetime  # For handling dates

# === Step 1: Data Loading and Preprocessing ===
# Load the cleaned sales data from CSV file
df = pd.read_csv("cleaned_sales_data.csv")
# Remove any rows with missing values in Order Date or Sales columns
df.dropna(subset=["Order Date", "Sales"], inplace=True)
# Convert Order Date column to datetime format, handling any invalid dates
df["Order Date"] = pd.to_datetime(df["Order Date"], errors='coerce')
# Filter out any rows where Order Date is null after conversion
df = df[df["Order Date"].notnull()]

# === Step 2: Data Aggregation ===
# Group the data by month and calculate total sales for each month
# ME stands for Month End frequency
monthly_sales = df.groupby(pd.Grouper(key="Order Date", freq="ME"))[["Sales"]].sum().reset_index()
# Rename columns to match Prophet's required format (ds for dates, y for target variable)
monthly_sales.columns = ["ds", "y"]

# === Step 3: Time Series Forecasting ===
# Initialize the Prophet model
model = Prophet()
# Fit the model to our monthly sales data
model.fit(monthly_sales)
# Create a future dataframe for the next 6 months
future = model.make_future_dataframe(periods=6, freq='ME')
# Generate predictions for all dates including future dates
forecast = model.predict(future)
# Get the last date from our actual data
last_date = monthly_sales["ds"].max()
# Filter forecast to only include future dates
future_forecast = forecast[forecast["ds"] > last_date]

# === Step 4: Business Insights Generation ===
# Calculate key metrics
total_sales = monthly_sales["y"].sum()  # Total sales across all months
average_sales = monthly_sales["y"].mean()  # Average monthly sales
best_month = monthly_sales.loc[monthly_sales["y"].idxmax()]  # Month with highest sales
worst_month = monthly_sales.loc[monthly_sales["y"].idxmin()]  # Month with lowest sales
# Get the latest forecast values
latest_forecast = future_forecast.iloc[-1]
previous_forecast = future_forecast.iloc[-2]
# Calculate month-over-month growth rate
growth_rate = (latest_forecast["yhat"] - previous_forecast["yhat"]) / previous_forecast["yhat"]
# Determine if the trend is increasing or decreasing
forecast_trend = "increase 📈" if growth_rate > 0 else "decline 📉"
# Create a summary of the forecast
forecast_summary = f"Expected {forecast_trend} of {abs(growth_rate):.2%} in sales for {latest_forecast['ds'].strftime('%B %Y')}."

# === Step 5: PDF Report Generation ===
# Create a PDF file to store all visualizations and insights
with PdfPages("AI_Annotated_Sales_Forecast_Report.pdf") as pdf:
    # Chart 1: Historical Monthly Sales Trend
    plt.figure(figsize=(12, 6))
    plt.plot(monthly_sales["ds"], monthly_sales["y"], color="blue", marker="o")
    plt.title("📊 Total Monthly Sales Trend")
    plt.xlabel("Month"); plt.ylabel("Sales ($)")
    plt.grid(True); plt.xticks(rotation=45)
    plt.tight_layout(); pdf.savefig(); plt.close()

    # Chart 2: Combined Historical and Forecasted Sales
    plt.figure(figsize=(12, 6))
    plt.plot(monthly_sales['ds'], monthly_sales['y'], label='Actual', color='blue', marker='o')
    plt.plot(forecast['ds'], forecast['yhat'], label='Forecast', color='orange', linestyle='--', marker='x')
    # Add confidence interval shading
    plt.fill_between(forecast['ds'], forecast['yhat_lower'], forecast['yhat_upper'], alpha=0.3, color='orange')
    plt.title("📈 Forecasted Sales with Confidence Interval")
    plt.xlabel("Month"); plt.ylabel("Sales ($)")
    plt.grid(True); plt.xticks(rotation=45); plt.legend()
    plt.tight_layout(); pdf.savefig(); plt.close()

    # Chart 3: Future Forecast Only
    plt.figure(figsize=(12, 6))
    plt.plot(future_forecast['ds'], future_forecast['yhat'], color='green', label='Forecast', marker='s')
    plt.fill_between(future_forecast['ds'], future_forecast['yhat_lower'], future_forecast['yhat_upper'], color='green', alpha=0.3)
    plt.title("🔮 Future Sales Forecast (Next 6 Months)")
    plt.xlabel("Month"); plt.ylabel("Sales ($)")
    plt.grid(True); plt.xticks(rotation=45); plt.legend()
    plt.tight_layout(); pdf.savefig(); plt.close()

    # Chart 4: Prophet Components Analysis
    # Shows trend, yearly seasonality, and weekly seasonality if applicable
    fig2 = model.plot_components(forecast)
    pdf.savefig(fig2); plt.close(fig2)

    # Page 5: Executive Summary
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.axis('off')
    # Create a comprehensive summary of findings and recommendations
    summary = f"""
    🧠 AI Sales Forecast Report ({datetime.today().strftime('%B %Y')})

    • Total Sales Analyzed: ${total_sales:,.2f}
    • Average Monthly Sales: ${average_sales:,.2f}
    • Best Month: {best_month['ds'].strftime('%B %Y')} — ${best_month['y']:,.2f}
    • Worst Month: {worst_month['ds'].strftime('%B %Y')} — ${worst_month['y']:,.2f}
    • {forecast_summary}

    📌 Recommendations:
    - Plan inventory around peaks like {best_month['ds'].strftime('%B')}.
    - Investigate {worst_month['ds'].strftime('%B')} performance.
    - Use forecasts for vendor negotiation & budgeting.

    ✅ Next Steps:
    - Build category/region-specific models
    - Add anomaly detection + alerts
    - Deploy interactive dashboard
    """
    ax.text(0.01, 0.95, summary, fontsize=12, verticalalignment='top', wrap=True)
    pdf.savefig(); plt.close()

# Print confirmation message
print("✅ Forecast PDF report generated: AI_Annotated_Sales_Forecast_Report.pdf")
