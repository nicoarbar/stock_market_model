#imports para Scrapear datos
import bs4 as bs #beautifulsoup - procesa HTML para web scraping
import pickle #serializa cualquier objeto de python - guarda la lista de tickers
import requests #llamadas a la API

#imports para trabajar con el sistema
import datetime as dt 
import os #revisa si existen directorios y ficheros
import time #necesito la funcion sleep al invocar a la API 
import logging #logger para llevar una traza del programa
import json

#imports de procesamiento y almacenamiento de datos
import pandas as pd #trabajar con dataframes
import pandas_datareader.data as web #lee datos de Yahoo Finance
import pymongo  #almacenar datos en MongoDB
import yfinance as yf  #modulo de Yahoo Finance para interactuar con su API e ingestar datos 


LOG_FORMAT = '%(asctime)s %(levelname)s - %(message)s'
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
logging.basicConfig(filename='scrapingstock.log', level=logging.INFO, format = LOG_FORMAT, filemode ='w', datefmt=DATETIME_FORMAT)
logger = logging.getLogger()

#comienzo y fin de datos historicos
start = dt.datetime(2000,1,1)
end = dt.datetime(2019,12,31)

#nombre fichero donde se alamacenan los tickers si se quiere
pickle_filename = 'sp500tickers.pickle'
#nombre diretorio a descargar ficheros de datos historicos
data_historic_dir = 'stock_data_historic_dir'
#nombre fichero para tickers no procesados
not_processed_filename = 'tickers_no_procesados.csv'

#funcion para tener un logger de trazabilidad
def logger_for_my_stock_app():
	logging.basicConfig(filename='scrapingstock.log', level=logging.INFO, format = LOG_FORMAT, filemode ='w', datefmt=DATETIME_FORMAT)
	logger = logging.getLogger()
	return logger

#funcion que busca una tabla de una pagina y coge columnas - se selecciona la columna con 'col_position'
def scrap_tickers(url, col_position):
	resp = requests.get(url)
	soup = bs.BeautifulSoup(resp.text, features="html5lib")
	table = soup.find('table', {'class':'wikitable sortable'})
	tickers = []
	logger.info('Buscando los tickers y su sector en la tabla HTML para scrapear')
	for row in table.findAll('tr')[1:]:
		ticker = row.findAll('td')[col_position].text
		ticker_with_no_space = ticker.rstrip("\n")
		tickers.append(ticker_with_no_space)
	return tickers

#si se quiere guardar los tickers en un objeto pickle de serializacion de python
def save_scrapped_tickers(pickle_filename, tickers):
	with open(pickle_filename,"wb") as f:
		pickle.dump(tickers, f)

#abrimos los tickers almacenados en el fichero de formato pickle
def open_scrapped_tickers(pickle_filename):
	with open(pickle_filename,"rb") as f:
		tickers = pickle.load(f)
	return tickers

#funcion que abre los tickers guardados o hace la llamada de nuevo
def get_data_from_yahoo(url, start, end, pickle_filename, data_historic_dir, not_processed_filename, recargar_tickers = False):
	tickers_no_procesados =[]
	if recargar_tickers:
		logger.info('Se buscan los tickers en la web')
		tickers = scrap_tickers(url)
	else:
		with open(pickle_filename,"rb") as f:
			tickers = pickle.load(f)
	#guarda en memoria
	if not os.path.exists(data_historic_dir):
		logger.info('No existe el directorio {}'.format(data_historic_dir))
		os.makedirs(data_historic_dir)
	
	logger.info('Se obtienen los datos de cada ticker')
	for ticker in tickers:
		logger.info('obteniendo info del ticker {}'.format(ticker))
		if not os.path.exists('{}/{}.csv'.format(data_historic_dir, ticker)):
			try:
				df = web.DataReader(ticker,'yahoo', start, end)
				df.to_csv('{}/{}.csv'.format(data_historic_dir, ticker))
			except:
				time.sleep(2)
				tickers_no_procesados.append(ticker)
				with open(not_processed_filename, 'w') as csv_tickers_no_procesados:
					csv_tickers_no_procesados.write(ticker)
		else:
			logger.info('Ya se tiene fichero historico de {}'.format(ticker))
	return tickers


