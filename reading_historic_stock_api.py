import yfinance as yf 
from naragon_stock_prediction_util_functions import Mongo_stock_metadata
import json

#vamos a descargar ficheros historicos de datos 
my_query = 'tickers_sp500'
#buscamos en mongo los tickers - para esta clase solo se llama con la base de datos y el nombre de la coleccion
mongo_tickers = Mongo_stock_metadata('stock_metadata', 'tickers_sectors')
tickers_list = mongo_tickers.coleccion.find()[0][my_query]


#Creamos en mongo otra colecion para la info de cada compañia - la coleccion sera 'tickers_info'
mongo_ticker_info = Mongo_stock_metadata('stock_metadata', 'tickers_info')

for ticker in tickers_list: 
	ticker_api = yf.Ticker(ticker)
	ticker_api_info = json.dumps(ticker_api.info)
	mongo_ticker_info.insert_in_mongodb(ticker_api_info)

print(tickers_list)
