from sqlalchemy import create_engine
import pandas as pd
import logging


def load_sql(url, dataframe, sql_table):
    """
    Load a Pandas DataFrame into:
    1. A csv file with the same name as the dataframe
    2. A PostgreSQL database table.

    Args:
        username (str): The username for the PostgreSQL database.
        password (str): The password for the PostgreSQL database.
        host (str): The host address of the PostgreSQL database.
        port (str): The port number of the PostgreSQL database.
        database (str): The name of the PostgreSQL database.
        dataframe (pandas.DataFrame): The DataFrame containing the data to be loaded.
        sql_table (str): The name of the SQL table where the data will be loaded.
    
    Note:
        The function uses SQLAlchemy's `to_sql()` method with the 'append' option for 
        existing tables.
    """

    logging.basicConfig(level=logging.INFO)

    # Saving the dataframe to CSV

    try:
        logging.info(f'Searching for "{sql_table}.csv"')
        df = pd.read_csv(f'{sql_table}.csv')  # Read existing data
        logging.info(f'"{sql_table}.csv" was found, appending the new data ....')
    
    except FileNotFoundError:
        logging.info(f'"{sql_table}.csv" was not found, creating a new file ....')
        # Create a new DataFrame if the file doesn't exist
        df = pd.DataFrame()
        
    df = pd.concat([df, dataframe], ignore_index=True)

    # Save back to CSV
    df.to_csv(f"{sql_table}.csv", index=False)
    print(f'{sql_table}.csv has been saved successfully')


    try:
        logging.info(f'Connecting to the database ....')
        engine = create_engine(url)

        logging.info(f'Adding {dataframe} to {sql_table} table in the database.....')
        dataframe.to_sql(sql_table, engine, if_exists='append', index=False)
        
        print(f'{sql_table} table loaded successfully. \nHere\'s a preview of its content... ')
        query = pd.read_sql(f"SELECT * FROM {sql_table}", engine)
        print(query.head())

    except Exception as e:
        logging.error(f"Error loading data into {sql_table}: {e}", exc_info=True)