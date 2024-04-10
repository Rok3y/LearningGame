import pymongo
import scrape as sc
import pandas as pd


def get_db_client(conn_str: str = 'mongodb://localhost:27017/'):
    return pymongo.MongoClient(conn_str)

def get_tickers() -> pd.Series:
    client = get_db_client()
    db = client['stock']
    collection = db['tickers']
    
    # Retrieve all documents
    tickers_cursor = collection.find({})
    
    # Optional: Count documents without converting cursor to list (efficient for large collections)
    tickers_count = collection.count_documents({})
    
    # Check if there is any data in the database
    if tickers_count == 0:
        print("No tickers found in database, scraping from Yahoo Finance...")
        tickers = sc.get_all_tickers()
        # save to database
        collection.insert_many([{'symbol': ticker} for ticker in tickers])
        print(f"Inserted {len(tickers)} tickers into database.")
        return tickers
    else:
        print(f"Found {tickers_count} documents.")
    
    # Convert to pandas Series
    return pd.Series([doc['symbol'] for doc in tickers_cursor])

def get_stocks() -> pd.DataFrame:
    client = get_db_client()
    db = client['stock']
    collection = db['stocks']
    
    # Retrieve all documents
    stocks_cursor = collection.find({})
    
    # Optional: Count documents without converting cursor to list (efficient for large collections)
    stocks_count = collection.count_documents({})
    
    # Check if there is any data in the database
    if stocks_count == 0:
        print("No stocks found in database, scraping from Yahoo Finance...")
        tickers = sc.get_top_100_tickers()
        stocks = sc.get_all_stocks(tickers)
        # save to database
        collection.insert_many(stocks)
        print(f"Inserted {len(stocks)} stocks into database.")
        return pd.DataFrame(stocks)
    else:
        print(f"Found {stocks_count} documents.")
    
    # Convert to pandas DataFrame
    return pd.DataFrame(list(stocks_cursor))

def get_stock(ticker: str):
    client = get_db_client()
    db = client['stock']
    collection = db['stocks']
    
    # Retrieve all documents
    stock = collection.find_one
    