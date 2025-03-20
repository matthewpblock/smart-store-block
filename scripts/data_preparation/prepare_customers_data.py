import pandas as pd

# Local Imports
from utils.logger import logger
import data_prep as dp

########################################
# Functions
########################################

def check_columns(df: pd.DataFrame) -> None:
    
def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    
def remove_outliers(df: pd.DataFrame) -> pd.DataFrame:
########################################
# Main Execution
########################################
def main() -> None:
    """Main function for processing customer, product, and sales data."""
    logger.info("Starting data preparation...")
    dp.process_data("customers_data.csv")
    logger.info("Data preparation complete.")

if __name__ == "__main__":
    main()
dp.process_data("customers_data.csv")


if __name__ == "__main__":
    main()