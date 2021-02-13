import pandas as pd
import numpy as np
import os
from datos_y_funciones.naragon_stock_prediction_util_functions import read_stock_csv
import pickle
from datetime import datetime, timedelta

"""
vamos a predecir para una empresa si va a crecer, bajar o mantenerse en su nivel
la prediccion va en funcion de si el resto de las empresas del ibex como se comportan
se puede ver que hay una correlacion entre los valores de las empresas respecto a una empresa
tenemos datos de casi dos decadas
correlation_matrix = df.corr()
"""

#vamos a generar un modelo para 1 ticker en base al resto de tickers
#podemos realizar una funcion que itere para todos los tickers

def get_adj_close_df(ticker, data_dir):
	df = read_stock_csv(ticker, data_dir)
	df.drop(['Open','Close','Volume', 'High', 'Low'],1, inplace=True)
	return df

def get_adj_close_col(df):
	df.drop(['Open','Close','Volume', 'High', 'Low'],1, inplace=True)
	return df

def union_train_and_test_df(test_df, train_df):
	union_df = pd.concat([train_df, test_df])
	return union_df

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

#para la variable independiente solo se mantienen las columnas de variacion
def get_variables_indep_y_target(df, col_target):
	cols_to_drop = []
	for col in df.columns:
		if 'target' in col:
			cols_to_drop.append(col)
	cols_to_drop.append('Adj Close')
	df_indep = df.drop(cols_to_drop, 1, inplace=False)
	x = df_indep.to_numpy()
	y = df[col_target].to_numpy()
	return x, y

def get_ticker_variables_indep_y_target(df, col_target):
	cols_to_drop = []
	for col in df.columns:
		if 'target' in col:
			cols_to_drop.append(col)
		elif 'porc_variacion_dias' in col:
			cols_to_drop.append(col)
	df_indep = df.drop(cols_to_drop, 1, inplace=False)
	x = df_indep.to_numpy()
	y = df[col_target].to_numpy()
	return x, y


def get_data_model_sube_baja_mantiene(df_porc, porcentaje_cambio_etiqueta, dias_analisis_variacion):
	#aplicamos las etiquetas con la columna 'target'
	for i in range(1, dias_analisis_variacion +1):
		#si el porcentaje de variacion es mayor que el porcentaje de cambio como parametro se le asigna 1, sino -1
		df_porc['target_dia'+'_{}'.format(i)] = np.select(
			[
			df_porc['porc_variacion_dia' +'_'+'{}'.format(i)].between(porcentaje_cambio_etiqueta*-1, porcentaje_cambio_etiqueta, inclusive = False),
			df_porc['porc_variacion_dia' +'_'+'{}'.format(i)] >= porcentaje_cambio_etiqueta,
			df_porc['porc_variacion_dia' +'_'+'{}'.format(i)] <= porcentaje_cambio_etiqueta,
			],
			[0,1,-1],
			default=0)
	return df_porc

#es lo mismo que la funcion score del clasiffier
def porcentaje_acierto_modelo(y_pred, y_test):
	acertado = []
	n_rows = len(y_pred)
	for i in range(n_rows):
		if y_pred[i] == y_test[i]:
			acertado.append(i)
	porc_acierto = (len(acertado)/n_rows)  * 100
	return porc_acierto

def modelo_fit_predict_and_score(modelo, x_train, y_train, x_test, y_test):
	#entrenamos con datos de entrenamiento
	modelo.fit(x_train, y_train)
	#prediccion con datos de test
	y_pred = modelo.predict(x_test)
	#score
	accuracy = modelo.score(x_test, y_test)
	return accuracy, y_pred, modelo

def modelo_predict_new_data(modelo, x_test):
	#prediccion con datos de test
	y_pred = modelo.predict(x_test)
	return y_pred

def join_test_df_with_pred_array_to_csv(y_pred, df_test, ticker, data_pred_dir, modelo):
	#convertimos el array predicho en dataframe y se nombra la columns
	pred_df = pd.DataFrame(y_pred, columns=['prediccion_modelo'])
	#se resetea el indice del dataframe de test para hace el join por indice
	reset_index_df = df_test.reset_index()
	#se hace el join
	resultado_df = reset_index_df.join(pred_df)
	#se vuelve a poner la columna 'Date' como indice
	resultado_df.set_index('Date', inplace=True)
	#finalmente se guarda en una nueva carpeta en un fichero csv. Si no existee la carpeta se crea
	if not os.path.exists(data_pred_dir):
		os.makedirs(data_pred_dir)
	resultado_df.to_csv('{}/{}.csv'.format(data_pred_dir, ticker + '_' + modelo))

def save_model_in_pickle_object(model_name, model):
	pickle.dump(model, open(model_name, 'wb'))

def open_model_in_pickle_object(model_name):
	restored_model = pickle.load(open(model_name, 'rb'))
	return restored_model

#funcion que calcula la diferencia en porcentaje del valor dee un dia para otro en el cierre
def percentage_diff(actual_value, prev_value):
	diff_value = actual_value - prev_value
	return diff_value / prev_value * 100

def get_current_date_minus_n_day_difference(n_day_difference):
	current_date = datetime.today()
	current_date_day_difference = current_date - timedelta(days=n_day_difference)
	current_date_str = current_date.strftime('%Y-%m-%d')
	current_date_day_difference_str = current_date_day_difference.strftime('%Y-%m-%d')
	return current_date_str, current_date_day_difference_str