import sqlite3
import pathlib
import sys
import os

# Get the path to the project directory (assuming it's one level up)
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
 # Add the parent directory to sys.path
sys.path.append(parent_dir)
 
# Local Imports
from utils.logger import logger
import dwbuilder as dwb

##############################################
# Constants (UPDATE PATHS TO CUSTOMIZE)
##############################################
DW_DIR = pathlib.Path("data").joinpath("dw")
DB_PATH = DW_DIR.joinpath("block_smart_sales.db")
PREPARED_DATA_DIR = pathlib.Path("data").joinpath("prepared")
SQL_PATH = pathlib.Path("scripts/schema.sql")

# Ensure the DW directory exists
DW_DIR.mkdir(parents=True, exist_ok=True)

# Connect to the database
conn = sqlite3.connect(str(DB_PATH))

# Construct the full paths to the CSV files (UPDATE SOURCES TO CUSTOMIZE)
customers_csv_path = PREPARED_DATA_DIR.joinpath("customers_data_prepared.csv")
products_csv_path = PREPARED_DATA_DIR.joinpath("products_data_prepared.csv")
sales_csv_path = PREPARED_DATA_DIR.joinpath("sales_data_prepared.csv")

################################################
# Execution Scripts
################################################
# Build the data warehouse from the schema file
dwb.execute_sql_file(conn, SQL_PATH)

# Load data from 'customers.csv' into the 'customers' table (UPDATE ARGUMENTS TO CUSTOMIZE)
dwb.csv_to_dw(str(customers_csv_path), conn, "customers", delete_first=True)

# Load data from 'products.csv' into the 'products' table, without deleting existing records.
dwb.csv_to_dw(str(products_csv_path), conn, "products", delete_first=True)

# Load data from 'sales.csv' into the 'sales' table, deleting existing records.
dwb.csv_to_dw(str(sales_csv_path), conn, "sales", delete_first=True)

conn.close()
