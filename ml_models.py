import pandas as pd
from naragon_stock_prediction_util_functions import read_stock_csv

#datos a procesar en el directorio
annomes_procesar = '200001_201812' #train
annomes_procesar = '201901_201912' #test
data_dir = 'historic_stock_data_{}'.format(annomes_procesar)

#leemos el Df total
df = read_stock_csv('TOTAL_' + annomes_procesar, data_dir)
#rellenamos los valores nulos
df.fillna(0, inplace=True)

#vamos a predecir para una empresa si va a crecer, bajar o mantenerse en su nivel
#la prediccion va en funcion de si el resto de las empresas del ibex como se comportan
#se puede ver que hay una correlacion entre los valores de las empresas respecto a una empresa
correlation_matrix = df.corr()

