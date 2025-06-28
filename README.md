Cryptocurrency Analytics ETL Project 🚀
A data engineering project that extracts, transforms, and loads cryptocurrency data, including price trends, sentiment analysis, and market behavior, into a structured database for analysis and insights.

🌟 Features
Cryptocurrency Price ETL: Automates data extraction from CoinGecko and updates it into a database.
Social Media Sentiment Tracking: Monitors daily mentions of "Bitcoin" on Reddit and Twitter.
Fear and Greed Index Integration: Tracks market sentiment over time using the Fear and Greed Index API.

🛠️ Technologies Used
Python: Core programming language.
APIs:
    CoinGecko for cryptocurrency price data.
    Reddit and Twitter APIs for sentiment tracking.
    Fear and Greed Index for market behavior analysis.
Pandas: Data manipulation and analysis.
PostgreSQL: Data storage and querying.
Airflow (will be added soon): For workflow automation.

📂 Project Structure

Copy code
├── pipeline/
│   ├── __init__.py     # Initializes the pipeline module
│   ├── extract.py      # Contains functions to extract data from APIs (Coingecko, Reddit, Fear & Greed Index, etc.)
│   ├── transform.py    # Data cleaning and transformation logic 
│   ├── load.py         # Functions to load processed data into a database
│
├── script.py           # Main script to run the ETL pipeline
└── README.md           # Project overview


📊 How It Works

Data Extraction:

Fetches cryptocurrency prices and market sentiment data from APIs.
Tracks social media activity around Bitcoin using Reddit and Twitter.
Data Transformation:

Converts raw data into structured formats.
Applies necessary conversions (e.g., converting timestamps, normalizing text).
Data Loading:

Stores the processed data into a PostgreSQL database.
Creates tables for easy querying and analysis.


🚀 Getting Started
Prerequisites
    Python 3.8+
    PostgreSQL
    API Keys for:
    Reddit
    Twitter (optional)
    Installation
    Clone this repository:
    bash
    Copy code
    git clone https://github.com/yourusername/crypto-etl.git
    cd crypto-etl

Install dependencies:
    bash
    Copy code
    pip install -r requirements.txt
    Set up .env file for API credentials:
    env
    Copy code
    REDDIT_CLIENT_ID=your_id
    REDDIT_SECRET=your_secret
    COINGECKO_API=your_key

📈 Sample Output
    Price Trends Table:

    Date	Bitcoin Price (USD)
    2024-11-23	$16,542
    2024-11-24	$16,732
    Sentiment Analysis:

    Date	Mentions	Sentiment Score
    2024-11-23	120	0.87
    2024-11-24	142	0.91


🛡️ License
    This project is licensed under the MIT License.

🤝 Contributing
    Contributions, issues, and feature requests are welcome! Feel free to check the issues page.

📬 Contact
    Email: your-email@example.com
    GitHub: yourusername
