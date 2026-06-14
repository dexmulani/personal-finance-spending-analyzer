import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

def prepare_time_series(df: pd.DataFrame):
    """Prepare monthly time series for forecasting."""
    expense_df = df[df['Transaction Type'] == 'Expense'].copy()
    expense_df['Month'] = expense_df['Date'].dt.to_period('M')
    monthly_exp = expense_df.groupby('Month')['Amount'].sum().reset_index()
    monthly_exp['Month'] = monthly_exp['Month'].dt.to_timestamp()
    monthly_exp = monthly_exp.sort_values('Month')
    return monthly_exp

def forecast_next_month(df: pd.DataFrame):
    """Simple forecasting using linear regression or moving average."""
    ts = prepare_time_series(df)
    if len(ts) < 2:
        return {'predicted': 0, 'trend': 'Insufficient data'}
    
    # Moving average for prediction
    if len(ts) >= 3:
        ma = ts['Amount'].rolling(window=3).mean().iloc[-1]
    else:
        ma = ts['Amount'].mean()
    
    # Linear regression
    ts['MonthNum'] = range(len(ts))
    X = ts[['MonthNum']]
    y = ts['Amount']
    
    model = LinearRegression()
    model.fit(X, y)
    next_month = len(ts)
    predicted_lr = model.predict([[next_month]])[0]
    
    predicted = round((ma + predicted_lr) / 2, 2)
    
    return {
        'predicted': predicted,
        'historical_avg': round(ts['Amount'].mean(), 2),
        'trend': 'Increasing' if predicted > ts['Amount'].iloc[-1] else 'Decreasing'
    }
