import sqlite3
import pathlib
import sys

# Import local modules
import scripts.dwbuilder as dwb

# Constants
DW_DIR = pathlib.Path("data").joinpath("dw")
DB_PATH = DW_DIR.joinpath("block_smart_sales.db")
PREPARED_DATA_DIR = pathlib.Path("data").joinpath("prepared")

conn = sqlite3.connect("your_database.db")

# Build the data warehouse from the schema file
dwb.execute_sql_file(conn, "schema.sql")

# Load data from 'customers.csv' into the 'customers' table, deleting existing records first.
dwb.csv_to_dw("customers.csv", conn, "customers")

# Load data from 'products.csv' into the 'products' table, without deleting existing records.
dwb.csv_to_dw("products.csv", conn, "products", delete_first=False)

conn.close()
