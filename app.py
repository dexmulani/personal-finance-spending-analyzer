import streamlit as st
import pandas as pd
from src.preprocessing import load_data, clean_data
from src.categorization import categorize_data
from src.analysis import calculate_kpis, get_category_summary, monthly_summary
from src.forecasting import forecast_next_month
from src.visualization import create_category_pie, create_monthly_trend, create_income_expense_bar, create_top_merchants
from src.insights import generate_insights
import plotly.express as px

st.set_page_config(page_title="Finance Analyzer", layout="wide")
st.title("💰 Personal Finance Spending Analyzer")

# File uploader
uploaded_file = st.file_uploader("Upload your transaction CSV", type=["csv"])

if uploaded_file is not None:
    try:
        # Load and process data
        df = load_data(uploaded_file)
        df_clean = clean_data(df)
        df_categorized = categorize_data(df_clean)
        
        st.success("Data loaded and processed successfully!")
        
        # KPIs
        kpis = calculate_kpis(df_categorized)
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Income", f"${kpis['total_income']}")
        col2.metric("Total Expenses", f"${kpis['total_expenses']}")
        col3.metric("Net Savings", f"${kpis['savings']}")
        col4.metric("Transactions", kpis['num_transactions'])
        
        # Tabs
        tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Visualizations", "Forecast", "Insights"])
        
        with tab1:
            st.subheader("Category Summary")
            cat_summary = get_category_summary(df_categorized)
            st.dataframe(cat_summary)
            
            st.subheader("Monthly Summary")
            monthly = monthly_summary(df_categorized)
            st.dataframe(monthly)
        
        with tab2:
            col_v1, col_v2 = st.columns(2)
            with col_v1:
                st.plotly_chart(create_category_pie(df_categorized), use_container_width=True)
                st.plotly_chart(create_income_expense_bar(df_categorized), use_container_width=True)
            with col_v2:
                st.plotly_chart(create_monthly_trend(df_categorized), use_container_width=True)
                if create_top_merchants(df_categorized):
                    st.plotly_chart(create_top_merchants(df_categorized), use_container_width=True)
        
        with tab3:
            forecast = forecast_next_month(df_categorized)
            st.subheader("Expense Forecast")
            st.metric("Predicted Next Month Expenses", f"${forecast['predicted']}")
            st.info(f"Trend: {forecast['trend']}. Historical average: ${forecast['historical_avg']}")
            
            # Simple forecast visualization
            ts = df_categorized[df_categorized['Transaction Type'] == 'Expense'].copy()
            ts['Month'] = ts['Date'].dt.to_period('M').dt.to_timestamp()
            monthly_exp = ts.groupby('Month')['Amount'].sum().reset_index()
            fig_forecast = px.line(monthly_exp, x='Month', y='Amount', title='Historical + Forecast')
            st.plotly_chart(fig_forecast, use_container_width=True)
        
        with tab4:
            st.subheader("Key Insights")
            insights = generate_insights(df_categorized)
            for insight in insights:
                st.write(f"• {insight}")
        
        # Download processed data
        csv = df_categorized.to_csv(index=False)
        st.download_button("Download Categorized Data", csv, "processed_transactions.csv", "text/csv")
        
    except Exception as e:
        st.error(f"Error processing file: {str(e)}")
else:
    st.info("Upload a CSV file to get started. Use sample data in sample_data/ for testing.")
    
    # Show sample
    if st.button("Load Sample Data"):
        try:
            # This would be handled in a full app, but for demo
            st.info("Sample data loaded - implement in production.")
        except:
            pass
