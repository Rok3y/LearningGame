import yfinance as yf
import database as db
import scrape as sc 
import pandas as pd
import asyncio
import aiohttp
import click
import logging
from concurrent.futures import ThreadPoolExecutor
from threading import Thread
from queue import Queue
from datetime import datetime, timedelta

LOG_FORMAT = "[%(threadName)s %(module)-20s %(asctime)s %(levelname)s] %(message)s"
logging.basicConfig(level=logging.INFO,
                    format=LOG_FORMAT,
                    datefmt='%H:%M:%S')

process_queue = Queue()

ticker_processed_succesfully = []

# An example of using yFinance to get stock data
# https://algotrading101.com/learn/yfinance-guide/

def update_ticker_list():
    # Get all tickers
    tickers = db.get_tickers()
    if tickers is None:
        tickers = pd.Series([])
    
    logging.info(f"found {len(tickers)}")
    
    logging.info("Fetching tickers...")
    scraped_tickers = sc.get_all_tickers()
    new_tickers = scraped_tickers[~scraped_tickers.isin(tickers)]
    if len(new_tickers) == 0:
        logging.info("No new tickers found.")
        return
    
    db.add_tickers_symbol(new_tickers.to_dict())
    logging.info(f"Updated {len(new_tickers)} tickers.")
    
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

def get_db_and_scraped_data(tickers: list) -> tuple[dict, dict, dict]:
    '''
        Get current data from the database and scrape data from the internet
        :param ticker: str
        :return: tuple[dict, dict]
    '''
    for ticker in tickers:
        # Get data from the database
        company_dict = db.get_company_document(ticker)
        if company_dict is None or len(company_dict) == 0:
            company_dict = {
                'ticker': ticker,
                'info': {},
                'history': []
            }
        
        # Get data from the internet
        try:
            yf_ticker = yf.Ticker(ticker)
        except Exception as e:
            logging.error(f"Error fetching data for ticker {ticker}")
            logging.error(e)
            continue
            
        
        new_collection = yf_ticker.info
        
        # Check for changes in the history collection
        if company_dict['history'] is None or len(company_dict['history']) == 0:
            history_data_dict = yf_ticker.history(period="max", interval="1d").to_dict()
        else:
            # Get last date in the history collection and get new data from that date
            last_date = datetime.strptime(company_dict['history'][-1]['Date'], '%Y-%m-%d %H:%M:%S')
            last_date = last_date + timedelta(days=1) # increment by one day
            history_data_dict = yf_ticker.history(start=last_date.strftime('%Y-%m-%d'), interval="1d").to_dict()
            
        process_queue.put((company_dict, new_collection, history_data_dict))
        
    # Processed all tickers, send the end signal
    process_queue.put((None, None, None))
    
    #return company_dict, new_collection, history_data_dict

def update_or_init_company_collection(exclude_attrs: list = ['companyOfficers', 'longBusinessSummary']):
    
    while True:
        db_coll, new_coll, history_data = process_queue.get(timeout=15)
        if db_coll is None and new_coll is None and history_data is None:
            logging.info("End signal received, exiting...")
            process_queue.task_done()
            break
    
        # check if the dictionarys are about the same company
        if db_coll['ticker'] != new_coll['symbol']:
            logging.warning("The company dictionaries are not about the same company")
            return
        
        ticker = db_coll['ticker']
        logging.info(f"Updating company document ({ticker})...")
        current_date = datetime.now().strftime("%Y-%m-%d")
        

        # Check for changes in the info collection
        changes = 0 # to keep track of changes made to the collection
        for attr_name, attr_value in new_coll.items():
            # Exclude specified attributes
            if attr_name in exclude_attrs:
                continue
            
            # Check if the attribute already exists
            if attr_name in db_coll['info']:
                # Update existing attribute
                # Check if new attribute value is different from the current one
                if attr_value != db_coll['info'][attr_name]['Values'][-1]:
                    changes += 1
                    logging.debug(f"{attr_name}: old value {db_coll['info'][attr_name]["Values"][-1]} --> new value: {attr_value}")
                    db_coll['info'][attr_name]['Dates'].append(current_date)
                    db_coll['info'][attr_name]['Values'].append(attr_value)
            else:
                # Initialize new attribute
                changes += 1
                db_coll['info'][attr_name] = {
                    'Dates': [current_date],
                    'Values': [attr_value]
                }
                
        # Add history data to the collection
        history_data_list = convert_history_data_to_list(history_data)
        db_coll['history'].extend(history_data_list)        
        
        # Add or update collection in database
        if changes > 0:
            # Update current collection
            db.add_or_update_company_document(db_coll)
            logging.info(f"Changes made to company document ({ticker}) : {changes}")
            process_queue.task_done()
        
        logging.info(f"No changes made to company document ({ticker})")
        process_queue.task_done()

