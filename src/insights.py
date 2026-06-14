import pandas as pd

def generate_insights(df: pd.DataFrame):
    """Generate financial insights."""
    insights = []
    expense_df = df[df['Transaction Type'] == 'Expense']
    
    if len(expense_df) == 0:
        return ["No expense data available."]
    
    # Highest spending category
    cat_sum = expense_df.groupby('Category')['Amount'].sum()
    if not cat_sum.empty:
        top_cat = cat_sum.idxmax()
        insights.append(f"Highest spending category: {top_cat} (${cat_sum.max():.2f})")
    
    # Monthly comparison (if enough data)
    df_monthly = df.copy()
    df_monthly['Month'] = df_monthly['Date'].dt.to_period('M')
    monthly_exp = df_monthly[df_monthly['Transaction Type'] == 'Expense'].groupby('Month')['Amount'].sum()
    
    if len(monthly_exp) >= 2:
        last_month = monthly_exp.iloc[-1]
        prev_month = monthly_exp.iloc[-2]
        change = ((last_month - prev_month) / prev_month * 100) if prev_month > 0 else 0
        insights.append(f"Expenses changed by {change:.1f}% from previous month.")
    
    insights.append(f"Total transactions: {len(df)}")
    
    return insights
