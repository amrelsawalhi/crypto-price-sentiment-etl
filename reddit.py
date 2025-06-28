import praw
from datetime import datetime
import pandas as pd

# Define your Reddit API credentials
reddit = praw.Reddit(
    client_id="2pl9O2yZgNpt-ycBSZYwUw",          # Replace with your Client ID
    client_secret="D3Q5Yo66YA_lva1ZTTuCBLzKBcnt1Q",  # Replace with your Client Secret
    user_agent="crypto_tracker",         # Replace with a descriptive User Agent
)

# Function to fetch the count of "Bitcoin" mentions in the past 24 hours (for both posts and comments)
def fetch_bitcoin_mentions():
    subreddit = reddit.subreddit("all")  # Search across all subreddits
    keyword = "bitcoin"  # Case-insensitive search term for "Bitcoin"
    current_date = datetime.now().strftime('%Y-%m-%d')  # Get the current date in YYYY-MM-DD format

    # Count mentions in posts (submissions)
    post_count = 0
    for post in subreddit.search(keyword, time_filter='day', limit=10000):
        post_count += 1

    # Count mentions in comments (this can be slower)
    comment_count = 0
    for comment in subreddit.comments(limit=10000):
        if keyword in comment.body.lower():  # Check if the keyword is mentioned in the comment body
            comment_count += 1

    total_mentions = post_count + comment_count
    return {"date": current_date, "mentions": total_mentions}

# Example of integrating this into a DataFrame (ETL step)
if __name__ == "__main__":
    # Fetch today's mentions
    data = fetch_bitcoin_mentions()

    # Append data to a DataFrame (could be integrated with a database or file storage)
    try:
        df = pd.read_csv("bitcoin_mentions.csv")  # Read existing data
    except FileNotFoundError:
        # Create a new DataFrame if the file doesn't exist
        df = pd.DataFrame(columns=["date", "mentions"])

    # Append new data
    df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)

    # Save back to CSV
    df.to_csv("bitcoin_mentions.csv", index=False)

    print(f"Updated mentions data: {data}")
