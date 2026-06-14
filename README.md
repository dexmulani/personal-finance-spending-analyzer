# Personal Finance Spending Analyzer and Expense Forecasting Dashboard

A complete end-to-end data science project for analyzing personal finances, built with Streamlit. Upload your bank transactions, get automatic categorization, visualizations, insights, and future expense forecasts.

## Features
- 📁 CSV data upload with validation
- 🧹 Data cleaning and preprocessing
- 🏷️ Rule-based expense categorization (extensible to ML)
- 📊 Comprehensive EDA and KPIs
- 📈 Interactive Plotly visualizations
- 🔮 Simple forecasting with Linear Regression & Moving Average
- 💡 Automated financial insights
- 📥 Download processed data

## Screenshots
*(Add screenshots of the running app here in your GitHub repo)*

## Installation
1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   streamlit run app.py
   ```

## Project Structure
```
finance-analyzer/
├── app.py
├── requirements.txt
├── README.md
├── data/
├── notebooks/
├── src/
│   ├── preprocessing.py
│   ├── categorization.py
│   ├── analysis.py
│   ├── forecasting.py
│   ├── visualization.py
│   └── insights.py
├── assets/
└── sample_data/
```

## Technologies
- Python, Pandas, NumPy
- Streamlit, Plotly
- Scikit-learn

## Future Improvements
- ML-based categorization
- PDF/OCR support
- Budget setting & alerts
- User authentication
- Database persistence

## Sample Data
Use `sample_data/sample_transactions.csv` to test the application.