#se crea una clase con funciones hechas a medidas para insertar documentos en colecciones de MongoDb
class Mongo_stock_metadata:
	def __init__(self, bbdd, coleccion):
		self.client = pymongo.MongoClient('localhost', 27017)
		self.bbdd = bbdd
		self.logger = logger
		self.db = self.client[self.bbdd]
		self.coleccion = self.db[coleccion]
		
	#funcion para almacenar datos en formato diccionario en MongoDB
	def insert_in_mongodb(self, dict_key_value):
		#se inserta
		logger.info('Insertando datos en la coleccion de MongoDB')
		if type(dict_key_value) == 'list':
			self.coleccion.insert_many(dict_key_value)
		elif len(dict_key_value) >= 1:
			self.coleccion.insert_one(dict_key_value)
		else:
			logger.warning('El documento a insertar esta vacio')
	
	def read_by_key_from_mongodb(self, key, value):
		logger.info('Leyendo datos en la coleccion de MongoDB')
		return self.coleccion.find_one({key:value})

	def read_all_from_mongodb(self):
		logger.info('Leyendo datos en la coleccion de MongoDB')
		return self.coleccion.find()

	def read_doc_keys_from_collection(self):
		logger.info('Leyendo datos en la coleccion de MongoDB')
		list_keys = []
		for document in self.coleccion.find():
			list_keys.append(document.keys())
		return list_keys

	def query_collections(self, my_query):
		logger.info('Leyendo query en la coleccion de MongoDB')
		return self.coleccion.find(my_query)
		 
	def count_elements_collection(self):
		return self.coleccion.find().count()

	def delete_collection(self):
		return self.coleccion.drop()


def insert_ticker_metadata_in_mongo(mongo_object, ticker_col, tickers_list):
	#almacenar tickers en mongoDB
	tickers_for_mongo = {'ticker_market': ticker_col}
	tickers_for_mongo['ticker_list'] = tickers_list
	#insertamos
	mongo_object.insert_in_mongodb(tickers_for_mongo) #insertamos listado de tickers en la coleccion
	#leemos que hay en mongo al logger
	logger.info('Coleccion en Mongo {}'.format(mongo_object.coleccion))	


def insert_ticker_info_in_mongo(mongo_object, ticker):
	logger.info('Ticker a procesar: {}'.format(ticker))
	ticker_api = yf.Ticker(ticker)
	try:
		ticker_api_info_str = json.dumps(ticker_api.info)
		ticker_api_info_dict = json.loads(ticker_api_info_str)
		ticker_api_info_dict['ticker_name'] = ticker
		ticker_api_info_dict['fecha_hora_insercion'] = dt.datetime.now()
		mongo_object.insert_in_mongodb(ticker_api_info_dict)
	except:
		pass

def get_tickers_list(ticker_col):
	mongo_tickers_list = Mongo_stock_metadata('stock_metadata', 'tickers_list')
	tickers_list = mongo_tickers_list.read_by_key_from_mongodb('ticker_market', ticker_col)['ticker_list']
	return tickers_list

#ticker_sample puede ser un ticker o una lista de tickers para descargar datos historicos
def get_historical_stock_data(ticker_sample, start, end, data_historic_dir):
	#podemos guardar para cada ticker los diferentes valores
	tickers_no_procesados = []
	#guarda en memoria
	if not os.path.exists(data_historic_dir):
		logger.info('No existe el directorio {}'.format(data_historic_dir))
		os.makedirs(data_historic_dir)

	for ticker in ticker_sample:
		logger.info('Obteniendo info del ticker {}'.format(ticker))
		if not os.path.exists('{}/{}.csv'.format(data_historic_dir, ticker)):
			try:
				df = yf.download(ticker, start=start, end=end)
				df.to_csv('{}/{}.csv'.format(data_historic_dir, ticker))
			except:
				logger.info('No se ha podido obtener historico del ticker: {}'.format(ticker))
				tickers_no_procesados.append(ticker)

	#reporcesado de algun ticker que falla en las peticiones a la API
	if len(tickers_no_procesados) > 0:
		time.sleep(20)
		for ticker in tickers_no_procesados:
			if not os.path.exists('{}/{}.csv'.format(data_historic_dir, ticker)):
				try:
					df = yf.download(ticker, start=start, end=end)
					df.to_csv('{}/{}.csv'.format(data_historic_dir, ticker))
				except:
					logger.info('No se ha podido obtener historico del ticker: {}'.format(ticker))
	