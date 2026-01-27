import streamlit as st
import pandas as pd
from src.data_loader import load_real_estate_data
from src.analytics import get_country_stats

st.title("🏠 Analyse de l'Immobilier Mondial")

# Chargement des données via le module de l'Étudiant 1
df = load_real_estate_data("data/raw/global_housing_market_extended.csv")

if df is not None:
    st.success("Données chargées avec succès !")
    
    # Sélecteur de pays
    countries = df['Country'].unique()
    selected_country = st.selectbox("Choisissez un pays", countries)
    
    # Affichage des stats via la fonction de l'Étudiant 1
    stats = get_country_stats(df, selected_country)
    
    if "error" not in stats:
        col1, col2 = st.columns(2)
        col1.metric("Prix Moyen Index", stats['avg_house_price_index'])
        col2.metric("Croissance GDP", f"{stats['latest_gdp_growth']}%")
    else:
        st.error(stats["error"])
else:
    st.error("Impossible de charger les données. Vérifiez le dossier data/raw/")