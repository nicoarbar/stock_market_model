import yfinance as yf 
from naragon_stock_prediction_util_functions import Mongo_stock_metadata, get_tickers_to_process, get_historical_stock_data
import pandas as pd
 
#seleccionamos los tickers a procesar - pueden ser todos o alguna seleccion de uno en particular
ticker_list = get_tickers_to_process('IDR.MC') #para testear la API el ticker de indra

#fechas de comienzo y fin
#set de datos para testar modelo de 2020 solo hasta septiembre (actualidad)
start_test = '2020-01-01'
end_test = '2020-09-30'

#set de datos para testar modelo de 2019 - datos de 2020 pueden ser anomalos por la pandemia 
start_test = '2019-01-01'
end_test = '2019-12-31'
#directorio donde almaceno los datos de cada ticker historicos con nombre del mes inicio a fin
data_historic_dir_test = 'historic_stock_data_{}_{}'.format(start_test[:7].replace('-',''), end_test[:7].replace('-',''))  

#set de datos historicos
start_train = '2000-01-01'
end_train = '2018-12-31'
#directorio donde almaceno los datos dde cada ticker historicos
data_historic_dir_train = 'historic_stock_data_{}_{}'.format(start_train[:7].replace('-',''), end_train[:7].replace('-','')) 

ticker_info_df = False
ticker_train = True
train_max = True
ticker_test = False

if ticker_info_df:
	#leemos la coleccion con la informacion de los indicadores de los tickers
	mongo_ticker_info = Mongo_stock_metadata('stock_metadata', 'tickers_info')
	#se transformka la info en un dataframe para analizar
	df = pd.DataFrame(mongo_ticker_info.coleccion.find())

	filter_sample = df['ticker_name'] == ticker_sample
	df_filter = df[filter_sample]
	print(df_filter[['ticker_name','website','shortName','beta']])

#para datos historicos solo cojo de Indra - ya que son muchos datos
if ticker_train:
	#si queremos no todo el periodo historico de Yahoo sino un rango de fechas
	#comprobamos si se le pasa la variable de incio de la fecha historica
	if train_max:
		#si no se le pasa el parametro de incio de fecha -saca todo el periodo maximo que tiene Yfinance
		#el modulo de Yfinance tiene su propia funcion para sacar el periodo maximo historico
		for ticker in ticker_list:
			i_ticker = yf.Ticker(ticker)
			df = i_ticker.history(period="max")
			#se renombra el fichero csv con la colectilla 'max'
			df.to_csv('{}/{}_max.csv'.format(data_historic_dir_train, ticker))		
	else:
		get_historical_stock_data(ticker_list, start_train, end_train, data_historic_dir_train)

#para datos de 2020 se coge de toda la lista de tickers del ibex 35 - solo de Indra
#tomamos datos de 2019 tambien para probar inferencias ya que los datos de 2020 son anomalos, no normales por la pandemia
if ticker_test:
	get_historical_stock_data(ticker_list, start_test, end_test, data_historic_dir_test)


