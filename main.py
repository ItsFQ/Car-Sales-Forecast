import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from supabase import create_client
from statsforecast import StatsForecast
from statsforecast.models import CrostonOptimized

@st.cache_resource
def init_connection():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

supabase = init_connection()


def run_query():
    response = supabase.table("Monthly Car Sales").select("*").execute()
    return response


def create_dataframe():
    rows = run_query()
    df = pd.json_normalize(rows.data)
    return df


def create_sf_object():
    models = [CrostonOptimized()]
    sf = StatsForecast(models=models, freq='MS', n_jobs=-1)
    return sf

@st.cache_data(show_spinner="Making predictions...")
def make_predictions(df, horizon):
    model_df = df.rename({"Month": "ds", "Sales": "y"}, axis=1)
    model_df["unique_id"] = "Car Sales"
    model_df = model_df[["unique_id", "ds", "y"]]
    sf = create_sf_object()
    forecast_df = sf.forecast(df=model_df, h=horizon)
    return forecast_df.to_csv(index=False)

df = create_dataframe()

st.title("Forecast Car Sales :chart_with_upwards_trend:")

st.subheader(":rainbow[Visulize Historical Car Sales & Forecast Future Sales]")

month_options = df['Month'].tolist()
selected_months = st.multiselect(
    "Select Month(s) to display on the line chart:", options=month_options, default=month_options
)


filtered_df = df[df['Month'].isin(selected_months)]


st.subheader("Car Sales Over Selected Months")
fig, ax = plt.subplots(figsize=(10, 5)) 
ax.plot(filtered_df['Month'], filtered_df['Sales'], marker='o')
ax.set_xlabel('Month')
ax.set_ylabel('Sales')
ax.set_title('Monthly Car Sales (Selected Months)')
ax.xaxis.set_major_locator(ticker.MaxNLocator(8)) 
plt.xticks(rotation=45)
st.pyplot(fig)

with st.expander("Forecast Future"):    
    horizon = st.slider("Forecast horizon (months)", 1, 12, step=1)
    forecast_btn = st.button("Forecast", type="primary")
    if forecast_btn:
        csv_file = make_predictions(filtered_df, horizon)
        st.download_button(
            label="Download predictions",
            data=csv_file,
            file_name="predictions.csv",
            mime="text/csv"
        )
