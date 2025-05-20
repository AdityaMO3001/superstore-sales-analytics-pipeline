# Import libraries
import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from datetime import datetime

# Step 1: Load and Preprocess Data
df = pd.read_csv("cleaned_sales_data.csv")
df.dropna(subset=["Order Date", "Sales"], inplace=True)
df["Order Date"] = pd.to_datetime(df["Order Date"], errors='coerce')
df = df[df["Order Date"].notnull()]

# Step 2: Aggregate Monthly Sales
monthly_sales = df.groupby(pd.Grouper(key="Order Date", freq="ME"))[["Sales"]].sum().reset_index()
monthly_sales.columns = ["ds", "y"]

# Step 3: Forecast Sales with Prophet
model = Prophet()
model.fit(monthly_sales)
future = model.make_future_dataframe(periods=6, freq='ME')
forecast = model.predict(future)
last_date = monthly_sales["ds"].max()
future_forecast = forecast[forecast["ds"] > last_date]

# Step 4: Generate Business Insights
total_sales = monthly_sales["y"].sum()
average_sales = monthly_sales["y"].mean()
best_month = monthly_sales.loc[monthly_sales["y"].idxmax()]
worst_month = monthly_sales.loc[monthly_sales["y"].idxmin()]
latest_forecast = future_forecast.iloc[-1]
previous_forecast = future_forecast.iloc[-2]
growth_rate = (latest_forecast["yhat"] - previous_forecast["yhat"]) / previous_forecast["yhat"]
forecast_trend = "increase 📈" if growth_rate > 0 else "decline 📉"
forecast_summary = f"Expected {forecast_trend} of {abs(growth_rate):.2%} in sales for {latest_forecast['ds'].strftime('%B %Y')}."

# Step 5: Generate PDF Report
with PdfPages("AI_Annotated_Sales_Forecast_Report.pdf") as pdf:
    # Chart 1: Monthly Sales Trend
    plt.figure(figsize=(12, 6))
    plt.plot(monthly_sales["ds"], monthly_sales["y"], color="blue", marker="o")
    plt.title("📊 Total Monthly Sales Trend")
    plt.xlabel("Month"); plt.ylabel("Sales ($)")
    plt.grid(True); plt.xticks(rotation=45)
    plt.tight_layout(); pdf.savefig(); plt.close()

    # Chart 2: Actual vs Forecasted Sales
    plt.figure(figsize=(12, 6))
    plt.plot(monthly_sales['ds'], monthly_sales['y'], label='Actual', color='blue', marker='o')
    plt.plot(forecast['ds'], forecast['yhat'], label='Forecast', color='orange', linestyle='--', marker='x')
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

    # Chart 4: Forecast Components
    fig2 = model.plot_components(forecast)
    pdf.savefig(fig2); plt.close(fig2)

    # Chart 5: Executive Summary Page
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.axis('off')
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

# Completion Message
print("✅ Forecast PDF report generated: AI_Annotated_Sales_Forecast_Report.pdf")
