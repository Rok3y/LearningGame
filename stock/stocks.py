import yfinance as yf
import database as db
import scrape as sc 
import pandas as pd
import click

# An example of using yFinance to get stock data
# https://algotrading101.com/learn/yfinance-guide/

@click.command()
@click.option('--update', is_flag=True, help="Update tickers in database")
def main(update):
    # Get all tickers
    tickers = db.get_tickers()
    print(f"found {len(tickers)}")
    
    if update:
        print("Updating tickers...")
        tickers = sc.get_all_tickers()
        db.update_tickers(tickers)
        print(f"Updated {len(tickers)} tickers.")
    
    print("Getting stock data...")
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        print(stock.info)
    
    print("Done!")


if __name__ == '__main__':    
    # Get all tickers
    # tickers = db.get_tickers()
    
    # Get multiple tickers example
    tickers_list = ["aapl", "goog", "amzn", "BAC", "BA"]
    tickers_data = {}
    
    for ticker in tickers_list:
        stock = yf.Ticker(ticker)
        
        # convert info() output from dictionary to dataframe
        temp = pd.DataFrame.from_dict(stock.info, orient='index')
        temp.reset_index(inplace=True)
        temp.columns = ['Attribute', 'Value']
        
        # add (ticker, dataframe) to main dictionary
        tickers_data[ticker] = temp
        
    combined_data = pd.concat(tickers_data)
    combined_data = combined_data.reset_index()
    
    del combined_data['level_1'] # clean up unnecessary column
    combined_data.columns = ['Ticker', 'Attribute', 'Value'] # rename columns
    # print(combined_data)
    
    empoyees = combined_data[combined_data['Attribute'] == 'fullTimeEmployees'].reset_index()
    del empoyees['index']
    
    employees = empoyees.sort_values(by='Value', ascending=False)
    print(empoyees)
    
    # Market cap example
    aapl = yf.Ticker("AAPL")
    aapl_historical = aapl.history(period="max", interval="1wk")
    print(aapl_historical)