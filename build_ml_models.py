import pandas as pd
from naragon_stock_prediction_util_functions import read_stock_csv
from naragon_ml_model_functions import *
from sklearn import svm, cross_validation, neighbors
from sklearn.ensemble import VotingClassifier, RandomForestClassifier

#datos a procesar en el directorio
annomes_procesar = '200001_201812' #train
annomes_procesar = '201901_201912' #test
parent_data_dir = 'lectura_escritura_almacenamiento_datos'
data_dir = parent_data_dir + '/' + 'historic_stock_data_' + annomes_procesar

#seleccionamos parametros para construir el modelo de entrenamiento y ajuste
#elegimos una empresa a analizar - el ticker corresponde a Indra
ticker = 'IDR'
variable_objetivo = 'Adj Close_' + ticker
porcentaje_cambio_etiqueta = 0.02
dias_analisis_variacion = 1
col_target = 'porc_variacion_dia_'.format(dias_analisis_variacion)

#leemos el Df total
df = read_stock_csv('TOTAL_' + annomes_procesar, data_dir)
#aplicamos columnas de interes para el analisis
df_porc = porcentaje_variacion_dias(df = df, n_dias=dias_analisis_variacion, columna=variable_objetivo)
#aplicamos las etiquetas con la columna 'target'
df_with_target = aplicar_etiquetas_acciones(df=df_porc, porc_cambio=porcentaje_cambio_etiqueta, columna=col_target)
#cogemos las variables independientes y la objetivo:'target'
x, y = get_variables_indep_y_target(df_with_target, ticker)