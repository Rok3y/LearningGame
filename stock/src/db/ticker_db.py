import pandas as pd
from src.logging_config import logger
import src.db.db_common as dbc


def get_tickers() -> pd.Series:
    logger.info('Getting tickers from database.')
    collection = dbc.MongoDBManager.get_ticker_collection()
    
    # Retrieve ticker document
    tickers_doc = collection.find_one({})
        
    # Check if there is any data in the database
    if tickers_doc is None:
        logger.warning(f"Cannot find any {dbc.TICKER_COLLECTION} documents.")
        return None
    
    # Convert to pandas Series
    #return pd.Series([doc['symbol'] for doc in tickers_doc])
    return pd.Series(tickers_doc["tickers"])


def add_tickers_symbol(tickers: list):
    logger.debug(f'Storing ticker symbols ({len(tickers)}) in database.')
    try:
        collection = dbc.MongoDBManager.get_ticker_collection()
        
        # Convert the tickers dictionary to a list of ticker symbols
        #tickers_list = list(tickers.values())

        # Create a document with a list of tickers
        document = {dbc.TICKER_COLLECTION: tickers}
        collection.insert_one(document)
    except Exception as e:
        logger.error(f'Error storing ticker ({len(tickers)}) document in database.')
        logger.error(e)
    
    logger.debug(f'Stored ({len(tickers)}) in database.')