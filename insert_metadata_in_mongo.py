#imports donde estan mis funciones 
from naragon_stock_prediction_util_functions import *

logger = logger_for_my_stock_app()

#flag para leer el tipo de mercado, ibeex o sp500
sp500 = False
ibex35 = True

if sp500:
	#sp500
	url_scrap = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies' #web donde cojo los datos de los tickers
	ticker_col = 'tickers_sp500'
	n_ticks = 500
if ibex35:
	#ibex35
	url_scrap = 'https://en.wikipedia.org/wiki/IBEX_35' #web donde cojo los datos de los tickers
	ticker_col = 'tickers_ibex35'
	n_ticks = 35

#objeto que tiene ya el cliente en local host de MongoDB, base de datos 'stock_metadata' y coleccion 'tickers_sectors' 
mongo_tickers_list_object = Mongo_stock_metadata('stock_metadata', 'tickers_list')
#se comprueba primero es que hay datos insertados de los tickers
try:
	mongo_tickers_list_data = mongo_tickers_list_object.read_by_key_from_mongodb('ticker_market', ticker_col)
except:
	mongo_tickers_list_data = None

#Creamos en mongo otra colecion para la info de cada compañia - la coleccion sera 'tickers_info'
mongo_ticker_info_object = Mongo_stock_metadata('stock_metadata', 'tickers_info')
#se comprueba primero es que hay datos insertados de los tickers
mongo_tickers_info_count = mongo_ticker_info_object.count_elements_collection()

#Screpamos si no hay datos alamcenados de los tickers
if mongo_tickers_list_data == None:
	tickers_list = scrap_tickers(url_scrap, 0)
	#para los tickers del Ibex35 hay que añadirles el sufijo '.MC' que es como estan codificados en Yahoo Finance
	if ibex35:
		ibex_tickers = []
		for ticker in tickers_list:
			new_ticker = ticker + '.MC'
			ibex_tickers.append(new_ticker)
		tickers_list = ibex_tickers
	insert_ticker_metadata_in_mongo(mongo_tickers_list_object, ticker_col, tickers_list)


#almacenamos datos de Yahoo Finance de los tickers ya cuando se tienen los tickers - solo cuando no se tenga info de algun ticker
if mongo_tickers_info_count == 0:
	tickers_list = mongo_tickers_list_object.read_by_key_from_mongodb('ticker_market', ticker_col)['ticker_list']
	for ticker in tickers_list:
		try:
			insert_ticker_info_in_mongo(mongo_ticker_info_object, ticker)
		except:
			logger.info('El ticker {} no viene informado'.format(ticker))
			print(ticker)
	print(mongo_ticker_info_object.count_elements_collection(), 'tickers insertados en mongo')
