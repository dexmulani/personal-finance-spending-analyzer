import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def create_category_pie(df: pd.DataFrame):
    """Pie chart for expense categories."""
    expense_df = df[df['Transaction Type'] == 'Expense']
    cat_sum = expense_df.groupby('Category')['Amount'].sum().reset_index()
    fig = px.pie(cat_sum, values='Amount', names='Category', title='Spending by Category')
    return fig

def create_monthly_trend(df: pd.DataFrame):
    """Monthly expense trend line chart."""
    monthly = df[df['Transaction Type'] == 'Expense'].copy()
    monthly['Month'] = monthly['Date'].dt.to_period('M').dt.to_timestamp()
    monthly_sum = monthly.groupby('Month')['Amount'].sum().reset_index()
    fig = px.line(monthly_sum, x='Month', y='Amount', title='Monthly Spending Trend')
    return fig

def create_income_expense_bar(df: pd.DataFrame):
    """Bar chart income vs expenses."""
    summary = df.groupby('Transaction Type')['Amount'].sum().reset_index()
    fig = px.bar(summary, x='Transaction Type', y='Amount', title='Income vs Expenses')
    return fig

def create_top_merchants(df: pd.DataFrame, top_n=5):
    """Top merchants bar chart."""
    if 'Merchant' not in df.columns:
        return None
    expense_df = df[df['Transaction Type'] == 'Expense']
    top = expense_df.groupby('Merchant')['Amount'].sum().nlargest(top_n).reset_index()
    fig = px.bar(top, x='Merchant', y='Amount', title=f'Top {top_n} Merchants')
    return fig
