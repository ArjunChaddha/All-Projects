import pandas as pd
import pandas_datareader as web
import datetime
from datetime import datetime

#Function takes in stock, startDate, and endDate and creates the CSV file for the given stock between the dates
def MakeCSVFileforAstock(stock, startDate, endDate):
    date_format = "%Y-%m-%d"
    start = datetime.strptime(startDate, date_format)
    end = datetime.strptime(endDate, date_format)
    df = web.DataReader(stock, 'yahoo', start, end)
    df.to_csv(stock+'.csv')

MakeCSVFileforAstock('TSLA','2020-10-26','2022-10-26')
MakeCSVFileforAstock('AMZN','2020-10-26','2022-10-26')

#all stocks except - 'ITC.NS and IOC.NS have been considered because it didn't have data from 2012.
#List of all stocks in NIFTY-50 as per 25th October 2022
# stocks = ['ADANIPORTS.NS', 'ASIANPAINT.NS', 'AXISBANK.NS', 'BAJFINANCE.NS', 'BAJAJFINSV.NS', 'BHARTIARTL.NS', 'BPCL.NS', 'BRITANNIA.NS', 'CIPLA.NS', 'COALINDIA.NS', 'DIVISLAB.NS', 'DRREDDY.NS', 'EICHERMOT.NS', 'GRASIM.NS', 'HCLTECH.NS', 'HDFC.NS', 'HDFCBANK.NS', 'HDFCLIFE.NS', 'HEROMOTOCO.NS', 'HINDALCO.NS', 'HINDUNILVR.NS', 'ICICIBANK.NS', 'INDUSINDBK.NS', 'INFY.NS', 'JSWSTEEL.NS', 'KOTAKBANK.NS', 'LT.NS', 'M&M.NS', 'MARUTI.NS', 'NESTLEIND.NS', 'NTPC.NS', 'ONGC.NS', 'POWERGRID.NS', 'RELIANCE.NS', 'SBILIFE.NS', 'SBIN.NS', 'TATACONSUM.NS', 'SUNPHARMA.NS', 'TATAMOTORS.NS', 'TATASTEEL.NS', 'TCS.NS', 'TECHM.NS', 'TITAN.NS', 'ULTRACEMCO.NS', 'UPL.NS', 'WIPRO.NS']
# print (len(stocks))

#Looping through all the stocks and generating CSV Files
# for stock in stocks:
#     MakeCSVFileforAstock(stock, '2012-01-01','2021-12-31')
#     print (stock)