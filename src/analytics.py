import pandas as pd
from typing import Dict, Any, List

def get_country_stats(df: pd.DataFrame, country: str) -> Dict[str, Any]:
    """
    Calculates key metrics for a specific country using the loaded data.
    
    Args:
        df (pd.DataFrame): The full dataset.
        country (str): The country name (case-sensitive, e.g., 'USA').
        
    Returns:
        Dict[str, Any]: A dictionary with Average Price, Max Inflation, etc.
                        Returns an error message if country is not found.
    """
    # Filter for the specific country
    subset = df[df['Country'] == country]
    
    if subset.empty:
        return {"error": f"Country '{country}' not found in dataset."}
    
    # Calculate metrics
    stats = {
        "country": country,
        "avg_house_price_index": round(subset['House Price Index'].mean(), 2),
        "avg_rent_index": round(subset['Rent Index'].mean(), 2),
        "max_inflation": round(subset['Inflation Rate (%)'].max(), 2),
        "latest_gdp_growth": round(subset.iloc[-1]['GDP Growth (%)'], 2), # Assumes data is sorted by year
        "data_years": f"{subset['Year'].min()} - {subset['Year'].max()}"
    }
    
    return stats

def get_top_growth_countries(df: pd.DataFrame, year: int = 2023) -> pd.DataFrame:
    """
    Identifies countries with the highest GDP growth in a specific year.
    
    Args:
        df (pd.DataFrame): Full dataset.
        year (int): The year to analyze.
        
    Returns:
        pd.DataFrame: A table of the top 5 countries sorted by GDP Growth.
    """
    # Filter by year
    yearly_data = df[df['Year'] == year].copy()
    
    if yearly_data.empty:
        return pd.DataFrame() # Return empty if year doesn't exist
        
    # Sort by GDP Growth descending and take top 5
    top_5 = yearly_data.sort_values(by='GDP Growth (%)', ascending=False).head(5)
    
    return top_5[['Country', 'GDP Growth (%)', 'House Price Index', 'Inflation Rate (%)']]

# --- Test Block (Runs only when executing this file) ---
if __name__ == "__main__":
    from data_loader import load_real_estate_data
    
    # 1. Load Data
    df = load_real_estate_data("data/raw/global_housing_market_extended.csv")
    
    if df is not None:
        # 2. Test Country Stats
        print("\n--- Testing USA Stats ---")
        stats = get_country_stats(df, "USA")
        print(stats)
        
        # 3. Test Top Growth
        print("\n--- Testing Top 5 Countries by GDP (2019) ---")
        top_growth = get_top_growth_countries(df, 2019)
        print(top_growth.to_string(index=False))