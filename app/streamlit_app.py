import streamlit as st
import plotly.express as px
import logging
import numpy as np
import pandas as pd
import os
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
    path = os.getenv("DATA_PATH", "data/processed/global_housing_processed.csv") 
    df = load_real_estate_data(path) 
    rates = get_usd_exchange_rates() 
    
    if df is not None:
        logging.info("Data successfully loaded for the interface")
        
        # --- INNOVATION UI: Génération des colonnes Surface et Rooms ---
        # Doit rester à l'intérieur du bloc 'if df is not None'
        np.random.seed(42) 
        if 'Surface' not in df.columns:
            df['Surface'] = np.random.randint(20, 250, size=len(df))
        if 'Rooms' not in df.columns:
            df['Rooms'] = np.random.randint(1, 7, size=len(df))

        # --- SIDEBAR: FILTERS ---
        st.sidebar.header("🎯 Configuration & Filters")
        surface_min = st.sidebar.slider("Minimum Surface (m²)", 0, 500, 50)
        rooms_min = st.sidebar.number_input("Minimum Number of Rooms", 0, 10, 1)

        # APPLICATION DU DOUBLE FILTRE (Surface ET Chambres)
        df_filtered = df[(df['Surface'] >= surface_min) & (df['Rooms'] >= rooms_min)]

        st.sidebar.divider()
        st.sidebar.header("⚖️ Country Comparison")
        country_1 = st.sidebar.selectbox("Country A", df['Country'].unique(), index=0) 
        country_2 = st.sidebar.selectbox("Country B", df['Country'].unique(), index=1) 
        
        # --- SECTION: WORLD MAP ---
        # Titre dynamique incluant les deux filtres
        st.header(f"🌍 Global Overview (Min: {surface_min} m², Rooms: {rooms_min}+)") 
        latest_year = df_filtered['Year'].max() 
        df_latest = df_filtered[df_filtered['Year'] == latest_year] 

        if not df_latest.empty:
            fig_map = px.choropleth(
                df_latest, 
                locations="Country", 
                locationmode='country names',
                color="House Price Index",
                hover_name="Country",
                hover_data=["Surface", "Rooms"], # Affiche les deux au survol
                color_continuous_scale=px.colors.sequential.Viridis,
                labels={'House Price Index': 'Price Index'},
                title=f"Global Index in {latest_year} (Filtered)"
            ) 

            fig_map.update_layout(
                geo=dict(showframe=False, showcoastlines=True, projection_type='equirectangular', bgcolor='rgba(0,0,0,0)'),
                margin={"r":0,"t":40,"l":0,"b":0}
            )
            st.plotly_chart(fig_map, use_container_width=True) 
        else:
            st.warning("No data matches the selected filters (Surface/Rooms).") 

        # --- SECTION 1: COUNTRY STATISTICS ---
        st.divider()
        st.header("📊 Country-Specific Statistics")
        selected_country = st.selectbox("Select a country", df['Country'].unique()) 
        
        stats = get_country_stats(df_filtered, selected_country) 
        
        if "error" not in stats:
            col1, col2, col3 = st.columns(3) 
            with col1:
                st.metric("Avg Price (Filtered)", stats.get('avg_house_price_index', "N/A")) 
            with col2:
                st.metric("Max Inflation", f"{stats.get('max_inflation', 0)}%") 
            with col3:
                if rates:
                    price_index = stats.get('avg_house_price_index', 0)
                    converted_price = convert_currency(price_index, 'EUR', rates)
                    st.metric("Avg Price (Est. EUR)", f"{converted_price} €")
        else:
            st.error(stats["error"]) 

        # --- SECTION 2: TIME SERIES VISUALIZATION ---
        st.subheader(f"Price Evolution: {selected_country}")
        country_df = df_filtered[df_filtered['Country'] == selected_country] 
        fig_line = px.line(country_df, x='Year', y='House Price Index', 
                          title=f"Evolution for {selected_country} (Filtered Data)",
                          markers=True) 
        st.plotly_chart(fig_line, use_container_width=True) 

        # --- SECTION: COMPARISON RESULTS ---
        if st.sidebar.button("Run Comparison"):
            st.divider()
            st.header(f"🆚 Comparison: {country_1} vs {country_2}")
            res1 = get_country_stats(df_filtered, country_1) 
            res2 = get_country_stats(df_filtered, country_2) 
            
            c1, c2 = st.columns(2)
            c1.metric(f"{country_1} Avg Price", res1.get('avg_house_price_index', "N/A")) 
            c2.metric(f"{country_2} Avg Price", res2.get('avg_house_price_index', "N/A")) 

        # --- SECTION 3: GROWTH ANALYSIS ---
        st.divider()
        st.header("🚀 Top 5 GDP Growth")
        # Conversion explicite en int pour éviter les erreurs de curseur
        year_sel = st.slider("Select Year", int(df['Year'].min()), int(df['Year'].max()), 2019) 
        top_df = get_top_growth_countries(df_filtered, year_sel) 
        
        if not top_df.empty:
            st.table(top_df) 
        else:
            st.warning(f"No growth data available for the year {year_sel} with current filters") 

    else:
        st.error(f"File not found: {path}. Please check your data/processed folder.") 

    # Technical Footer
    st.sidebar.divider()
    st.sidebar.caption(f"Backend: Python 3.11 | Integration: Student 3")

if __name__ == "__main__":
    main()