import requests
import logging
from time import sleep
import praw
from datetime import datetime

def binance_api(url, max_retries=3, timeout=10):

    """
    Fetch all OHLCV data for a symbol from Binance since its listing date.

    Args:
        symbol (str): The trading pair symbol (default: BTCUSDT).
        interval (str): Candlestick interval (default: 1d for daily).
        start_date (str): Start date in 'YYYY-MM-DD' format (default: listing date).

    Returns:
        pd.DataFrame: A DataFrame containing timestamp, open, high, low, close, and volume.
    
    """
    
    logging.basicConfig(level=logging.INFO)

    retries = 0

    while retries < max_retries:
        try:
            logging.info(f"Attempting request to URL: {url}")
            
            response = requests.get(url, timeout=timeout)

            if response.status_code == 200:
                
                logging.info(f"Response status code: {response.status_code}")
                                
                response.raise_for_status()
                                
                logging.info("Data fetched successfully.")

            
            return response.json() 
            

        except requests.exceptions.Timeout:
            logging.warning(f'Timeout occurred for URL: {url}. Retrying ({retries + 1}/{max_retries}) ...')
            retries += 1
            sleep(2)


        except Exception as e:  
            logging.error(f"An error occurred: {e}")
            break 

    logging.error(f"Failed to fetch data from API after {max_retries} attempts.")
    return None

def fear_greed_index_api(url, max_retries=3, timeout=10):

    """
    Fetch data from an API endpoint and return the response as a JSON object.

    Args:
        url (str): The API endpoint URL from which to fetch data.
        max_retries (int): Maximum number of retries for timeout errors.
        timeout (int): Timeout for the API request in seconds.

    Returns:
        dict: The response from the API in JSON format
        None: If the request fails after retries or encounters an unrecoverable error.
    
    """
    
    logging.basicConfig(level=logging.INFO)

    retries = 0

    while retries < max_retries:
        try:
            logging.info(f"Attempting request to URL: {url}")

            response = requests.get(url, timeout=timeout)

            sleep(2)

            if response.status_code == 200:
                
                logging.info(f"Response status code: {response.status_code}")
                                
                response.raise_for_status()

                sleep(2)                

                logging.info("Data fetched successfully.")
           
            return  response.json()
            

        except requests.exceptions.Timeout:
            logging.warning(f'Timeout occurred for URL: {url}. Retrying ({retries + 1}/{max_retries}) ...')
            retries += 1
            sleep(2)


        except Exception as e:  
            logging.error(f"An error occurred: {e}")
            break 

    logging.error(f"Failed to fetch Fear And Greed data from API after {max_retries} attempts.")
    return None

def reddit_api(client_id, client_secret, user_agent):
    """
    Initializes and returns a Reddit API client using the provided credentials.

    Args:
        client_id (str): The client ID for your Reddit application.
        client_secret (str): The client secret for your Reddit application.
        user_agent (str): A string representing the user agent for the Reddit application, typically identifying the app or script making the requests.

    Returns:
        praw.Reddit: An authenticated Reddit API client that can be used to interact with Reddit's API.

    """
    reddit = praw.Reddit(
        client_id = client_id,         
        client_secret = client_secret,  
        user_agent = user_agent        
    )
    return reddit