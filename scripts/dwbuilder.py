import pandas as pd
import sqlite3
import sys
import os
import re


# Import local modules
# Get the path to the directory containing 'utils' (assuming it's one level up)
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
 # Add the parent directory to sys.path
sys.path.append(parent_dir)
 
# Local Imports
from utils.logger import logger

###################################################################
# Functions
###################################################################
# Function to run SQL files, e.g., schema.sql, data.sql
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
    
# Function to remove records from tables in the data warehouse 
def delete_existing_records(cursor: sqlite3.Cursor, table_name: str, should_delete: bool = False) -> None:
    """
    Delete existing records from specified tables.

    Args:
        cursor (sqlite3.Cursor): The database cursor.
        table_name (str): Name of the table to delete from.
        should_delete (bool): True to delete, False to skip.
    """
    if should_delete:
        try:
            cursor.execute(f"DELETE FROM {table_name}")
            logger.info(f"Deleted all records from table: {table_name}")
        except sqlite3.OperationalError as e:
            logger.error(f"Error deleting from table {table_name}: {e}")
            raise

def load_csv(file_path: str) -> pd.DataFrame:
    """
    Load a CSV file into a DataFrame.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        pd.DataFrame: DataFrame containing the loaded data.
    """
    try:
        df = pd.read_csv(file_path)
        logger.info(f"Loaded CSV file: {file_path}")
        return df
    except Exception as e:
        logger.error(f"Failed to load CSV file {file_path}: {e}")
        raise

# Prepare the DataFrame for SQL insertion by removing uppercase letters and special characters
#TODO: Implement this function to convert DataFrame column names to lowercase and remove special characters
def convert_to_sql_format(df: pd.DataFrame) -> str:
    """
    Convert a DataFrame to SQL format for insertion into a database.

    Args:
        df (pd.DataFrame): DataFrame to convert.

    Returns:
        str: SQL formatted string for insertion.
    """
    try:
        new_columns = []
        for col in df.columns:
            # Insert underscore before uppercase letters
            new_col = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', col)
            new_col = re.sub('([a-z0-9])([A-Z])', r'\1_\2', new_col) #Handle consecutive uppercase letters
            new_col = new_col.lower()  # Convert to lowercase
            new_col = re.sub(r'[^a-z0-9_]', '', new_col)  # Remove remaining special characters
            new_columns.append(new_col)

        df.columns = new_columns
        logger.info("Converted DataFrame column names to lowercase, adding underscores before uppercase letters, and removed special characters.")
        return df
    except Exception as e:
        logger.error(f"Failed to convert DataFrame column names to SQL format: {e}")
        raise

# Function to load data from DataFrame into the SQLite database
def load_data_to_dw(connection: sqlite3.Connection, df: pd.DataFrame, table_name: str) -> None:
    """
    Load data from a DataFrame into the specified table in the SQLite database.
    Gracefully handles columns that do not exist in the table.

    Args:
        connection (sqlite3.Connection): SQLite connection object.
        df (pd.DataFrame): DataFrame containing the data to load.
        table_name (str): Name of the table to load data into.
    """
    try:
        cursor = connection.cursor()

        # Get the existing column names from the table
        cursor.execute(f"PRAGMA table_info({table_name})")
        existing_columns = [row[1] for row in cursor.fetchall()]

        # Identify columns to be filtered out
        columns_to_filter = list(set(df.columns) - set(existing_columns))

        # Filter the DataFrame to only include existing columns
        df_filtered = df[df.columns.intersection(existing_columns)]

        # Log the filtered columns
        if columns_to_filter:
            logger.info(f"Columns filtered out for table '{table_name}': {', '.join(columns_to_filter)}")

        # Load the filtered data into the table
        df_filtered.to_sql(table_name, connection, if_exists='append', index=False)
        logger.info(f"Loaded data into {table_name} table (ignoring non-existent columns)")

    except sqlite3.OperationalError as e:
        logger.error(f"Failed to load data into {table_name}: {e}")
        if "no such table" in str(e):
            logger.error(f"Table '{table_name}' does not exist.")
        raise
    except Exception as e:
        logger.error(f"An unexpected error occurred while loading data into {table_name}: {e}")
        raise
    
def csv_to_dw(file_path: str, connection: sqlite3.Connection, table_name: str, delete_first: bool = False) -> None:
    """
    Load CSV data into the specified table in the SQLite database.

    Args:
        file_path (str): Path to the CSV file.
        connection (sqlite3.Connection): SQLite connection object.
        table_name (str): Name of the table to load data into.
        delete_first (bool): Whether to delete existing records in the table before loading. Defaults to True.
    """
    df = load_csv(file_path)
    delete_existing_records(connection.cursor(), table_name, delete_first)
    convert_to_sql_format(df)
    load_data_to_dw(connection, df, table_name)

##################################################################
# Main function
##################################################################
if __name__ == "__main__":
    pass