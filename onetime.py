import requests
import pandas as pd
import time
from pipeline import load

from sqlalchemy import create_engine
import pandas as pd
import logging
from sqlalchemy.dialects.postgresql import insert


from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.dialects.postgresql import insert
import logging


def load_sql_bulk_upsert(url, dataframe, sql_table_name):
    """
    Load a Pandas DataFrame into a PostgreSQL database table with bulk upsert.

    Args:
        url (str): SQLAlchemy database URL.
        dataframe (pandas.DataFrame): The DataFrame containing the data to be loaded.
        sql_table_name (str): The name of the SQL table where the data will be loaded.
    """
    logging.basicConfig(level=logging.INFO)
    logging.info(f"Connecting to the database and preparing for bulk upsert into {sql_table_name}...")

    try:
        # Connect to the database and reflect the table
        engine = create_engine(url)
        metadata = MetaData(bind=engine)
        metadata.reflect()  # Reflects existing database tables
        sql_table = Table(sql_table_name, metadata, autoload_with=engine)

        # Bulk upsert using SQLAlchemy
        with engine.connect() as conn:
            stmt = insert(sql_table).values(dataframe.to_dict(orient='records'))
            upsert_stmt = stmt.on_conflict_do_update(
                index_elements=['timestamp'],  # Ensure 'timestamp' is defined as UNIQUE or PRIMARY KEY
                set_={
                    'open': stmt.excluded.open,
                    'high': stmt.excluded.high,
                    'low': stmt.excluded.low,
                    'close': stmt.excluded.close,
                    'volume': stmt.excluded.volume,
                },
            )
            conn.execute(upsert_stmt)
            logging.info(f"Bulk upsert into {sql_table_name} completed successfully.")

    except Exception as e:
        logging.error(f"Error during bulk upsert into {sql_table_name}: {e}", exc_info=True)




def fetch_binance_ohlcv(symbol="BTCUSDT", interval="1d", start_date="2017-08-17", limit=10):
    """
    Fetch all OHLCV data for a symbol from Binance since its listing date.

    Args:
        symbol (str): The trading pair symbol (default: BTCUSDT).
        interval (str): Candlestick interval (default: 1d for daily).
        start_date (str): Start date in 'YYYY-MM-DD' format (default: listing date).

    Returns:
        pd.DataFrame: A DataFrame containing timestamp, open, high, low, close, and volume.
    """
    url = "https://api.binance.com/api/v3/klines"
    start_time = int(pd.Timestamp(start_date).timestamp() * 1000)  # Convert to milliseconds
    all_data = []

    while True:
        params = {
            "symbol": symbol,
            "interval": interval,
            "limit": limit,
            "startTime": start_time,
        }
        response = requests.get(url, params=params)
        if response.status_code != 200:
            print(f"Error: {response.json()}")
            break

        data = response.json()
        if not data:
            break
        
        all_data.extend(data)

        # Update start_time to the last candle's close time + 1ms
        start_time = data[-1][6] + 1

        # Sleep to avoid rate limit issues
        time.sleep(0.1)

        # Stop if less than the limit of rows was returned (end of data)
        if len(data) < limit:
            break

    # Convert to DataFrame
    df = pd.DataFrame(all_data, columns=[
        'timestamp', 'open', 'high', 'low', 'close', 'volume',
        'close_time', 'quote_asset_volume', 'num_trades',
        'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
    ])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df = df[['timestamp', 'open', 'high', 'low', 'close', 'volume']].copy()

    # Convert numeric columns to floats
    df[['open', 'high', 'low', 'close', 'volume']] = df[['open', 'high', 'low', 'close', 'volume']].astype(float)
    return df

# Fetch data
bitcoin_data = fetch_binance_ohlcv(limit=10)
print(bitcoin_data.info())

# Save to CSV
bitcoin_data.to_csv("bitcoin_daily_ohlcv.csv", index=False)
print("Data saved to bitcoin_daily_ohlcv.csv")


db_url = 'postgresql://crypto_owner:C7KtqsLR9nFY@ep-mute-waterfall-a81wdisb.eastus2.azure.neon.tech/crypto?sslmode=require' #add the full url of your database
load_sql_bulk_upsert(url=db_url, dataframe= bitcoin_data, sql_table_name= 'bitcoin_ohlc') #loading bitcoin_table


