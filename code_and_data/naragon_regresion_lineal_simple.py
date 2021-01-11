#MODELO DEE REGRESION LINEAL EN EL QUE SE PREDICEN LOS PRECIOS EN FUNCION DE DATOS HISTORICOS
#CADA TICKER VA POR SEPARADO

import pandas as pd
from datos_y_funciones.naragon_ml_model_functions import *
from datos_y_funciones.naragon_stock_prediction_util_functions import get_tickers_to_process, Mongo_stock_metadata

#modelos de regresion lineal de sklearn y regresion de SVM
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Lasso
from sklearn.linear_model import ElasticNet
from sklearn.svm import SVR

#datos a procesar en el directorio
annomes_procesar_train = '200001_201812' #train
annomes_procesar_test = '201901_201912' #test
data_dir_train = 'datos_y_funciones/historic_stock_data_{}'.format(annomes_procesar_train)
data_dir_test = 'datos_y_funciones/historic_stock_data_{}'.format(annomes_procesar_test)
model_filename = 'modelos_desarrollados'

#o se puede coger toda la lista de tickers
tickers_list = get_tickers_to_process(ticker_col='tickers_ibex35')

#el codigo está preparado para analizar todos los ticker de la lista en un bucle for 
#sin embargo para probar solo tomaré uno de ejemplo - cojo el ticker de Indra
tickers_list = ['IDR.MC']

#se crea la columna con la prediccion de dentro de n numero de dias
#sera la variable objetivo
#para ello lo que se hace es para cada fecha poner el valor que tiene el precio de la accion en n dias futuros
n_dias_pred = 15

#data_pred_dir
data_pred_dir = 'datos_y_funciones/predicted_data'

#objeto Mongo para almacenar scores en la colección model_scores
mongo_scores = Mongo_stock_metadata('stock_metadata', 'model_scores')

for ticker in tickers_list:
	#se lee fichero del ticker de test y train
	df_train = get_adj_close_df(ticker, data_dir_train)
	df_test  = get_adj_close_df(ticker, data_dir_test)

	#se crea la columna de prediccion con el parametro de n_dias_pred
	df_train['prediccion_n_dias'] = df_train[['Adj Close']].shift(-n_dias_pred)
	df_test['prediccion_n_dias'] = df_test[['Adj Close']].shift(-n_dias_pred)

	#se elimina las filas que no tienen valor ya que la nueva columna tendra las ultimas n filas vacias
	df_train.dropna(subset=['prediccion_n_dias'], inplace=True)
	df_test.dropna(subset=['prediccion_n_dias'], inplace=True)

	#se separa la variable objetivo de la independiente
	x_train = df_train.drop(['prediccion_n_dias'], 1, inplace=False)
	y_train = df_train.drop(['Adj Close'], 1, inplace=False)
	x_test = df_test.drop(['prediccion_n_dias'], 1, inplace=False)
	y_test = df_test.drop(['Adj Close'], 1, inplace=False)

	#se toman los dataframes como arrays para entrenar e inferir
	x_train = x_train.to_numpy()
	y_train = y_train.to_numpy()
	x_test = x_test.to_numpy() 
	y_test = y_test.to_numpy() 

	#vamos a probar los tipos de regresiones
	#primero tenemos que crear el objeto modelo
	
	#regresion lineal
	regresion_lineal = LinearRegression()
	#lasso
	lasso = Lasso()
	#elastic net
	elastic_net = ElasticNet()
	#regresion de SVM
	svr = SVR() 

	#con la funcion 'modelo_fit_predict_and_score' hacemos el fit, predict y score directamente
	#nos devuelve el score y la columna de prediccion 
	accuracy_regresion, y_pred_regresion, regresion_lineal = modelo_fit_predict_and_score(regresion_lineal, x_train, y_train, x_test, y_test)
	accuracy_lasso, y_pred_lasso, lasso = modelo_fit_predict_and_score(lasso, x_train, y_train, x_test, y_test)
	accuracy_elastic_net, y_pred_elastic_net, elastic_net = modelo_fit_predict_and_score(elastic_net, x_train, y_train, x_test, y_test)
	accuracy_svr, y_pred_svr, svr = modelo_fit_predict_and_score(svr, x_train, y_train, x_test, y_test)

	#voy a guardar la columna y_pred de los modelos junto a los datos de test
	#el df_test se tendra que unir a el array resultante
	#con esta funcion se guarda el df resultante en un fichero csv
	join_test_df_with_pred_array_to_csv(y_pred_regresion, df_test, ticker, data_pred_dir, 'regresion_linal')
	join_test_df_with_pred_array_to_csv(y_pred_lasso, df_test, ticker, data_pred_dir, 'lasso')
	join_test_df_with_pred_array_to_csv(y_pred_elastic_net, df_test, ticker, data_pred_dir, 'elastic_net')
	join_test_df_with_pred_array_to_csv(y_pred_svr, df_test, ticker, data_pred_dir, 'svr')

	#se almacenan los scores en MongoDB
	#se crea diccionario que se inserta directamente como un elemento de la colección por cada ticker
	model_scores_dict = {}
	#se le quita el punto MC del nombre al ticker ya que no se permite ese nombre como clave de Mongo
	ticker_simple = ticker.replace('.MC','')
	model_scores_dict[ticker_simple + '_regresion_lineal'] = accuracy_regresion
	model_scores_dict[ticker_simple + '_lasso'] = accuracy_lasso
	model_scores_dict[ticker_simple + '_elastic_net'] = accuracy_elastic_net
	model_scores_dict[ticker_simple + '_svr'] = accuracy_svr
	mongo_scores.insert_in_mongodb(model_scores_dict)

	#se guarda el modelo en pickle con las fechas de entrenamiento
	save_model_in_pickle_object('{}/{}_regresion_lineal_simple_{}'.format(model_filename,ticker_simple, annomes_procesar_train), regresion_lineal)
	save_model_in_pickle_object('{}/{}_lasso_simple_{}'.format(model_filename,ticker_simple, annomes_procesar_train), lasso)
	save_model_in_pickle_object('{}/{}_elastic_net_simple_{}'.format(model_filename,ticker_simple, annomes_procesar_train), elastic_net)
	save_model_in_pickle_object('{}/{}_svr_simple_{}'.format(model_filename,ticker_simple, annomes_procesar_train), svr)



