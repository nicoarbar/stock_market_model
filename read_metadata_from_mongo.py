#script para leer y hacer analitica en MongoDB
from naragon_stock_prediction_util_functions import Mongo_stock_metadata

#modificar flags para realizar operaciones de lecutra o borrado de lo que se quiera
delete_collections = False
read_tickers = False
read_info = True
count_elements = True
read_specific_ticker = 'IDR.MC'

#objetos que seran base de datos y colecciones de MongoDB de mi app
mongo_tickers_list = Mongo_stock_metadata('stock_metadata', 'tickers_list')
mongo_ticker_info = Mongo_stock_metadata('stock_metadata', 'tickers_info')

#ELIMINAR COLECCIONES SI FUESE NECESARIO
if delete_collections:
	mongo_tickers_list.coleccion.drop()
	mongo_ticker_info.coleccion.drop()
	print('Se han borrado las colecciones')

if read_tickers:
	#se COLECCION DE TICKERS
	mongo_tickers_list_all = mongo_tickers_list.read_all_from_mongodb()
	for doc in mongo_tickers_list_all:
		print(doc['ticker_market'], ':', doc['ticker_list'])

if read_info:
	#se lee INFORMACION DE CADA TICKER
	mongo_tickers_info_all = mongo_ticker_info.read_all_from_mongodb()
	for doc in mongo_tickers_info_all:
		print(doc['ticker_name'])

if count_elements:
	print('n info de tickers', mongo_ticker_info.count_elements_collection())
	print('n tickers lists', mongo_tickers_list.count_elements_collection())

if read_specific_ticker:
	specific_ticker_info = mongo_ticker_info.read_by_key_from_mongodb('ticker_name', read_specific_ticker)
	for key, value in specific_ticker_info.items():
		print(key, ':', value)
