import pandas as pd
from naragon_stock_prediction_util_functions import read_stock_csv

#datos a procesar en el directorio
annomes_procesar = '200001_201812' #train
annomes_procesar = '201901_201912' #test
data_dir = 'historic_stock_data_{}'.format(annomes_procesar)
#elegimos una empresa a analizar - el ticker corresponde a Indra
tickers = 'IDR'

"""
vamos a predecir para una empresa si va a crecer, bajar o mantenerse en su nivel
la prediccion va en funcion de si el resto de las empresas del ibex como se comportan
se puede ver que hay una correlacion entre los valores de las empresas respecto a una empresa
tenemos datos de casi dos decadas
correlation_matrix = df.corr()
"""

#vamos a generar un modelo para 1 ticker en base al resto de tickers
#podemos realizar una funcion que itere para todos los tickers

#leemos el Df total
df = read_stock_csv('TOTAL_' + annomes_procesar, data_dir)
#rellenamos los valores nulos
df.fillna(0, inplace=True)
#añadimos columna media de los ultimos 100 dias
df['media_100_' + ticker] = df['adj_' + ticker].rolling(window=100).mean()

#metodo 'resample' coge frecuencias de periodo que se le indique agrupando
#necesita una funcion de agregacion como la suma o 'ohlc' que calcula minimos y maximos cada 10 dias
df_ohlc = df['Adj Close'].resample('10D').ohlc()
df_volume = df['Volume'].resample('10D').sum()