def update_or_init_collection_old(ticker: str, exclude_attrs: list = ['companyOfficers', 'longBusinessSummary']):
    '''
        Update or initialize a collection for a given ticker
        :param ticker: str
        :param exclude_attrs: list
        :return: dict
    '''
    logging.info(f"Updating company document ({ticker})...")
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    # Get current data (data from database and scraped data) and update db data with new data
    company_dict = db.get_company_document(ticker)
    yf_ticker = yf.Ticker(ticker)
    if yf_ticker is None:
        logging.warning(f"Ticker {ticker} not found in Yahoo Finance")
        return
    new_collection = yf_ticker.info
    if not len(new_collection.keys()) > 1:
        logging.warning(f"Ticker {ticker} does not have any data")
        return
    
    # Check if the collection exists
    if company_dict is None or len(company_dict) == 0:
        logging.debug(f'Company document ({ticker}) is empty, creating new document')
        company_dict = {
        'ticker': ticker,
        'info': {},
        'history': []
    }

    # Check for changes in the info collection
    for attr_name, attr_value in new_collection.items():
        # Exclude specified attributes
        if attr_name in exclude_attrs:
            continue
        
        # Check if the attribute already exists
        if attr_name in company_dict['info']:
            # Update existing attribute
            # Check if new attribute value is different from the current one
            if attr_value != company_dict['info'][attr_name]['Values'][-1]:
                logging.debug(f"{attr_name}: old value {company_dict['info'][attr_name]["Values"][-1]} --> new value: {attr_value}")
                company_dict['info'][attr_name]['Dates'].append(current_date)
                company_dict['info'][attr_name]['Values'].append(attr_value)
        else:
            # Initialize new attribute
            company_dict['info'][attr_name] = {
                'Dates': [current_date],
                'Values': [attr_value]
            }
    
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
            logging.info(f"History data for {ticker} is up to date.")
        
    # Check if history data is available
    if history_data_dict is not None and len(history_data_dict) > 0:
        # Add history data to the collection
        history_data_list = convert_history_data_to_list(history_data_dict)
        company_dict['history'].extend(history_data_list)
    
    # Add or update collection in database
    result = db.add_or_update_company_document(company_dict)
    # logging.info(f"Changes made to company document ({ticker}) : {changes}")
    if result.upserted_id is not None:
        print("Upserted ID:", result.upserted_id)
    else:
        logging.info(f"No changes made to company document ({ticker})")
        
    ticker_processed_succesfully.append(ticker)
    return company_dict
            


@click.command()
@click.option('--update-tickers', is_flag=True, help="Update tickers in database")
def main(update_tickers: bool):
    
    start_time = datetime.now()
    if update_tickers:
        update_ticker_list()
        
    # Get all tickers
    # tickers = db.get_tickers()
    tickers = sc.get_top_100_tickers() # [:10]
    
    ticker_counter = 0
    # Get ticker data from database and check for new data
    for ticker in tickers:        
        ticker_collection = update_or_init_collection_old(ticker)
        ticker_counter += 1
        logging.info(f"{ticker_counter}/{len(tickers)} Ticker: {ticker} done! ")
        
    ticker_failed = list(set(tickers) - set(ticker_processed_succesfully))
    logging.info(f"Failed to process tickers: {ticker_failed}")
    
    # with ThreadPoolExecutor(max_workers=32) as executor:
    #     executor.map(update_or_init_collection, tickers)
    
    # t1 = Thread(target=get_db_and_scraped_data, args=(tickers,))
    # t2 = Thread(target=update_or_init_company_collection)
    # t1.start()
    # t2.start()
    # t1.join()
    # t2.join()
    
    
    end_time = datetime.now()
    logging.info(f"Time taken: {end_time - start_time}s")
    
    logging.info("Done!")

if __name__ == '__main__':    
    main()
    
    