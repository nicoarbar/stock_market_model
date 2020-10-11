#script para leer y hacer analitica en MongoDB
from naragon_stock_prediction_util_functions import Mongo_stock_metadata

#objetos que seran base de datos y colecciones de MongoDB de mi app
mongo_tickers_sectors = Mongo_stock_metadata('stock_metadata', 'tickers_sectors')
mongo_ticker_info = Mongo_stock_metadata('stock_metadata', 'tickers_info')

#se lee el primer elemento de cada coleccion
mongo_tickers_sectors_one = mongo_tickers_sectors.read_one_from_mongodb()
mongo_tickers_info_one = mongo_ticker_info.read_one_from_mongodb()

#print(mongo_tickers_sectors_one)
#print(mongo_tickers_info_one)

#se todo de cada coleccion
mongo_tickers_sectors_all_prim = mongo_tickers_sectors.read_all_from_mongodb()[0]
mongo_tickers_sectors_all_segu = mongo_tickers_sectors.read_all_from_mongodb()[1]
mongo_tickers_info_all_prim = mongo_ticker_info.read_all_from_mongodb()[0]

print(mongo_tickers_sectors_all_prim)
print(mongo_tickers_sectors_all_segu)
print(mongo_tickers_info_all_prim)



