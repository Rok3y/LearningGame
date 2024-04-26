import requests
import pandas as pd
import ftplib
import io
import re
import json
import datetime

def tickers_dow(include_company_data = False):
    
    '''Downloads list of currently traded tickers on the Dow'''

    site = "https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average"
    
    table = pd.read_html(site, attrs = {"id":"constituents"})[0]
    
    if include_company_data:
        return table

    dow_tickers = sorted(table['Symbol'].tolist())
    
    return dow_tickers    

def tickers_ftse100(include_company_data = False):
    
    '''Downloads a list of the tickers traded on the FTSE 100 index'''
    
    table = pd.read_html("https://en.wikipedia.org/wiki/FTSE_100_Index", attrs = {"id": "constituents"})[0]
    
    if include_company_data:
        return table
    
    return sorted(table.Ticker.tolist())

def tickers_ftse250(include_company_data = False):
    
    
    '''Downloads a list of the tickers traded on the FTSE 250 index'''
    
    table = pd.read_html("https://en.wikipedia.org/wiki/FTSE_250_Index", attrs = {"id": "constituents"})[0]
    
    #table.columns = ["Company", "Ticker"]
    
    if include_company_data:
        return table
    
    return sorted(table.Ticker.tolist())

def tickers_ibovespa(include_company_data = False):
    
    '''Downloads list of currently traded tickers on the Ibovespa, Brazil'''

    table = pd.read_html("https://pt.wikipedia.org/wiki/Lista_de_companhias_citadas_no_Ibovespa")[0]
    table.columns = ["Symbol", "Share", "Sector", "Type", "Site"]
    
    if include_company_data:
        return table
    
    ibovespa_tickers = sorted(table.Symbol.tolist())
    
    return ibovespa_tickers 

def tickers_nasdaq(include_company_data = False):
    
    '''Downloads list of tickers currently listed in the NASDAQ'''
    
    ftp = ftplib.FTP("ftp.nasdaqtrader.com")
    ftp.login()
    ftp.cwd("SymbolDirectory")
    
    r = io.BytesIO()
    ftp.retrbinary('RETR nasdaqlisted.txt', r.write)
    
    if include_company_data:
        r.seek(0)
        data = pd.read_csv(r, sep = "|")
        return data
    
    info = r.getvalue().decode()
    splits = info.split("|")
    
    
    tickers = [x for x in splits if "\r\n" in x]
    tickers = [x.split("\r\n")[1] for x in tickers if "NASDAQ" not in x != "\r\n"]
    tickers = [ticker for ticker in tickers if "File" not in ticker]    
    
    ftp.close()    

    return tickers

def tickers_nifty50(include_company_data = False, headers = {'User-agent': 'Mozilla/5.0'}):

    '''Downloads list of currently traded tickers on the NIFTY 50, India'''

    site = "https://finance.yahoo.com/quote/%5ENSEI/components?p=%5ENSEI"
    table = pd.read_html(requests.get(site, headers=headers).text)[0]
    
    if include_company_data:
        return table
    
    nifty50 = sorted(table['Symbol'].tolist())

    return nifty50

def tickers_niftybank():
    ''' Currently traded tickers on the NIFTY BANK, India '''
    
    niftybank = ['AXISBANK', 'KOTAKBANK', 'HDFCBANK', 'SBIN', 'BANKBARODA', 'INDUSINDBK', 'PNB', 'IDFCFIRSTB', 'ICICIBANK', 'RBLBANK', 'FEDERALBNK', 'BANDHANBNK']
    
    return niftybank

def tickers_other(include_company_data = False):
    '''Downloads list of tickers currently listed in the "otherlisted.txt"
       file on "ftp.nasdaqtrader.com" '''
    ftp = ftplib.FTP("ftp.nasdaqtrader.com")
    ftp.login()
    ftp.cwd("SymbolDirectory")
    
    r = io.BytesIO()
    ftp.retrbinary('RETR otherlisted.txt', r.write)
    
    if include_company_data:
        r.seek(0)
        data = pd.read_csv(r, sep = "|")
        return data
    
    info = r.getvalue().decode()
    splits = info.split("|")    
    
    tickers = [x for x in splits if "\r\n" in x]
    tickers = [x.split("\r\n")[1] for x in tickers]
    tickers = [ticker for ticker in tickers if "File" not in ticker]        
    
    ftp.close()    

    return tickers

def tickers_sp500(include_company_data = False):
    '''Downloads list of tickers currently listed in the S&P 500 '''
    # get list of all S&P 500 stocks
    sp500 = pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")[0]
    sp500["Symbol"] = sp500["Symbol"].str.replace(".", "-", regex=True)

    if include_company_data:
        return sp500

    sp_tickers = sp500.Symbol.tolist()
    sp_tickers = sorted(sp_tickers)
    
    return sp_tickers