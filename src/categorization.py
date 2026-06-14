import pandas as pd
import re

def categorize_transaction(description: str, merchant: str = "") -> str:
    """Rule-based categorization with improved rules for Indian bank statements."""
    text = (str(description) + " " + str(merchant)).lower().strip()
    
    categories = {
        'Salary': ['salary', 'neft', 'sbint', 'hdfc', 'credit', 'payroll'],
        'Investments': ['investment', 'dividend', 'stock', 'mutual'],
        'Food & Dining': ['zomato', 'swiggy', 'restaurant', 'hotel', 'dining', 'groceries', 'biryani'],
        'Transportation': ['uber', 'ola', 'auto', 'bus', 'metro', 'petrol'],
        'Shopping': ['amazon', 'flipkart', 'meesho', 'myntra', 'shopping'],
        'Entertainment': ['netflix', 'prime', 'movie', 'ott'],
        'Utilities': ['electricity', 'water', 'gas', 'bill', 'hescom', 'jio', 'airtel'],
        'Rent': ['rent', 'landlord'],
        'Bills': ['bill', 'recharge', 'phonepe', 'upi'],
        'Healthcare': ['1mg', 'health', 'doctor', 'medical', 'pharmacy'],
        'Travel': ['travel', 'flight', 'train', 'hotel'],
        'Education': ['school', 'college', 'tuition', 'fees'],
    }
    
    # Specific merchant mappings from user's data
    merchant_map = {
        'abutalah': 'Other',  # personal transfer
        'nafeesab': 'Other',
        'sangalli': 'Other',
        'budesaheb': 'Food & Dining',
        'ayubraje': 'Food & Dining',
        'phonepe': 'Bills',
        'flipkart': 'Shopping',
        'hdfcbank': 'Bills',
        'atm': 'Cash Withdrawal',
    }
    
    # Check merchant first
    for m, cat in merchant_map.items():
        if m in text:
            return cat
    
    for category, keywords in categories.items():
        if any(re.search(r'\b' + re.escape(kw) + r'\b', text) for kw in keywords):
            return category
    
    return 'Other'

def categorize_data(df: pd.DataFrame) -> pd.DataFrame:
    """Apply categorization to the dataframe."""
    df = df.copy()
    if 'Category' not in df.columns:
        df['Category'] = df.apply(
            lambda row: categorize_transaction(
                row.get('Description', ''), 
                row.get('Merchant', '')
            ), axis=1
        )
    return df
