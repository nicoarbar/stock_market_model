import yfinance as yf
#EJEMPLO PARA UN SOLO TICKER - LAS FUNCIONES DE YFINANCE
ticker = 'IDR.MC'
ticker1 = 'ENG.MC'

#datos de varios tickers
df = yf.download('{} {}'.format(ticker, ticker1), start="2017-01-01", end="2017-01-05")
print(df[['Close','Open']])
#df.to_csv('historic_stock_data_202001_202009/multiple_stock.csv')

#ticker_yf = yf.Ticker(ticker)

# get stock info
#for key, value in ticker_yf.info.items():
#	print(key, ':', value)

# get historical market data
#hist = ticker_yf.history(period="max")

# show actions (dividends, splits)
#print(ticker_yf.actions)

# show dividends
#print(ticker_yf.dividends)

# show splits
#ticker_yf.splits

# show financials
#print(ticker_yf.financials)
#print(ticker_yf.quarterly_financials)

# show major holders
#print(ticker_yf.major_holders)

# show institutional holders
#print(ticker_yf.institutional_holders)

# show balance sheet
#print(ticker_yf.balance_sheet)
#ticker_yf.quarterly_balance_sheet

# show cashflow
#print(ticker_yf.cashflow)
#ticker_yf.quarterly_cashflow

# show earnings
#print(ticker_yf.earnings)
#print(ticker_yf.quarterly_earnings)

# show sustainability
#print(ticker_yf.sustainability)

# show analysts recommendations
#print(ticker_yf.recommendations)

# show next event (earnings, etc)
#ticker_yf.calendar

# show ISIN code - *experimental*
# ISIN = International Securities Identification Number
#ticker_yf.isin

# show options expirations
#print(ticker_yf.options)

# get option chain for specific expiration
#opt = ticker_yf.option_chain('YYYY-MM-DD')
# data available via: opt.calls, opt.puts