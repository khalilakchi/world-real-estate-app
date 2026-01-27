import streamlit as st
import plotly.express as px
import logging
import numpy as np
import pandas as pd
# Import local modules 
from src.data_loader import load_real_estate_data
from src.analytics import get_country_stats, get_top_growth_countries
from src.api_client import get_usd_exchange_rates, convert_currency

# 1. Page and Logging Configuration
st.set_page_config(page_title="World Real Estate Market Analyzer", layout="wide")
logging.basicConfig(level=logging.INFO)

def main():
    st.title("🏠 World Real Estate Market Analyzer")
    
    # 2. Data and API Loading
    path = "data/raw/global_housing_market_extended.csv"
    df = load_real_estate_data(path)
    rates = get_usd_exchange_rates()
    
    if df is not None:
        logging.info("Data successfully loaded for the interface")

        # --- SECTION: WORLD MAP ---
        st.header("🌍 Global Real Estate Overview")
        latest_year = df['Year'].max()
        df_latest = df[df['Year'] == latest_year]

        fig_map = px.choropleth(
            df_latest, 
            locations="Country", 
            locationmode='country names',
            color="House Price Index",
            hover_name="Country",
            color_continuous_scale=px.colors.sequential.Viridis,
            labels={'House Price Index': 'Price Index'},
            title=f"Global House Price Index in {latest_year}"
        )

        # Map design improvements
        fig_map.update_layout(
            geo=dict(
                showframe=False,
                showcoastlines=True,
                projection_type='equirectangular',
                bgcolor='rgba(0,0,0,0)' # Transparent background
            ),
            margin={"r":0,"t":40,"l":0,"b":0},
            coloraxis_colorbar=dict(title="Index", thicknessmode="pixels", thickness=15)
        )

        st.plotly_chart(fig_map, use_container_width=True)

        # --- SIDEBAR: FILTERS AND COMPARISON ---
        st.sidebar.header("Configuration")
        
        # Advanced Filters
        st.sidebar.header("🎯 Advanced Filters")
        surface = st.sidebar.slider("Minimum Surface (m²)", 0, 500, 50)
        rooms = st.sidebar.number_input("Minimum Number of Rooms", 0, 10, 1)

        # Country Comparison
        st.sidebar.header("⚖️ Country Comparison")
        country_1 = st.sidebar.selectbox("Country A", df['Country'].unique(), index=0)
        country_2 = st.sidebar.selectbox("Country B", df['Country'].unique(), index=1)
        
        # --- SECTION 1: COUNTRY STATISTICS ---
        st.divider()
        st.header("📊 Country-Specific Statistics")
        selected_country = st.selectbox("Select a country for detailed analysis", df['Country'].unique())
        
        stats = get_country_stats(df, selected_country)
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Avg Price (Index)", stats.get('avg_house_price_index', "N/A"))
        with col2:
            st.metric("Max Inflation", f"{stats.get('max_inflation', 0)}%")
        with col3:
            if rates:
                price_index = stats.get('avg_house_price_index', 0)
                converted_price = convert_currency(price_index, 'EUR', rates)
                st.metric("Avg Price (Est. EUR)", f"{converted_price} €")

        # --- SECTION 2: TIME SERIES VISUALIZATION ---
        st.subheader(f"Price Evolution: {selected_country}")
        country_df = df[df['Country'] == selected_country]
        fig_line = px.line(country_df, x='Year', y='House Price Index', 
                          title=f"House Price Index over Time ({selected_country})",
                          markers=True)
        st.plotly_chart(fig_line, use_container_width=True)

        # --- SECTION: COMPARISON RESULTS ---
        if st.sidebar.button("Run Comparison"):
            st.divider()
            st.header(f"🆚 Comparison: {country_1} vs {country_2}")
            res1 = get_country_stats(df, country_1)
            res2 = get_country_stats(df, country_2)
            
            c1, c2 = st.columns(2)
            c1.metric(f"{country_1} Avg Price", res1.get('avg_house_price_index'))
            c2.metric(f"{country_2} Avg Price", res2.get('avg_house_price_index'))

        # --- SECTION 3: GROWTH ANALYSIS ---
        st.divider()
        st.header("🚀 Top 5 GDP Growth")
        year = st.slider("Select Year", int(df['Year'].min()), int(df['Year'].max()), 2019)
        top_df = get_top_growth_countries(df, year)
        
        if not top_df.empty:
            st.table(top_df)
        else:
            st.warning(f"No growth data available for the year {year}")

    else:
        st.error(f"File not found: {path}. Please place it in data/raw/")

    # Technical Footer
    st.sidebar.divider()
    st.sidebar.caption(f"Backend: Python 3.11 | NumPy: {np.__version__}")

if __name__ == "__main__":
    main()