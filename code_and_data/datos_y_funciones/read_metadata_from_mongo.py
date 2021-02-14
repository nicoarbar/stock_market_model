#script para leer y hacer analitica en MongoDB
from naragon_stock_prediction_util_functions import Mongo_stock_metadata
import yfinance as yf

#modificar flags para realizar operaciones de lecutra o borrado de lo que se quiera
delete_collections = False
read_tickers = False
read_info = False
count_elements = False
read_specific_ticker = 'TEF.MC'
read_specific_ticker = False
read_scores = True
read_new_data_yf = False

#objetos que seran base de datos y colecciones de MongoDB de mi app
mongo_tickers_list = Mongo_stock_metadata('stock_metadata', 'tickers_list')
mongo_ticker_info = Mongo_stock_metadata('stock_metadata', 'tickers_info')
mongo_scores = Mongo_stock_metadata('stock_metadata', 'model_scores')

#ELIMINAR COLECCIONES SI FUESE NECESARIO
if delete_collections:
	#mongo_tickers_list.coleccion.drop()
	#mongo_ticker_info.coleccion.drop()
	mongo_scores.coleccion.drop()
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

if read_scores:
	all_scores = mongo_scores.read_all_from_mongodb()
	for doc in all_scores:
		for k, v in doc.items():
			print(k,':', v)
	#leo por la clave del indice del documento
	one_score = mongo_scores.read_by_key_from_mongodb('_id', '5ffb5869b4327212ce2da102')
	print(one_score)

if read_new_data_yf:
	start = '2021-01-04'
	end = '2021-01-09'
	ticker = 'IDR.MC'
	df = yf.download(ticker, start=start, end=end)
	print(df)
	