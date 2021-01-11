#MODELOS DE CLASIFICACION - SUBE, BAJA, SE MANTIENE

import pandas as pd
from datos_y_funciones.naragon_ml_model_functions import *
from datos_y_funciones.naragon_stock_prediction_util_functions import get_tickers_to_process, Mongo_stock_metadata
#modelos ml de sklearn
from sklearn import svm, neighbors
from sklearn.ensemble import VotingClassifier, RandomForestClassifier

#datos a procesar en el directorio
annomes_procesar_train = '200001_201812' #train
annomes_procesar_test = '201901_201912' #test
data_dir_train = 'datos_y_funciones/historic_stock_data_{}'.format(annomes_procesar_train)
data_dir_test = 'datos_y_funciones/historic_stock_data_{}'.format(annomes_procesar_test)

#data_pred_dir
data_pred_dir = 'datos_y_funciones/predicted_data'
#ruta para almacenar los modelos
model_filename = 'modelos_desarrollados'

#elegimos una empresa a analizar - el ticker corresponde a Indra
#o se puede coger toda la lista de tickers
tickers_list = get_tickers_to_process(ticker_col='tickers_ibex35')
tickers_list = ['IDR.MC']

#objeto Mongo para almacenar scores en la colección model_scores
mongo_scores = Mongo_stock_metadata('stock_metadata', 'model_scores')

#seleccionamos parametros para construir el modelo de entrenamiento y ajuste
porcentaje_cambio_etiqueta = 0.04
dias_analisis_variacion = 5

#se leen datos totales de entrenamiento y ajuste
df_train = read_stock_csv('TOTAL_' + annomes_procesar_train, data_dir_train)
df_test = read_stock_csv('TOTAL_' + annomes_procesar_test, data_dir_test)

#se tiene que limpiar los datos ya que tiene muchos nulos _indice
#axis = 0 indica filas, how='any' indica que algunos de los valores son nulos
df_train.dropna(axis=0, how='any', inplace=True)
df_test.dropna(axis=0, how='any', inplace=True)

#iteramos sobre cada ticker
for ticker in tickers_list:
	#en el fichero TOTAL los nombres de las columnas tienen el ticker sin el '.MC'
	ticker_simple = ticker.replace('.MC','')

	#aplicamos columnas de interes para el analisis - sera a columa de porcentaje de variacion de dias
	df_porc_train = porcentaje_variacion_dias(df = df_train, n_dias=dias_analisis_variacion, columna='Adj Close_{}'.format(ticker_simple))
	df_porc_test = porcentaje_variacion_dias(df = df_test, n_dias=dias_analisis_variacion, columna='Adj Close_{}'.format(ticker_simple))

	#se aplica la funcion de calcular las variables objetivo en etiquetas
	df_class_train = get_data_model_sube_baja_mantiene(df_porc_train, porcentaje_cambio_etiqueta, dias_analisis_variacion)
	df_class_test = get_data_model_sube_baja_mantiene(df_porc_test, porcentaje_cambio_etiqueta, dias_analisis_variacion)

	#cogemos las variables independientes y la objetivo:'target'
	x_train, y_train = get_ticker_variables_indep_y_target(df_class_train, 'target_dia' + '_' + str(dias_analisis_variacion))
	x_test, y_test = get_ticker_variables_indep_y_target(df_class_test, 'target_dia' + '_' + str(dias_analisis_variacion))

	#ya tenemos los datos vamos a construir el modelo
	clasificador_knc = neighbors.KNeighborsClassifier()
	#el modelo VotingClassifier asigna el mejor clasificador de todos los que se le pasen
	#VotingClassifier se le pasan tuplas de distintos clasificadores
	clasificador_vc = VotingClassifier([
		('lsvc', svm.LinearSVC()),
		('knn', neighbors.KNeighborsClassifier()),
		('rfor', RandomForestClassifier())
		])
	#con esta funcion a medida se hace el fit, predict y el score para modelos de clasificacion
	accuracy_knc, y_pred_knc, clasificador_knc = modelo_fit_predict_and_score(clasificador_knc, x_train, y_train, x_test, y_test)
	accuracy_vc, y_pred_vc, clasificador_vc = modelo_fit_predict_and_score(clasificador_vc, x_train, y_train, x_test, y_test)
	
	# mi funcion de score tiene que dar el mismo resultado que el score del clasificador
	mi_accuracy_knc = porcentaje_acierto_modelo(y_pred_knc, y_test)
	mi_accuracy_vc = porcentaje_acierto_modelo(y_pred_vc, y_test)


	#voy a almacenar los resultados de la prediccion en el dataframe de test con los indicadores calculados
	join_test_df_with_pred_array_to_csv(y_pred_knc, df_class_test, ticker, data_pred_dir, 'clasificacion_knc_multiple')
	join_test_df_with_pred_array_to_csv(y_pred_vc, df_class_test, ticker, data_pred_dir, 'clasificacion_vc_multiple')

	#se almacenan los scores en MongoDB
	#se crea diccionario que se inserta directamente como un elemento de la colección por cada ticker
	model_scores_dict = {}
	model_scores_dict[ticker_simple + 'knc_multiple'] = accuracy_knc
	model_scores_dict[ticker_simple + 'voting_classifier_multiple'] = accuracy_vc
	mongo_scores.insert_in_mongodb(model_scores_dict)

	#se guarda el modelo en pickle con las fechas de entrenamiento
	save_model_in_pickle_object('{}/{}_clasificador_knc_multiple_{}'.format(model_filename, ticker_simple, annomes_procesar_train), clasificador_knc)
	save_model_in_pickle_object('{}/{}_clasificador_vc_multiple_{}'.format(model_filename,  ticker_simple, annomes_procesar_train), clasificador_vc)