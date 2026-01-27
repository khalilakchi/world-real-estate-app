import pytest
import pandas as pd
from src.analytics import get_country_stats

# 1. Use a Fixture to avoid recreating the DataFrame for every test
@pytest.fixture
def sample_data():
    """Provides a minimal dataset for testing purposes."""
    return pd.DataFrame({
        'Country': ['USA', 'USA', 'France'],
        'Year': [2020, 2021, 2020],
        'House Price Index': [100.0, 110.0, 105.0],
        'Rent Index': [50.0, 55.0, 60.0],
        'Inflation Rate (%)': [2.0, 3.0, 1.0],
        'GDP Growth (%)': [1.5, 2.0, 1.2]
    })

# 2. Test nominal case (Success)
def test_get_country_stats_valid(sample_data):
    """Verifies average calculations for an existing country."""
    stats = get_country_stats(sample_data, 'USA')
    # Average of 100 and 110 = 105
    assert stats['avg_house_price_index'] == 105.0
    assert stats['country'] == 'USA'
    assert "data_years" in stats

# 3. Test error case (Fail)
def test_get_country_stats_invalid(sample_data):
    """Verifies handling of a country that does not exist in the dataset."""
    result = get_country_stats(sample_data, 'Mars')
    assert "error" in result
    assert "Mars" in result["error"]