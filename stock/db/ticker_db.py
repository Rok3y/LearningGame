import scrape as sc
import pandas as pd
import logging
import db.db_common as dbc

TICKER_COLLECTION = 'tickers'

def get_tickers() -> pd.Series:
    logging.info('Getting tickers from database.')
    client = dbc.get_db_client()
    db = client['stock']
    collection = db[TICKER_COLLECTION]
    
    # Retrieve ticker document
    tickers_doc = collection.find_one({})
        
    # Check if there is any data in the database
    if tickers_doc is None:
        logging.warning(f"Cannot find any {TICKER_COLLECTION} documents.")
        return None
    
    # Convert to pandas Series
    #return pd.Series([doc['symbol'] for doc in tickers_doc])
    return pd.Series(tickers_doc["tickers"])


def add_tickers_symbol(tickers: dict):
    logging.debug(f'Storing ticker symbols ({len(tickers)}) in database.')
    try:
        client = dbc.get_db_client()
        db = client['stock']
        collection = db[TICKER_COLLECTION]
        
        # Convert the tickers dictionary to a list of ticker symbols
        tickers_list = list(tickers.values())

        # Create a document with a list of tickers
        document = {TICKER_COLLECTION: tickers_list}        
        collection.insert_one(document)
    except Exception as e:
        logging.error(f'Error storing ticker ({len(tickers)}) document in database.')
        logging.error(e)
    
    logging.debug(f'Stored ({len(tickers)}) in database.')