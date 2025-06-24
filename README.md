# Streamlit Monthly Car Sales Forecast 🚗 📈

This project is a Streamlit web app for visualizing and forecasting monthly car sales data. It connects to a Supabase database, displays sales trends, and provides future sales forecasts using the CrostonOptimized model from the statsforecast library.

## Features
- Connects to a Supabase table with columns `Month` and `Sales`
- Interactive line chart of sales over time
- Multiselect widget to filter months displayed on the chart
- Forecasts future sales using CrostonOptimized
- Downloadable CSV of forecast results

## Setup
1. **Clone the repository and install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
2. **Configure Supabase credentials:**
   - Create a `.streamlit/secrets.toml` file with:
     ```toml
     SUPABASE_URL = "<your-supabase-url>"
     SUPABASE_KEY = "<your-supabase-key>"
     ```
3. **Run the app:**
   ```sh
   streamlit run main.py
   ```

## Usage
- The app will display a table and a line chart of your monthly car sales.
- Use the multiselect to choose which months to display.
- Use the forecast expander to select a forecast horizon and download predictions.

## Requirements
- Python 3.8+
- See `requirements.txt` for all dependencies

## Data Format
Your Supabase table should be named `Monthly Car Sales` and have the following columns:
- `Month` (text, format: YYYY-MM)
- `Sales` (integer)
