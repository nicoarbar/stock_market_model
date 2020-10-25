import pandas as pd
from naragon_ml_model_functions import get_data_model_sube_baja_mantiene, porcentaje_acierto_modelo, clasificador_fit_predict_and_score
#modelos ml
from sklearn import svm, neighbors
from sklearn.ensemble import VotingClassifier, RandomForestClassifier

#parametros para lanzar modelos
modelo_knc = False
modelo_vc = True

#seleccionamos parametros para construir el modelo de entrenamiento y ajuste
#elegimos una empresa a analizar - el ticker corresponde a Indra
ticker = 'IDR'
porcentaje_cambio_etiqueta = 0.04
dias_analisis_variacion = 4
col_target_dia = 4

#datos a procesar en el directorio
annomes_procesar_train = '200001_201812' #train
annomes_procesar_test = '201901_201912' #test

#datos train
df_train, x_train, y_train= get_data_model_sube_baja_mantiene(annomes_procesar_train, ticker, porcentaje_cambio_etiqueta, dias_analisis_variacion, col_target_dia)
#datos test 
df_test, x_test, y_test= get_data_model_sube_baja_mantiene(annomes_procesar_test, ticker, porcentaje_cambio_etiqueta, dias_analisis_variacion, col_target_dia)

if modelo_knc:
	#ya tenemos los datos vamos a construir el modelo
	clasificador = neighbors.KNeighborsClassifier()
	#con esta funcion a medida se hace el fit, predict y el score para modelos de clasificacion
	accuracy, y_pred = clasificador_fit_predict_and_score(clasificador, x_train, y_train, x_test, y_test)
	# mi funcion de score tiene que dar el mismo resultado que el score del clasificador
	mi_accuracy = porcentaje_acierto_modelo(y_pred, y_test)

#el modelo VotingClassifier asigna el mejor clasificador de todos los que se le pasen
if modelo_vc:
	#VotingClassifier se le pasan tuplas de distintos clasificadores
	clasificador = VotingClassifier([
		('lsvc', svm.LinearSVC()),
		('knn', neighbors.KNeighborsClassifier()),
		('rfor', RandomForestClassifier())
		])
	#con esta funcion a medida se hace el fit, predict y el score para modelos de clasificacion
	accuracy, y_pred = clasificador_fit_predict_and_score(clasificador, x_train, y_train, x_test, y_test)
	# mi funcion de score tiene que dar el mismo resultado que el score del clasificador
	mi_accuracy = porcentaje_acierto_modelo(y_pred, y_test)

print(accuracy)
print(mi_accuracy)
print(y_pred)