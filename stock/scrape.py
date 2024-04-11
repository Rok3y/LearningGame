import yahoo_fin.stock_info as si
import yfinance as yf
import pandas as pd
import asyncio
import aiohttp
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

def get_all_tickers() -> pd.Series:
    logging.info(f"Scraping all tickers...")
    dow_list = si.tickers_dow()
    #ftse100_list = si.tickers_ftse100() # error
    #ftse250_list = si.tickers_ftse250() # error
    ibovespa_list = si.tickers_ibovespa()
    nasdaq_list = si.tickers_nasdaq() # 4954
    nifty50_list = si.tickers_nifty50()
    niftybank_list = si.tickers_niftybank()
    other_list = si.tickers_other()
    sp500_list = si.tickers_sp500()

    # combine all lists and do not allow duplicates
    all_tickers = list(set(dow_list + nasdaq_list + nifty50_list + niftybank_list + other_list + sp500_list + ibovespa_list))
    logging.info(f"Scrapped {len(all_tickers)} tickers")
    
    # convert to pandas series
    all_tickers = pd.Series(all_tickers)

    return all_tickers

def get_top_100_tickers() -> pd.Series:
    return pd.Series([
    "MSFT", "AAPL", "NVDA", "2222.SR", "AMZN", "GOOG", "META", "BRK-B", "TSM", "LLY",
    "AVGO", "JPM", "V", "NVO", "TSLA", "WMT", "XOM", "MA", "MC.PA", "UNH",
    "005930.KS", "ASML", "JNJ", "TCEHY", "PG", "HD", "ORCL", "TM", "MRK", "COST",
    "CVX", "ABBV", "BAC", "CRM", "600519.SS", "NFLX", "AMD", "NESN.SW", "RMS.PA", "KO",
    "601857.SS", "1398.HK", "RELIANCE.NS", "IHC.AE", "OR.PA", "PEP", "SHEL", "SAP", "LIN", "TMO",
    "ADBE", "DIS", "ACN", "AZN", "601288.SS", "WFC", "CSCO", "NVS", "MCD", "ROG.SW",
    "QCOM", "ABT", "0941.HK", "CAT", "TMUS", "DHR", "BABA", "INTU", "VZ", "AMAT",
    "IBM", "TCS.NS", "TTE", "GE", "601988.SS", "INTC", "CMCSA", "AXP", "NOW", "601939.SS",
    "COP", "UBER", "HSBC", "TXN", "IDEXY", "PDD", "MS", "PFE", "BHP", "SIE.DE",
    "HDB", "UNP", "CDI.PA", "AIR.PA", "RY", "AMGN", "PRX.AS", "MU", "PM", "SPGI"
    ])
    

def get_stock_summary(ticker: str) -> pd.DataFrame:
    ''' 
    Fetch stock summary
    @param ticker: str
    @return: pd.DataFrame
    '''
    logging.debug(f"Scraping {ticker} summary...")
    yf_ticker = yf.Ticker(ticker)
    df_ticker = pd.DataFrame.from_dict(yf_ticker.info, orient='index')
    df_ticker.reset_index(inplace=True)
    df_ticker.columns = ['Attribute', 'Value']
    return df_ticker