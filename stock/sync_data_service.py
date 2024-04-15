import yfinance as yf
import database as db
import scrape as sc 
import pandas as pd
from logging_config import logger
from datetime import datetime, timedelta

#logger = logging.getLogger('StocksLogger')
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

def update_or_init_collection(ticker: str, exclude_attrs: list = ['companyOfficers', 'longBusinessSummary']):
    '''
        Update or initialize a collection for a given ticker
        :param ticker: str
        :param exclude_attrs: list
        :return: dict
    '''
    logger.info(f"Updating company document ({ticker})...")
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    # Get current data (data from database and scraped data) and update db data with new data
    company_dict = db.get_company_document(ticker)
    
    # Scrape data and check if the ticker is valid
    try:
        yf_ticker = yf.Ticker(ticker)
        if yf_ticker is None:
            logger.warning(f"Ticker {ticker} not found in Yahoo Finance")
                
        if yf_ticker.info is None:
            logger.warning(f"Ticker {ticker} does not have any data")
    except Exception as e:
        logger.error(f"Error occurred while fetching data for {ticker}: {e}")
        return
    
    
    new_collection = yf_ticker.info
    if not len(new_collection.keys()) > 1:
        logger.warning(f"Ticker {ticker} does not have any data")
        return
    
    # Check if the collection exists
    if company_dict is None or len(company_dict) == 0:
        logger.debug(f'Company document ({ticker}) is empty, creating new document')
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
                logger.debug(f"{attr_name}: old value {company_dict['info'][attr_name]["Values"][-1]} --> new value: {attr_value}")
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
            logger.info(f"History data for {ticker} is up to date.")
        
    # Check if history data is available
    if history_data_dict is not None and len(history_data_dict) > 0:
        # Add history data to the collection
        history_data_list = convert_history_data_to_list(history_data_dict)
        company_dict['history'].extend(history_data_list)
    
    # Add or update collection in database
    result = db.add_or_update_company_document(company_dict)
    # logging.info(f"Changes made to company document ({ticker}) : {changes}")
    if result.upserted_id is not None:
        logger.info(f"Upserted ID: {result.upserted_id}")
    else:
        logger.info(f"No changes made to company document ({ticker})")
        
    ticker_processed_succesfully.append(ticker)
    return company_dict