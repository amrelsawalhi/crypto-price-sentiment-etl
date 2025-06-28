# 🪙 Crypto Price & Sentiment ETL Pipeline

This project extracts, transforms, and loads real-time Bitcoin price data alongside sentiment signals from social media. It combines market data with Reddit-based discourse to explore correlations, patterns, and potential trading signals.

## 🚀 Features

- 📈 Real-time OHLC price data
- 💬 Reddit-based sentiment scraping
- 🧠 TextBlob sentiment scoring
- 📊 Technical indicators (MA, RSI)
- 🔄 Modular ETL design (Extract, Transform, Load)
- 💾 Output to CSV/database-ready format

## 🗂️ Project Structure

```
crypto-price-sentiment-etl/
├── pipeline/
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
├── script.py
├── reddit.py
├── MA-RSI.py
├── bitcoin_ohlc.csv
├── bitcoin_mentions.csv
├── requirements.txt
└── README.md
```

## 🧪 How to Run

```bash
pip install -r requirements.txt
python script.py
```

## 💡 Use Cases

- Backtesting sentiment-based signals
- Analyzing social vs market movement correlations
- Input for ML-based financial models

## 📌 Future Work

- Add Twitter & Google Trends sentiment
- Streamlit dashboard
- SQLite/PostgreSQL backend
- Enhanced NLP with Vader or transformers

## 📜 License

MIT License

## 👤 Author

**Amr El Sawalhi**  
[GitHub](https://github.com/amrelsawalhi)
