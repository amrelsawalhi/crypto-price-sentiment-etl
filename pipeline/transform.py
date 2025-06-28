from sqlalchemy import create_engine
import pandas as pd
import logging
from time import sleep
from datetime import datetime
from textblob import TextBlob

logging.basicConfig(level=logging.INFO)

def coingecko(response):
    """
    Transform a JSON response into a Pandas DataFrame with proper column names and time format.

    Args:
        response (list or dict): The raw JSON response.

    Returns:
        pandas.DataFrame: A transformed DataFrame with the columns 'date', 'open', 'high', 'low', and 'close',
                           and a properly formatted 'date' column.
    
    Note:
        The 'date' column is converted to the 'YYYY-MM-DD' format to be compatible with PostgreSQL date type.
    """
   
    logging.info("Starting data transformation for coingecko")

    sleep(2)

    try:
        logging.info('Transforming data into a dataframe...')
        df = pd.DataFrame(response)

        df.columns=['timestamp', 'open', 'high', 'low', 'close']

        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms', utc=True, origin='unix')

        logging.info("Coingecko's Data transformation completed successfully and here's a preview...")
        print(df.head())

        return df
    

    except Exception as e:
        logging.error(f'Error: {e}')
        raise

def fear_greed_index(data):

    

    logging.info("Starting data transformation for fear and greed index")
    
    sleep(2)

    try:
        data_dict = data.get("data", [])

        df = pd.DataFrame(data_dict)

        df['timestamp'] = pd.to_numeric(df['timestamp'], errors='coerce')  # Ensure it's numeric
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')  # Convert to datetime
        df = df.drop('time_until_update', axis=1)
        
        logging.info("Fear And Greed Index table is now ready to be loaded, and here's a preview ...")
        print(df.head())

        return df
    
    except Exception as e:
        logging.error(f'Error: {e}')
        raise

def analyze_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity, blob.sentiment.subjectivity


def reddit(praw_reddit, subreddit, keyword):
    """
    Analyzes Reddit data for keyword mentions and sentiment within the past 24 hours.

    Args:
        praw_reddit (praw.Reddit): Authenticated Reddit client.
        subreddit (str): Subreddit to search.
        keyword (str): Keyword to look for.

    Returns:
        pd.DataFrame: A DataFrame containing the following columns:
            - timestamp: The date when the data was collected (YYYY-MM-DD format).
            - mentions: The total number of posts and comments mentioning the keyword.
            - avg_polarity: The average sentiment polarity of the posts and comments.
            - avg_subjectivity: The average subjectivity of the posts and comments.
    """
    try:
        subreddit = praw_reddit.subreddit(subreddit)
        current_date = datetime.now().strftime('%Y-%m-%d')
        
        total_mentions = 0
        total_polarity = 0
        total_subjectivity = 0

        # Process posts
        for post in subreddit.search(keyword, time_filter='day', limit=1000):
            total_mentions += 1
            polarity, subjectivity = analyze_sentiment(post.title)
            total_polarity += polarity
            total_subjectivity += subjectivity

        # Process comments
        for comment in subreddit.comments(limit=1000):
            if keyword.lower() in comment.body.lower():
                total_mentions += 1
                polarity, subjectivity = analyze_sentiment(comment.body)
                total_polarity += polarity
                total_subjectivity += subjectivity

        
        avg_polarity = total_polarity / total_mentions if total_mentions > 0 else 0 # added the if condition to avoid devision by zero
        avg_subjectivity = total_subjectivity / total_mentions if total_mentions > 0 else 0 # added the if condition to avoid devision by zero

        # Create DataFrame
        reddit_df = pd.DataFrame({
            "timestamp": [current_date],
            "mentions": [total_mentions],
            "avg_polarity": [round(avg_polarity, 5)],
            "avg_subjectivity": [round(avg_subjectivity, 5)],
        })

        return reddit_df

    except Exception as e:
        logging.error(f"Error during Reddit data processing: {e}", exc_info=True)
        raise