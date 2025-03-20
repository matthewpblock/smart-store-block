import pandas as pd
import sys
import os

# Get the path to the directory containing 'utils' (assuming it's two levels up)
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
 # Add the parent directory to sys.path
sys.path.append(parent_dir)
 
# Local Imports
from utils.logger import logger

########################################
# Functions
########################################

def verify_columns(df: pd.DataFrame, expected_columns: dict) -> bool:
    """
    Verifies the correct number and type of columns in a DataFrame.

    Args:
        df: The DataFrame to check.
        expected_columns: A dictionary where keys are column names and values are expected data types (e.g., 'int64', 'float64', 'object').

    Returns:
        True if the DataFrame has the correct columns and types, False otherwise.
    """
    logger.info("Verifying columns and types...")

    # Check if the number of columns is correct
    if len(df.columns) != len(expected_columns):
        logger.error(f"Incorrect number of columns. Expected: {len(expected_columns)}, Found: {len(df.columns)}")
        return False

    # Check if all expected columns are present
    for col_name in expected_columns:
        if col_name not in df.columns:
            logger.error(f"Missing column: {col_name}")
            return False

    # Check the data type of each column
    for col_name, expected_type in expected_columns.items():
        actual_type = str(df[col_name].dtype)
        if actual_type != expected_type:
            logger.error(f"Incorrect data type for column '{col_name}'. Expected: {expected_type}, Found: {actual_type}")
            return False

    logger.info("Columns and types verified successfully.")
    return True

def convert_wholesale_price_to_float(df: pd.DataFrame) -> pd.DataFrame:
    """Converts the 'WholesalePrice' column to float, handling errors."""
    logger.info("Converting 'WholesalePrice' column to float...")

    try:
        # Convert 'WholesalePrice' to float, coercing errors to NaN
        df['WholesalePrice'] = df['WholesalePrice'].astype('float64')
        
        #Check for remaining non-numeric values after cleaning
        non_numeric_count = df['WholesalePrice'].isnull().sum()
        if non_numeric_count > 0:
            logger.warning(f"Found {non_numeric_count} non-numeric values in 'WholesalePrice' after cleaning.  These will be NaN.")

        logger.info("'WholesalePrice' column successfully converted to float.")
    except Exception as e:
        logger.error(f"Error converting 'WholesalePrice' to float: {e}")
    return df

def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Removes duplicate rows from the DataFrame."""
    df.drop_duplicates(inplace=True)
    return df


########################################
# Main Execution
########################################
def main() -> None:
    """Main function for processing customer, product, and sales data."""
    logger.info("Starting data preparation...")

    try:
        df_products = pd.read_csv("data/raw/products_data.csv")

        # Convert WholesalePrice to float *before* verification
        df_products = convert_wholesale_price_to_float(df_products)
        
        expected_cols = {
            "ProductID": "int64",
            "ProductName": "object",
            "Category": "object",
            "UnitPrice": "float64",
            "WholesalePrice": "float64",
            "Supplier": "object",
        }

        
        if verify_columns(df_products, expected_cols):
            logger.info("Proceeding with data processing...")
            df_products = remove_duplicates(df_products)

            # Create the 'data/prepared' directory if it doesn't exist
            prepared_data_dir = "data/prepared"
            os.makedirs(prepared_data_dir, exist_ok=True)

            # Write the processed DataFrame to a CSV file in the 'data/prepared' directory
            output_filepath = os.path.join(prepared_data_dir, "products_data_prepared.csv")
            df_products.to_csv(output_filepath, index=False)  # index=False prevents writing the index
            logger.info(f"Processed data saved to: {output_filepath}")

        else:
            logger.error("Data validation failed. Exiting.")
            return
    except FileNotFoundError:
        logger.error("products_data.csv not found")
        return

    logger.info("Data preparation complete.")


if __name__ == "__main__":
    main()
