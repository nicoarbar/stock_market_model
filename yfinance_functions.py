import yfinance as yf
#EJEMPLO PARA UN SOLO TICKER - LAS FUNCIONES DE YFINANCE
ticker = 'IDR.MC'

ticker_yf = yf.Ticker(ticker)

# get stock info
#ticker_yf.info

# get historical market data
#hist = ticker_yf.history(period="max")

# show actions (dividends, splits)
#print(ticker_yf.actions)

# show dividends
#ticker_yf.dividends

# show splits
#ticker_yf.splits

# show financials
#ticker_yf.financials
#ticker_yf.quarterly_financials

# show major holders
#ticker_yf.major_holders

# show institutional holders
#print(ticker_yf.institutional_holders)

# show balance sheet
#ticker_yf.balance_sheet
#ticker_yf.quarterly_balance_sheet

# show cashflow
#ticker_yf.cashflow
#ticker_yf.quarterly_cashflow

# show earnings
#print(ticker_yf.earnings)
print(ticker_yf.quarterly_earnings)

# show sustainability
#ticker_yf.sustainability

# show analysts recommendations
#ticker_yf.recommendations

# show next event (earnings, etc)
#ticker_yf.calendar

# show ISIN code - *experimental*
# ISIN = International Securities Identification Number
#ticker_yf.isin

# show options expirations
#ticker_yf.options

# get option chain for specific expiration
#opt = ticker_yf.option_chain('YYYY-MM-DD')
# data available via: opt.calls, opt.puts