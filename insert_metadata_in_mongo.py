#imports donde estan mis funciones 
from naragon_stock_prediction_util_functions import Mongo_stock_metadata, scrap_tickers, logger_for_my_stock_app
import yfinance as yf  #modulo de Yahoo Finance para interactuar con su API e ingestar datos 
import json #respuestas de la API vienen en json - hay que transformarlas a diccionarios de Python

logger = logger_for_my_stock_app()

#objeto que tiene ya el cliente en local host de MongoDB, base de datos 'stock_metadata' y coleccion 'tickers_sectors' 
mongo_tickers = Mongo_stock_metadata('stock_metadata', 'tickers_sectors')
key_for_tickers = 'tickers_sp500'
key_for_sectors = 'sectors_sp500'

#se comprueba primero es que hay datos insertados de los tickers
#mongo_tickers_with_data = mongo_tickers.read_one_from_mongodb()

#se pone este flag a True para activar la descarga de informacion de la API de los tickers en la coleccion 'tickers_info'
mongo_tickers_with_data = True

#Screpamos si no hay datos alamcenados de los tickers
if mongo_tickers_with_data == None:
	url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies' #web donde cojo los datos de los tickers
	tickers_sector = scrap_tickers(url)

	#almacenar tickers en mongoDB
	tickers_list = list(tickers_sector.keys())
	tickers_for_mongo = {'{}': tickers_list}.format(key_for_tickers)
	#sectores
	sectors_list = list(set(tickers_sector.values()))
	sectors_for_mongo = {'{}': sectors_list}.format(key_for_sectors)

	#insertamos
	mongo_tickers.insert_in_mongodb(tickers_for_mongo) #insertamos listado de tickers en la coleccion
	mongo_tickers.insert_in_mongodb(sectors_for_mongo) #insertamos listado de sectores en la coleccion

	#leemos que hay en mongo al logger
	logger.info('Coleccion en Mongo {}'.format(mongo_tickers.read_all_from_mongodb()[1]))


#almacenamos datos de Yahoo Finance de los tickers ya cuando se tienen los tickers
if mongo_tickers_with_data:
	tickers_list = mongo_tickers.coleccion.find()[0][key_for_tickers]
	logger.info('Lista de tickers: {}'.format(tickers_list))
	#Creamos en mongo otra colecion para la info de cada compañia - la coleccion sera 'tickers_info'
	mongo_ticker_info = Mongo_stock_metadata('stock_metadata', 'tickers_info')
	
	ticker_example = [tickers_list[20]]
	for ticker in ticker_example:
		logger.info('Ticker a procesar: {}'.format(ticker))
		ticker_api = yf.Ticker(ticker)
		ticker_api_info_str = json.dumps(ticker_api.info)
		ticker_api_info_dict = json.loads(ticker_api_info_str)
		#mongo_ticker_info.insert_in_mongodb(ticker_api_info_dict)
		print(type(ticker_api_info_dict))


