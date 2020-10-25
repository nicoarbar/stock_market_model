import pandas as pd
from naragon_stock_prediction_util_functions import read_stock_csv, get_tickers_to_process

#datos a procesar en el directorio
annomes_procesar = '201901_201912' #test
annomes_procesar = '200001_201812' #train
data_dir = 'historic_stock_data_{}'.format(annomes_procesar)
join_ticker_train_data = True
#parametro de columnas que quiero en mi DF unificado
#columnas_df = ['High', 'Low', 'Adj Close']
columnas_df = ['Adj Close']

#leer csv de datos que guardamos
#leemos lista de tickers 
if join_ticker_train_data:
	total_df = pd.DataFrame()
	tickers_list = get_tickers_to_process(ticker_col='tickers_ibex35')
	for ticker in tickers_list:
		df = read_stock_csv(ticker, data_dir)
		#borramos algunas columnas que no nos interesan - ya que sera un DF bastante grande
		df.drop(['Open','Close','Volume', 'High', 'Low'],1, inplace=True)
		#renombramos las columnas con su ticker
		ticker_name = ticker.replace('.MC','')
		
		#nombrado de columnas en base a los campos que quiero con sufijo ticker
		diccionario_col_renombrar = {}
		for col_name in columnas_df:
			diccionario_col_renombrar[col_name] = col_name + '_' + ticker_name
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