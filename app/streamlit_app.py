import streamlit as st
import plotly.express as px
import logging
import numpy as np
import pandas as pd
# Importation des modules locaux
from src.data_loader import load_real_estate_data
from src.analytics import get_country_stats, get_top_growth_countries
from src.api_client import get_usd_exchange_rates, convert_currency

# 1. Configuration de la page et du logging
st.set_page_config(page_title="World Real Estate Market Analyzer", layout="wide")
logging.basicConfig(level=logging.INFO)

def main():
    st.title("🏠 World Real Estate Market Analyzer")
    
    # 2. Chargement des données et API
    path = "data/raw/global_housing_market_extended.csv"
    df = load_real_estate_data(path)
    rates = get_usd_exchange_rates()
    
    if df is not None:
        logging.info("Données chargées pour l'interface")

        # --- SECTION : CARTE DU MONDE ---
        st.header("🌍 Aperçu Mondial des Prix")
        latest_year = df['Year'].max()
        df_latest = df[df['Year'] == latest_year]
        
        fig_map = px.choropleth(df_latest, 
                                locations="Country", 
                                locationmode='country names',
                                color="House Price Index",
                                hover_name="Country",
                                title=f"Indice des prix immobiliers mondiaux en {latest_year}",
                                color_continuous_scale=px.colors.sequential.Plasma)
        st.plotly_chart(fig_map, width='stretch')

        # --- BARRE LATÉRALE : FILTRES ET COMPARAISON ---
        st.sidebar.header("Configuration")
        
        # Filtres Avancés (Préparation pour l'évolution du dataset)
        st.sidebar.header("🎯 Filtres Avancés")
        surface = st.sidebar.slider("Surface minimum (m²)", 0, 500, 50)
        chambres = st.sidebar.number_input("Nombre de chambres minimum", 0, 10, 1)

        # Comparaison de Pays
        st.sidebar.header("⚖️ Comparaison de Pays")
        country_1 = st.sidebar.selectbox("Pays A", df['Country'].unique(), index=0)
        country_2 = st.sidebar.selectbox("Pays B", df['Country'].unique(), index=1)
        
        # --- SECTION 1 : STATISTIQUES PAR PAYS ---
        st.divider()
        st.header("📊 Statistiques par Pays")
        selected_country = st.selectbox("Sélectionnez un pays pour l'analyse détaillée", df['Country'].unique())
        
        stats = get_country_stats(df, selected_country)
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Prix Moyen (Index)", stats.get('avg_house_price_index', "N/A"))
        with col2:
            st.metric("Inflation Max", f"{stats.get('max_inflation', 0)}%")
        with col3:
            if rates:
                price_index = stats.get('avg_house_price_index', 0)
                converted_price = convert_currency(price_index, 'EUR', rates)
                st.metric("Prix Moyen (Est. EUR)", f"{converted_price} €")

        # --- SECTION 2 : VISUALISATION TEMPORELLE ---
        st.subheader(f"Évolution temporelle : {selected_country}")
        country_df = df[df['Country'] == selected_country]
        fig_line = px.line(country_df, x='Year', y='House Price Index', 
                          title=f"Indice des prix à travers le temps ({selected_country})",
                          markers=True)
        st.plotly_chart(fig_line, width='stretch')

        # --- SECTION : RESULTAT DE LA COMPARAISON ---
        if st.sidebar.button("Lancer la comparaison"):
            st.divider()
            st.header(f"🆚 Comparaison : {country_1} vs {country_2}")
            res1 = get_country_stats(df, country_1)
            res2 = get_country_stats(df, country_2)
            
            c1, c2 = st.columns(2)
            c1.metric(f"Prix Moyen {country_1}", res1.get('avg_house_price_index'))
            c2.metric(f"Prix Moyen {country_2}", res2.get('avg_house_price_index'))

        # --- SECTION 3 : ANALYSE DE LA CROISSANCE ---
        st.divider()
        st.header("🚀 Top 5 Croissance GDP")
        year = st.slider("Choisir une année", int(df['Year'].min()), int(df['Year'].max()), 2019)
        top_df = get_top_growth_countries(df, year)
        
        if not top_df.empty:
            st.table(top_df)
        else:
            st.warning(f"Aucune donnée de croissance disponible pour l'année {year}")

    else:
        st.error(f"Fichier introuvable : {path}. Veuillez le placer dans data/raw/")

    # Footer technique
    st.sidebar.divider()
    st.sidebar.caption(f"Backend: Python 3.11 | NumPy: {np.__version__}")

if __name__ == "__main__":
    main()