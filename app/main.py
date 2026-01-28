import os
import pandas as pd
import streamlit as st

st.set_page_config(page_title="World Real Estate App", page_icon="🏠")
st.title("Housing dataset check 🏠")

data_path = os.getenv("DATA_PATH", "/app/data/raw/global_housing_market_extended.csv")
st.write("Dataset path:", data_path)

df = pd.read_csv(data_path)

st.write("Rows:", df.shape[0])
st.write("Columns:", df.shape[1])
st.dataframe(df.head(20))
