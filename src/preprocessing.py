import pandas as pd
from datetime import datetime
import re

def load_data(file) -> pd.DataFrame:
    """Load CSV data from uploaded file or path."""
    if isinstance(file, str):
        df = pd.read_csv(file)
    else:
        df = pd.read_csv(file)
    return df

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and preprocess the transaction data. Supports multiple bank formats."""
    # Copy to avoid modifying original
    df = df.copy()
    
    # === Handle different column formats ===
    # Bank statement format (date, DrCr, amount, name, etc.)
    if 'date' in df.columns and 'DrCr' in df.columns and 'amount' in df.columns:
        df = df.rename(columns={
            'date': 'Date',
            'amount': 'Amount',
            'name': 'Merchant' if 'name' in df.columns else 'Description'
        })
        
        # Map DrCr to Transaction Type and sign
        df['Transaction Type'] = df['DrCr'].map({'Cr': 'Income', 'Db': 'Expense'})
        # Make amount positive
        df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
        
    # Standard format fallback
    elif 'Date' in df.columns and 'Amount' in df.columns:
        pass  # already good
    
    # Parse dates
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce', dayfirst=False)
    
    # Convert Amount to numeric
    if 'Amount' in df.columns:
        df['Amount'] = pd.to_numeric(df['Amount'].astype(str).str.replace('[$,]', '', regex=True), errors='coerce')
    
    # Drop rows with missing critical fields
    df = df.dropna(subset=['Date', 'Amount'])
    
    # Remove duplicates
    df = df.drop_duplicates()
    
    # Standardize text columns
    for col in ['Description', 'Merchant', 'name']:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.lower()
    
    # Ensure Transaction Type
    if 'Transaction Type' not in df.columns:
        df['Transaction Type'] = df['Amount'].apply(lambda x: 'Income' if x > 0 else 'Expense')
    
    # Make all amounts positive
    df['Amount'] = abs(df['Amount'])
    
    # Sort by date
    df = df.sort_values('Date').reset_index(drop=True)
    
    return df
