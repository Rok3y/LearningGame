import yfinance as yf
import database as db
import scrape as sc 
import pandas as pd
import click
import logging
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

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
    
def convert_history_data_to_dict(history_data: dict):
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
    logging.info(f"Updating company document ({ticker})...")
    current_date = datetime.now().strftime("%Y-%m-%d")
    new_document = False
    
    # Get current data (data from database and scraped data) and update db data with new data
    company_dict = db.get_company_document(ticker)
    yf_ticker = yf.Ticker(ticker)
    new_collection = yf_ticker.info
        
    # simulate changes
    new_collection['marketCap'] = 2000000000000
    new_collection['forwardPE'] = 30
    new_collection['dividendYield'] = 0.01
    new_collection['regularMarketPrice'] = 150
    new_collection['regularMarketVolume'] = 50000000
    
    # Check if the collection exists
    if company_dict is None or len(company_dict) == 0:
        new_document = True
        logging.info(f'Company document ({ticker}) is empty, creating new document')
        company_dict = {
        'ticker': ticker,
        'info': {},
        'history': []
    }

    # Check for changes in the info collection
    changes = 0 # to keep track of changes made to the collection
    for attr_name, attr_value in new_collection.items():
        # Exclude specified attributes
        if attr_name in exclude_attrs:
            continue
        
        # Check if the attribute already exists
        if attr_name in company_dict['info']:
            # Update existing attribute
            # Check if new attribute value is different from the current one
            if attr_value != company_dict['info'][attr_name]['Values'][-1]:
                changes += 1
                logging.info(f"{attr_name}: old value {company_dict['info'][attr_name]["Values"][-1]} --> new value: {attr_value}")
                company_dict['info'][attr_name]['Dates'].append(current_date)
                company_dict['info'][attr_name]['Values'].append(attr_value)
        else:
            # Initialize new attribute
            changes += 1
            company_dict['info'][attr_name] = {
                'Dates': [current_date],
                'Values': [attr_value]
            }
    
    # Check for changes in the history collection
    if company_dict['history'] is None or len(company_dict['history']) == 0:
        history_data_dict = yf_ticker.history(period="max", interval="1d").to_dict()
    else:
        # Get last date in the history collection and get new data from that date
        last_date = datetime.strptime(company_dict['history'][-1]['Date'], '%Y-%m-%d %H:%M:%S')
        last_date = last_date + timedelta(days=1) # increment by one day
        history_data_dict = yf_ticker.history(start=last_date.strftime('%Y-%m-%d'), interval="1d").to_dict()
        
    # Add history data to the collection
    history_data_list = convert_history_data_to_dict(history_data_dict)
    company_dict['history'].extend(history_data_list)        
    
    # Update collection in database
    if new_document:
        # Add new collection
        db.add_company_document(company_dict)
        logging.info("Added new company document({ticker}) to the database")
        return company_dict
    elif changes > 0:
        # Update current collection
        db.update_company_document(company_dict)
        logging.info(f"Changes made to company document ({ticker}) : {changes}")
        return company_dict
    
    logging.info(f"No changes made to company document ({ticker})")
    return company_dict
            


@click.command()
@click.option('--update-tickers', is_flag=True, help="Update tickers in database")
def main(update_tickers: bool):
    
    if update_tickers:
        update_ticker_list()
        
    # Get all tickers
    # tickers = db.get_tickers()
    tickers = sc.get_top_100_tickers()[:1]
    
    ticker_counter = 0
    # Get ticker data from database and check for new data
    for ticker in tickers:        
        ticker_collection = update_or_init_collection(ticker)
        ticker_counter += 1
        print(f"{ticker_counter}/{len(tickers)} Ticker: {ticker} done! ")
        # Add updated stock data to database
    
    
    
    # Add stock summary to database
    
    print("Done!")

if __name__ == '__main__':    
    main()
    
    