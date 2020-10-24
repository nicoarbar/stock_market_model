import pandas as pd
from naragon_stock_prediction_util_functions import read_stock_csv

"""
vamos a predecir para una empresa si va a crecer, bajar o mantenerse en su nivel
la prediccion va en funcion de si el resto de las empresas del ibex como se comportan
se puede ver que hay una correlacion entre los valores de las empresas respecto a una empresa
tenemos datos de casi dos decadas
correlation_matrix = df.corr()
"""

#vamos a generar un modelo para 1 ticker en base al resto de tickers
#podemos realizar una funcion que itere para todos los tickers

#funcion que calcula columna del DF que tiene el porcentaje del cambio respecto a n dias
def porcentaje_variacion_dias(df, n_dias, columna):
	for i in range(1, n_dias + 1):
		df['porc_variacion_dia_{}'.format(i)] = (df[columna].shift(-i) - df[columna]) / df[columna]
		df.fillna(0, inplace=True)
	return df

def media_ultimos_n_dias(df, ticker, n_dias):
	#añadimos columna media de los ultimos n dias
	df['media_ult_{}_dias'.format(n_dias)] = df['adj_' + ticker].rolling(window=n_dias).mean()
	return df 

def etiqueta_crece_baja_mantiene(porc_cambio, *args):
	cols = [c for c in args]
	for col in cols:
		if col > porc_cambio:
			return 1
		elif col < -porc_cambio:
			return -1
		else:
			return 0 

def aplicar_etiquetas_acciones(df, porc_cambio, columna):
	df['target'] = list(map(etiqueta_crece_baja_mantiene(porc_cambio, columna)))		
	return df 

def get_variables_indep_y_target(df, ticker):
	df_indep = df.drop(['Adj Close_{}'.format(ticker), 'target'], 1, inplace=True)
	x = df_indep.values
	y = df['target'].values
	return x, y