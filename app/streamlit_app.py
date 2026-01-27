import streamlit as st
import plotly.express as px
import logging
from src.data_loader import load_real_estate_data

# 1. Configuration de la page
st.set_page_config(page_title="Immo Global Dashboard", layout="wide")
logging.basicConfig(level=logging.INFO)

def main():
    st.title("🏠 Analyse du Marché Immobilier")
    
    # 2. Chargement des données
    path = "data/raw/global_housing_market_extended.csv"
    df = load_real_estate_data(path)
    
    if df is not None:
        logging.info("Données chargées pour l'interface")
        
        # 3. Sidebar pour les filtres
        st.sidebar.header("Filtres")
        country_list = df['Country'].unique()
        selected_country = st.sidebar.selectbox("Sélectionnez un pays", country_list)
        
        # 4. Graphique interactif
        st.subheader(f"Évolution des prix : {selected_country}")
        country_df = df[df['Country'] == selected_country]
        
        fig = px.line(country_df, x='Year', y='House Price Index', 
                     title=f"Indice des prix à travers le temps ({selected_country})",
                     markers=True)
        st.plotly_chart(fig, use_container_width=True)
        
    else:
        st.error(f"Fichier introuvable : {path}. Veuillez le placer dans data/raw/")

if __name__ == "__main__":
    main()