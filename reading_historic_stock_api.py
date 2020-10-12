import yfinance as yf 
from naragon_stock_prediction_util_functions import Mongo_stock_metadata, get_tickers_list, get_historical_stock_data
import pandas as pd

ticker_col = 'tickers_ibex35'
ticker_sample = ['ENG.MC', 'IDR.MC'] #para testear la API dos tickers enagas e indra

#fechas de comienzo y fin
start = '2020-01-01'
end = '2020-09-30'
data_historic_dir = 'historic_stock_data_202001_202009' #directorio donde almaceno los datos dde cada ticker historicos

ticker_info = False
ticker_historic = True

if ticker_info:
	#leemos la coleccion con la informacion de los indicadores de los tickers
	mongo_ticker_info = Mongo_stock_metadata('stock_metadata', 'tickers_info')

	df = pd.DataFrame(mongo_ticker_info.coleccion.find())

	filter_sample = df['ticker_name'] == ticker_sample
	df_filter = df[filter_sample]
	print(df_filter[['ticker_name','website','shortName','beta']])

if ticker_historic:
	ticker_list = get_tickers_list(ticker_col)
	get_historical_stock_data(ticker_list, start, end, data_historic_dir)

