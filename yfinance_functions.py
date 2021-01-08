import yfinance as yf
#EJEMPLO PARA UN SOLO TICKER - LAS FUNCIONES DE YFINANCE
ticker = 'IDR.MC'
ticker1 = 'ENG.MC'
ticker = 'DDOG'
empresa = 'DataDog'

#datos de varios tickers
df = yf.download('{} {}'.format(ticker, ticker1), start="2019-01-01", end="2019-01-05")
#print(df[['Close','Open']])
df.to_csv('historic_stock_data_202001_202009/multiple_stock.csv')

ticker_yf = yf.Ticker(ticker)
print('ticker: {}'.format(ticker), 'empresa: {}'.format(empresa))

# get stock info
#for key, value in ticker_yf.info.items():
#	print(key, ':', value)

# get historical market data
#hist = ticker_yf.history(period="max")

# show actions (dividends, splits)
print('acciones: ', ticker_yf.actions)

# show dividends
print('dividendos: ', ticker_yf.dividends)

# show splits
print('splits: ',ticker_yf.splits)

# show financials
print('datos financieros: ',ticker_yf.financials)
print('datos financieros cuatrimestral: ', ticker_yf.quarterly_financials)

# show major holders
print('accionistas mayores: ', ticker_yf.major_holders)

# show institutional holders
print('accionistas institucionales: ', ticker_yf.institutional_holders)

# show balance sheet
print('balance: ', ticker_yf.balance_sheet)
print('balance cuatrimestral', ticker_yf.quarterly_balance_sheet)

# show cashflow
print('flujo de caja: ', ticker_yf.cashflow)
print('flujo de caja cuatrimestral: ', ticker_yf.quarterly_cashflow)

# show earnings
print('beneficios: ', ticker_yf.earnings)
print('beneficios cuatrimestrales', ticker_yf.quarterly_earnings)

# show sustainability
print('sostenibilidad: ', ticker_yf.sustainability)

# show analysts recommendations
print('recomendaciones: ', ticker_yf.recommendations)

# show next event (earnings, etc)
print('calendario: ', ticker_yf.calendar)

# show ISIN code - *experimental*
# ISIN = International Securities Identification Number
print('codigo ISIN: ', ticker_yf.isin)


# get option chain for specific expiration
#data available via: opt.calls, opt.puts
try:
	# show options expirations
	print('opciones: ', ticker_yf.options)
	opt = ticker_yf.option_chain('2020-01-03')
	print('opciones del dia de expiracion : ', opt)
except:
	pass 
