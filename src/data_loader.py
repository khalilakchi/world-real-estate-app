import pandas as pd
import logging
from pathlib import Path
from typing import Optional

# Configure logging to show timestamp and level (INFO/ERROR)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_real_estate_data(file_path: str) -> Optional[pd.DataFrame]:
    """
    Loads the real estate dataset from a CSV file.

    Args:
        file_path (str): The relative path to the CSV file.

    Returns:
        Optional[pd.DataFrame]: A pandas DataFrame containing the data, 
                                or None if the file is not found.
    """
    path = Path(file_path)
    
    # Check if file exists before trying to read it
    if not path.exists():
        logging.error(f"File not found at: {path.absolute()}")
        return None

    try:
        df = pd.read_csv(path)
        logging.info(f"Successfully loaded data: {len(df)} rows, {len(df.columns)} columns.")
        
        # Verify essential columns exist
        required_cols = ['Country', 'Year', 'House Price Index']
        if not all(col in df.columns for col in required_cols):
            logging.error(f"Missing required columns. Found: {df.columns.tolist()}")
            return None
            
        return df

    except Exception as e:
        logging.error(f"Error loading data: {e}")
        return None

if __name__ == "__main__":
    # This block only runs when you execute this file directly
    # It tests if the data loads correctly
    test_path = "data/raw/global_housing_market_extended.csv"
    df = load_real_estate_data(test_path)
    
    if df is not None:
        print("\n--- Preview of Data ---")
        print(df.head())