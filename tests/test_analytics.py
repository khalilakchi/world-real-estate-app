import pytest
import pandas as pd
from src.analytics import get_country_stats

def test_get_country_stats_not_found():
    """Vérifie que la fonction gère correctement un pays inexistant."""
    # Création d'un petit DataFrame de test
    df_test = pd.DataFrame({'Country': ['France'], 'House Price Index': [100.0], 
                            'Rent Index': [90.0], 'Inflation Rate (%)': [2.0], 
                            'Year': [2023], 'GDP Growth (%)': [1.0]})
    
    # On teste avec un pays qui n'est pas dans le DataFrame
    result = get_country_stats(df_test, "Atlantide")
    
    # Vérification (Assertion)
    assert "error" in result
    assert result["error"] == "Country 'Atlantide' not found in dataset."