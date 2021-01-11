#MODELO DEE REGRESION LINEAL MULTIPLE EN EL QUE SE PREDICEN LOS PRECIOS EN FUNCION DE DATOS HISTORICOS DEL INDICE


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
#ruta para almacenar los modelos
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

#se leen datos totales de entrenamiento y ajuste
df_train = read_stock_csv('TOTAL_' + annomes_procesar_train, data_dir_train)
df_test = read_stock_csv('TOTAL_' + annomes_procesar_test, data_dir_test)

#se tiene que limpiar los datos ya que tiene muchos nulos 
#axis = 0 indica filas, how='any' indica que algunos de los valores son nulos
df_train.dropna(axis=0, how='any', inplace=True)
df_test.dropna(axis=0, how='any', inplace=True)

for ticker in tickers_list:
	#se le quita el punto MC del nombre al ticker ya que asi estará l nombre de la columna
	ticker_simple = ticker.replace('.MC','')
	
	#se crean las variables independientes y la variable objetivo (sera la columna correspondiente al ticker)
	#para cada ticker, se toma su columna de adj close y será la variable objetivo a predecir
	x_train = df_train.drop(['Adj Close_{}'.format(ticker_simple)], 1, inplace=False)
	y_train = df_train['Adj Close_{}'.format(ticker_simple)]
	x_test = df_test.drop(['Adj Close_{}'.format(ticker_simple)], 1, inplace=False)
	y_test = df_test['Adj Close_{}'.format(ticker_simple)]

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

	#voy a guardar la columna y_pred de los modelos junto a los datos de test de la empresa
	#para ello me genero un dataframe con la columna 'Date' y la columna del precio de la empresa
	df_test_ticker = df_test['Adj Close_{}'.format(ticker_simple)]

	#el df_test se tendra que unir a el array resultante
	#con esta funcion se guarda el df resultante en un fichero csv
	join_test_df_with_pred_array_to_csv(y_pred_regresion, df_test_ticker, ticker, data_pred_dir, 'regresion_linal_multiple')
	join_test_df_with_pred_array_to_csv(y_pred_lasso, df_test_ticker, ticker, data_pred_dir, 'lasso_multiple')
	join_test_df_with_pred_array_to_csv(y_pred_elastic_net, df_test_ticker, ticker, data_pred_dir, 'elastic_net_multiple')
	join_test_df_with_pred_array_to_csv(y_pred_svr, df_test_ticker, ticker, data_pred_dir, 'svr_multiple')

	#se almacenan los scores en MongoDB
	#se crea diccionario que se inserta directamente como un elemento de la colección por cada ticker
	model_scores_dict = {}
	model_scores_dict[ticker_simple + '_regresion_lineal_multiple'] = accuracy_regresion
	model_scores_dict[ticker_simple + '_lasso_multiple'] = accuracy_lasso
	model_scores_dict[ticker_simple + '_elastic_net_multiple'] = accuracy_elastic_net
	model_scores_dict[ticker_simple + '_svr_multiple'] = accuracy_svr
	mongo_scores.insert_in_mongodb(model_scores_dict)

	#se guarda el modelo en pickle con las fechas de entrenamiento
	save_model_in_pickle_object('{}/{}_regresion_lineal_multiple_{}'.format(model_filename,ticker_simple, annomes_procesar_train), regresion_lineal)
	save_model_in_pickle_object('{}/{}_lasso_multiple_{}'.format(model_filename,ticker_simple, annomes_procesar_train), lasso)
	save_model_in_pickle_object('{}/{}_elastic_net_multiple_{}'.format(model_filename,ticker_simple, annomes_procesar_train), elastic_net)
	save_model_in_pickle_object('{}/{}_svr_multiple_{}'.format(model_filename,ticker_simple, annomes_procesar_train), svr)