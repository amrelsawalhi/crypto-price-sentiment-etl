from pipeline import extract, load, transform


# Bitcoin_OHLC
api_url = "https://api.coingecko.com/api/v3/coins/bitcoin/ohlc?vs_currency=usd&days=1&precision=2"

headers = {
    "accept": "application/json",
    "x-cg-demo-api-key": "CG-Vdg9LFchH3WwG57dNWvMGuYM"
}

bitcoin = extract.coingecko_api(api_url, headers)

bitcoin = transform.coingecko(bitcoin)

# Fear_Greed_Index

fgi_url= 'https://api.alternative.me/fng/?limit=5000'

fgi = extract.fear_greed_index_api(fgi_url)

fgi = transform.fear_greed_index(fgi)

# Reddit mentions of bitcoin
client_id="2pl9O2yZgNpt-ycBSZYwUw"                  # Replace with your Client ID
client_secret="D3Q5Yo66YA_lva1ZTTuCBLzKBcnt1Q"      # Replace with your Client Secret
user_agent="crypto_tracker"                         # Replace with a descriptive User Agent

praw_reddit = extract.reddit_api(client_id= client_id, client_secret= client_secret, user_agent= user_agent)
reddit_mentions = transform.reddit(praw_reddit, subreddit='all', keyword='bitcoin')

# Loading all tables into csv files and the database
db_url = 'postgresql://crypto_owner:C7KtqsLR9nFY@ep-mute-waterfall-a81wdisb.eastus2.azure.neon.tech/crypto?sslmode=require' #add the full url of your database

# add the name of the table in the database, if it doesn't exist it will create a new table. 
# Note: it will use the same name for the csv file
bitcoin_table = 'bitcoin_ohlc' 
fgi_table = 'fear_greed_index'
reddit_table= 'reddit_mentions'

load.load_sql(url=db_url, dataframe= bitcoin, sql_table= bitcoin_table) #loading bitcoin_table
load.load_sql(url=db_url, dataframe= fgi, sql_table= fgi_table) #loading fgi_table
load.load_sql(url=db_url, dataframe= reddit_mentions, sql_table= reddit_table) #loading reddit_table