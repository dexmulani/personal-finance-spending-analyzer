import pandas as pd

def calculate_kpis(df: pd.DataFrame):
    """Calculate key performance indicators."""
    income = df[df['Transaction Type'] == 'Income']['Amount'].sum()
    expenses = df[df['Transaction Type'] == 'Expense']['Amount'].sum()
    savings = income - expenses
    num_transactions = len(df)
    
    if len(df) > 0:
        avg_daily = expenses / ((df['Date'].max() - df['Date'].min()).days + 1) if (df['Date'].max() - df['Date'].min()).days > 0 else 0
    else:
        avg_daily = 0
    
    return {
        'total_income': round(income, 2),
        'total_expenses': round(expenses, 2),
        'savings': round(savings, 2),
        'num_transactions': num_transactions,
        'avg_daily_spending': round(avg_daily, 2),
    }

def get_category_summary(df: pd.DataFrame):
    """Get spending by category."""
    expense_df = df[df['Transaction Type'] == 'Expense']
    return expense_df.groupby('Category')['Amount'].agg(['sum', 'count']).round(2)

def monthly_summary(df: pd.DataFrame):
    """Monthly income and expenses."""
    df_monthly = df.copy()
    df_monthly['Month'] = df_monthly['Date'].dt.to_period('M')
    monthly = df_monthly.groupby(['Month', 'Transaction Type'])['Amount'].sum().unstack(fill_value=0)
    return monthly
