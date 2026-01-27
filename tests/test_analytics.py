import pytest
import pandas as pd
from src.analytics import get_country_stats, get_top_growth_countries

# 1. Création d'un "Fixture" : un petit jeu de données de test
# Cela évite de charger le gros fichier CSV à chaque test
@pytest.fixture
def sample_data():
    data = {
        'Country': ['USA', 'USA', 'France', 'France'],
        'Year': [2022, 2023, 2022, 2023],
        'House Price Index': [100.0, 110.0, 90.0, 95.0],
        'Rent Index': [105.0, 108.0, 92.0, 94.0],
        'Inflation Rate (%)': [8.0, 4.0, 5.0, 3.0],
        'GDP Growth (%)': [2.1, 1.5, 1.8, 0.9]
    }
    return pd.DataFrame(data)

# 2. Test d'un cas qui doit fonctionner (Succès)
def test_get_country_stats_success(sample_data):
    stats = get_country_stats(sample_data, "USA")
    
    assert stats['country'] == "USA"
    assert stats['avg_house_price_index'] == 105.0  # (100+110)/2
    assert "error" not in stats [cite: 44, 48]

# 3. Test d'un pays inexistant (Cas d'erreur géré)
def test_get_country_stats_not_found(sample_data):
    stats = get_country_stats(sample_data, "Atlantide")
    
    assert "error" in stats
    assert "not found" in stats['error'] [cite: 44]

# 4. Test de la croissance GDP
def test_get_top_growth_countries(sample_data):
    top_5 = get_top_growth_countries(sample_data, 2023)
    
    assert len(top_5) <= 5
    assert top_5.iloc[0]['Country'] == "USA" # Car 1.5 > 0.9