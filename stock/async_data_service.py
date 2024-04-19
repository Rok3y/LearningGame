import yfinance as yf
import stock.db.database as db
import stock.src.scrape as sc 
import pandas as pd
import logging
from queue import Queue
from datetime import datetime, timedelta
from time import sleep
logger = logging.getLogger('StocksLogger')


########################################################################################
# Now when doing bulk inserts it can take a lot of time when approaching 10000 documents
# In this case we could utilise process queue to separate the scrape and db operations
########################################################################################

process_db_queue = Queue()
process_dl_queue = Queue()
ticker_processed_succesfully = []

def convert_history_data_to_list(history_data: dict):
    history_data_list = []
    for date in history_data['Open']:
    # Build the dictionary for each date
        data_entry = {
            "Date": date.strftime('%Y-%m-%d %H:%M:%S'),
            "Open": history_data['Open'].get(date),
            "High": history_data['High'].get(date),
            "Low": history_data['Low'].get(date),
            "Close": history_data['Close'].get(date),
            "Volume": history_data['Volume'].get(date),
            "Dividends": history_data['Dividends'].get(date),
            "Stock Splits": history_data['Stock Splits'].get(date)
        }
        history_data_list.append(data_entry)
    return history_data_list


def get_db_and_scraped_data_old(ticker) -> tuple[dict, dict, dict]:
    '''
        Get current data from the database and scrape data from the internet
        :param ticker: str
        :return: tuple[dict, dict]
    '''
    #or ticker in tickers:
    # Get data from the database
    company_dict = db.get_company_document(ticker)
    # Check if the collection exists
    if company_dict is None or len(company_dict) == 0:
        logger.debug(f'Company document ({ticker}) is empty, creating new document')
        company_dict = {
        'ticker': ticker,
        'info': {},
        'history': []
    }
    
    # Get data from the internet
    yf_ticker = yf.Ticker(ticker)
    if yf_ticker is None:
        logger.warning(f"Ticker {ticker} not found in Yahoo Finance")
        return None, None, None
    new_collection = yf_ticker.info
    if not len(new_collection.keys()) > 1:
        logger.warning(f"Ticker {ticker} does not have any data")
        return None, None, None
                
    # Check for changes in the history collection
    history_data_dict = None
    if company_dict['history'] is None or len(company_dict['history']) == 0:
        history_data_dict = yf_ticker.history(period="max", interval="1d").to_dict()
    else:
        # Get last date in the history collection and get new data from that date
        last_date = datetime.strptime(company_dict['history'][-1]['Date'], '%Y-%m-%d %H:%M:%S')
        last_date = last_date + timedelta(days=1) # increment by one day
        if last_date.date() <= datetime.now().date():
            history_data_dict = yf_ticker.history(start=last_date.strftime('%Y-%m-%d'), interval="1d").to_dict()
        else:
            logger.info(f"History data for {ticker} is up to date.")
            
        # process_db_queue.put((company_dict, new_collection, history_data_dict))
        
    # Processed all tickers, send the end signal
    # process_db_queue.put((None, None, None))
    
    return company_dict, new_collection, history_data_dict
    
def get_db_and_scraped_data():
    '''
        Get current data from the database and scrape data from the internet
        :param ticker: str
        :return: tuple[dict, dict]
    '''
    #for ticker in tickers:
    while not process_dl_queue.empty():
        try:
            ticker = process_dl_queue.get(block=False)        
            # Get data from the database
            company_dict = db.get_company_document(ticker)
            # Check if the collection exists
            if company_dict is None or len(company_dict) == 0:
                logger.debug(f'Company document ({ticker}) is empty, creating new document')
                company_dict = {
                'ticker': ticker,
                'info': {},
                'history': []
            }
            
            # Get data from the internet
            yf_ticker = yf.Ticker(ticker)
            if yf_ticker is None:
                logger.warning(f"Ticker {ticker} not found in Yahoo Finance")
                process_dl_queue.task_done()
                continue
            new_collection = yf_ticker.info
            if not len(new_collection.keys()) > 1:
                logger.warning(f"Ticker {ticker} does not have any data")
                process_dl_queue.task_done()
                continue
                        
            # Check for changes in the history collection
            history_data_dict = None
            if company_dict['history'] is None or len(company_dict['history']) == 0:
                history_data_dict = yf_ticker.history(period="max", interval="1d").to_dict()
            else:
                # Get last date in the history collection and get new data from that date
                last_date = datetime.strptime(company_dict['history'][-1]['Date'], '%Y-%m-%d %H:%M:%S')
                last_date = last_date + timedelta(days=1) # increment by one day
                if last_date.date() <= datetime.now().date():
                    history_data_dict = yf_ticker.history(start=last_date.strftime('%Y-%m-%d'), interval="1d").to_dict()
                else:
                    logger.info(f"History data for {ticker} is up to date.")
                
            process_db_queue.put((company_dict, new_collection, history_data_dict))
            process_dl_queue.task_done()
        except Queue.Empty:
            logger.info("Download queue empty")

def update_or_init_company_collection(exclude_attrs: list = ['companyOfficers', 'longBusinessSummary']):
    
    while True:
        if process_db_queue.empty():
            logger.info("Queue is empty, waiting for data...")
            # sleep for 1 seconds
            sleep(1)
            continue
        db_coll, new_coll, history_data = process_db_queue.get()
        if db_coll is None and new_coll is None and history_data is None:
            logger.info("End signal received, exiting...")
            process_db_queue.task_done()
            break
    
        # check if the dictionarys are about the same company
        if db_coll['ticker'] != new_coll['symbol']:
            logger.warning("The company dictionaries are not about the same company")
            process_db_queue.task_done()
            continue
        
        ticker = db_coll['ticker']
        logger.info(f"Updating company document ({ticker})...")
        current_date = datetime.now().strftime("%Y-%m-%d")

        # Check for changes in the info collection
        for attr_name, attr_value in new_coll.items():
            # Exclude specified attributes
            if attr_name in exclude_attrs:
                continue
            
            # Check if the attribute already exists
            if attr_name in db_coll['info']:
                # Update existing attribute
                # Check if new attribute value is different from the current one
                if attr_value != db_coll['info'][attr_name]['Values'][-1]:
                    logger.debug(f"{attr_name}: old value {db_coll['info'][attr_name]["Values"][-1]} --> new value: {attr_value}")
                    db_coll['info'][attr_name]['Dates'].append(current_date)
                    db_coll['info'][attr_name]['Values'].append(attr_value)
            else:
                # Initialize new attribute
                db_coll['info'][attr_name] = {
                    'Dates': [current_date],
                    'Values': [attr_value]
                }
                
        # Add history data to the collection
        if history_data is not None and len(history_data) > 0:
            history_data_list = convert_history_data_to_list(history_data)
            db_coll['history'].extend(history_data_list)
        
        # Add or update collection in database
        result = db.add_or_update_company_document(db_coll)
        if result.upserted_id is not None:
            logger.info(f"Updated company document ({ticker})")
        else:
            logger.info(f"No changes made to company document ({ticker})")
            
        ticker_processed_succesfully.append(ticker)
        
        logger.info(f"End for ({ticker})")
        process_db_queue.task_done()
    
    logger.info("Thread finished")