import pandas as pd
from naragon_stock_prediction_util_functions import read_stock_csv, get_tickers_to_process

#datos a procesar en el directorio
annomes_procesar = '201901_201912' #test
annomes_procesar = '200001_201812' #train
data_dir = 'historic_stock_data_{}'.format(annomes_procesar)
join_ticker_train_data = True

#leer csv de datos que guardamos
#leemos lista de tickers 
if join_ticker_train_data:
	total_df = pd.DataFrame()
	tickers_list = get_tickers_to_process(ticker_col='tickers_ibex35')
	for ticker in tickers_list:
		df = read_stock_csv(ticker, data_dir)
		#borramos algunas columnas que no nos interesan - ya que sera un DF bastante grande
		df.drop(['Open','Close','Volume'],1, inplace=True)
		#renombramos las columnas con su ticker
		ticker_name = ticker.replace('.MC','')
		diccionario_col_renombrar = {'High': 'max_{}'.format(ticker_name), 'Low':'min_{}'.format(ticker_name), 'Adj Close': 'adj_{}'.format(ticker_name)}
		df.rename(columns=diccionario_col_renombrar, inplace=True)

		#ahora haremos join con el dataframe principal
		#el join se hace a través del 'index' que sera 'Date' la fechas
		#se hace outer join para mantener que todas las fechas de todos los tickers esten presentes 
		if total_df.empty:
			total_df = df 
		else:
			total_df = total_df.join(df, how='outer')
	#una vez que termina de unir todos los ficheros de los tickers
	#se guarda el fichero en el directorio bajo el nombre 'total.csv'
	total_df.to_csv('{}/{}.csv'.format(data_dir, 'TOTAL_' + annomes_procesar))


#print(df.corr())