import pandas as pd
import numpy as np
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

def etiqueta_crece_baja_mantiene(df, porc_cambio, *args):
	cols = [c for c in args]
	for col in cols:
		if df[col] > porc_cambio:
			return 1
		elif df[col] < -porc_cambio:
			return -1
		else:
			return 0 

def aplicar_etiquetas_acciones(df, porc_cambio, columna):
	df['target'] = 	df.apply(etiqueta_crece_baja_mantiene(df, porc_cambio, columna), axis =1)
	return df 

def get_variables_indep_y_target(df, ticker, col_target):
	cols_to_drop = []
	for col in df.columns:
		if 'target' in col:
			cols_to_drop.append(col)
		elif 'porc_variacion' in col:
			cols_to_drop.append(col)
	cols_to_drop.append('Adj Close_{}'.format(ticker))
	df_indep = df.drop(cols_to_drop, 1, inplace=False)
	x = df_indep.values
	y = df[col_target].values
	return x, y


def get_data_model_sube_baja_mantiene(annomes_procesar, ticker, porcentaje_cambio_etiqueta, dias_analisis_variacion, col_target_dia):
	#nombres columnas clave
	col_porcentajes = 'porc_variacion_dia'
	col_target = 'target_dia'

	#directorio donde estan los ficheros csv con datos
	data_dir = 'historic_stock_data_' + annomes_procesar

	#leemos el Df total
	df = read_stock_csv('TOTAL_' + annomes_procesar, data_dir)

	#aplicamos columnas de interes para el analisis
	df_porc = porcentaje_variacion_dias(df = df, n_dias=dias_analisis_variacion, columna='Adj Close_' + ticker)

	#aplicamos las etiquetas con la columna 'target'
	for i in range(1, dias_analisis_variacion +1):
		#si el porcentaje de variacion es mayor que el porcentaje de cambio como parametro se le asigna 1, sino -1
		df_porc[col_target+'_{}'.format(i)] = np.where(df[col_porcentajes +'_'+'{}'.format(i)] > porcentaje_cambio_etiqueta, 1, -1)
		#si la variacion es la misma que el parametro se le asigna 0
		df_porc[col_target+'_{}'.format(i)] = np.where(df[col_porcentajes +'_'+'{}'.format(i)] == porcentaje_cambio_etiqueta, 0, df_porc[col_target+'_{}'.format(i)])

	#cogemos las variables independientes y la objetivo:'target'
	x, y = get_variables_indep_y_target(df_porc, ticker, col_target + '_' + str(col_target_dia))

	return df_porc, x, y 

#es lo mismo que la funcion score del clasiffier
def porcentaje_acierto_modelo(y_pred, y_test):
	acertado = []
	n_rows = len(y_pred)
	for i in range(n_rows):
		if y_pred[i] == y_test[i]:
			acertado.append(i)
	porc_acierto = (len(acertado)/n_rows)  * 100
	return porc_acierto

def clasificador_fit_predict_and_score(clasificador, x_train, y_train, x_test, y_test):
	#entrenamos con datos de entrenamiento
	clasificador.fit(x_train, y_train)
	#prediccion con datos de test
	y_pred = clasificador.predict(x_test)
	#score
	accuracy = clasificador.score(x_test, y_test)
	return accuracy, y_pred