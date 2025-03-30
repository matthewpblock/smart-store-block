import pandas as pd
import sqlite3
import pathlib
import sys

# Import local modules
import utils.logger as logger

# For local imports, temporarily add project root to sys.path
PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

# Constants
DW_DIR = pathlib.Path("data").joinpath("dw")
DB_PATH = DW_DIR.joinpath("block_smart_sales.db")
PREPARED_DATA_DIR = pathlib.Path("data").joinpath("prepared")

###################################################################
# Functions
###################################################################
def execute_sql_file(connection, file_path) -> None:
    """
    Executes a SQL file using the provided SQLite connection.

    Args:
        connection (sqlite3.Connection): SQLite connection object.
        file_path (str): Path to the SQL file to be executed.
    """
    # We know reading from a file can raise exceptions, so we wrap it in a try block
    try:
        with open(file_path, 'r') as file:
            # Read the SQL file into a string
            sql_script: str = file.read()
        with connection:
            # Use the connection as a context manager to execute the SQL script
            connection.executescript(sql_script)
            logger.info(f"Executed: {file_path}")
    except Exception as e:
        logger.error(f"Failed to execute {file_path}: {e}")
        raise

def create_schema(cursor: sqlite3.Cursor) -> None:
    """Create tables in the data warehouse if they don't exist."""
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customer (
            customer_id INTEGER PRIMARY KEY,
            name TEXT,
            region TEXT,
            join_date TEXT
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS product (
            product_id INTEGER PRIMARY KEY,
            product_name TEXT,
            category TEXT
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sale (
            sale_id INTEGER PRIMARY KEY,
            customer_id INTEGER,
            product_id INTEGER,
            sale_amount REAL,
            sale_date TEXT,
            FOREIGN KEY (customer_id) REFERENCES customer (customer_id),
            FOREIGN KEY (product_id) REFERENCES product (product_id)
        )
    """)

def delete_existing_records(cursor: sqlite3.Cursor) -> None:
    """Delete all existing records from the customer, product, and sale tables."""
    cursor.execute("DELETE FROM customer")
    cursor.execute("DELETE FROM product")
    cursor.execute("DELETE FROM sale")

def insert_customers(customers_df: pd.DataFrame, cursor: sqlite3.Cursor) -> None:
    """Insert customer data into the customer table."""
    customers_df.to_sql("customer", cursor.connection, if_exists="append", index=False)

def insert_products(products_df: pd.DataFrame, cursor: sqlite3.Cursor) -> None:
    """Insert product data into the product table."""
    products_df.to_sql("product", cursor.connection, if_exists="append", index=False)

def insert_sales(sales_df: pd.DataFrame, cursor: sqlite3.Cursor) -> None:
    """Insert sales data into the sales table."""
    sales_df.to_sql("sale", cursor.connection, if_exists="append", index=False)

def load_data_to_db() -> None:
    try:
        # Connect to SQLite – will create the file if it doesn't exist
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Create schema and clear existing records
        create_schema(cursor)
        delete_existing_records(cursor)

        # Load prepared data using pandas
        customers_df = pd.read_csv(PREPARED_DATA_DIR.joinpath("customers_data_prepared.csv"))
        products_df = pd.read_csv(PREPARED_DATA_DIR.joinpath("products_data_prepared.csv"))
        sales_df = pd.read_csv(PREPARED_DATA_DIR.joinpath("sales_data_prepared.csv"))

        # Insert data into the database
        insert_customers(customers_df, cursor)
        insert_products(products_df, cursor)
        insert_sales(sales_df, cursor)

        conn.commit()
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    load_data_to_db()