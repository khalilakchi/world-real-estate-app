import requests
import logging
from typing import Optional, Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_usd_exchange_rates() -> Optional[Dict[str, float]]:
    """
    Fetches the latest USD exchange rates from a public API.
    
    Returns:
        Optional[Dict[str, float]]: A dictionary of rates (e.g., {'EUR': 0.92, 'GBP': 0.79}),
                                    or None if the request fails.
    """
    api_url = "https://open.er-api.com/v6/latest/USD"
    
    try:
        logging.info(f"Fetching live exchange rates from {api_url}...")
        response = requests.get(api_url, timeout=10) # 10-second timeout (Best Practice)
        
        # Check if the request was successful (Status Code 200)
        response.raise_for_status()
        
        data = response.json()
        
        # Validate the response structure
        if "rates" not in data:
            logging.error("Invalid API response format: 'rates' key missing.")
            return None
            
        logging.info("Successfully retrieved exchange rates.")
        return data["rates"]

    except requests.exceptions.Timeout:
        logging.error("The API request timed out.")
        return None
    except requests.exceptions.ConnectionError:
        logging.error("Connection error. Please check your internet.")
        return None
    except requests.exceptions.RequestException as e:
        logging.error(f"An unexpected API error occurred: {e}")
        return None

def convert_currency(amount: float, target_currency: str, rates: Dict[str, float]) -> Optional[float]:
    """
    Helper function to convert an amount from USD to a target currency.
    """
    if target_currency not in rates:
        logging.warning(f"Currency '{target_currency}' not found in exchange rates.")
        return None
        
    rate = rates[target_currency]
    return round(amount * rate, 2)

# --- Test Block ---
if __name__ == "__main__":
    # 1. Fetch Rates
    rates = get_usd_exchange_rates()
    
    if rates:
        print("\n--- Live Exchange Rates (Base: USD) ---")
        print(f"1 USD = {rates.get('EUR')} EUR")
        print(f"1 USD = {rates.get('GBP')} GBP")
        print(f"1 USD = {rates.get('JPY')} JPY")
        
        # 2. Test Conversion
        price_index = 150.80  # Example value from your data
        converted = convert_currency(price_index, 'EUR', rates)
        print(f"\nExample Conversion: Index {price_index} USD is approx {converted} EUR")