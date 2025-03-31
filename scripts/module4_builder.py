import sqlite3
import pathlib

# Import local modules
import dwbuilder as dwb

# Constants
DW_DIR = pathlib.Path("data").joinpath("dw")
DB_PATH = DW_DIR.joinpath("block_smart_sales.db")
PREPARED_DATA_DIR = pathlib.Path("data").joinpath("prepared")
SQL_PATH = pathlib.Path("scripts/schema.sql")

# Ensure the DW directory exists
DW_DIR.mkdir(parents=True, exist_ok=True)

# Connect to the database
conn = sqlite3.connect(str(DB_PATH))

# Build the data warehouse from the schema file
dwb.execute_sql_file(conn, SQL_PATH)

# Construct the full paths to the CSV files
customers_csv_path = PREPARED_DATA_DIR.joinpath("customers.csv")
products_csv_path = PREPARED_DATA_DIR.joinpath("products.csv")
sales_csv_path = PREPARED_DATA_DIR.joinpath("sales.csv")

# Load data from 'customers.csv' into the 'customers' table
dwb.csv_to_dw(str(customers_csv_path), conn, "customers")

# Load data from 'products.csv' into the 'products' table, without deleting existing records.
dwb.csv_to_dw(str(products_csv_path), conn, "products")

# Load data from 'sales.csv' into the 'sales' table, deleting existing records.
dwb.csv_to_dw(str(sales_csv_path), conn, "sales")

conn.close()
