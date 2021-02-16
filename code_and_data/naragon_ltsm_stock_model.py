# Algortimo LSTM
from datos_y_funciones.naragon_ml_model_functions import get_adj_close_df
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

from keras.models import Sequential
from keras.layers import Dense, LSTM

annomes_procesar_train = '200001_201812' 
annomes_procesar_test = '201901_201912' 
data_dir_train = 'datos_y_funciones/historic_stock_data_{}'.format(annomes_procesar_train)
data_dir_test = 'datos_y_funciones/historic_stock_data_{}'.format(annomes_procesar_test)
data_pred_dir = 'datos_y_funciones/predicted_data'

ticker = 'IDR.MC'

data_train = get_adj_close_df(ticker, data_dir_train)
data_test = get_adj_close_df(ticker, data_dir_test)

#se preparan los datos normalizando los valores de las acciones en un rango de 0 a 1
sc = MinMaxScaler(feature_range = (0,1))
train_normalizado = sc.fit_transform(data_train)

#tomar bloques de n datos consecutivos almacenados en conjuntos
#el siguiente dato es el que se infiere de ese subconjunto de n datos
time_step = 60
x_train = []
y_train = []
n_datos_train = len(train_normalizado)

for i in range(time_step, n_datos_train):
	x_train.append(train_normalizado[i, - time_step:i, 0])
	y_train.append(train_normalizado[i, 0])

x_train, y_train = np.array(x_train), np.array(y_train)

#cada dato sera 60x1
x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

n_neuronas = 50
dim_entrada = (x_train.shape[1],1)
dim_salida = 1 

#construimos modelo - contenedor de la red
modelo = Sequential()
#n_neuronas + tamaño entrada
modelo.add(LSTM(units=n_neuronas, input_shape=dim_entrada))
#capa de salida
modelo.add(Dense(units=dim_salida))
#metodo rmsprop similar al gradiente descendente para el entrenamiento + funcion de error
modelo.compile(optimizer='rmsprop', loss='mse')
#lotes de 32 ejemplos y 20 iteraciones
modelo.fit(x_train, y_train, epcohs=20, batch_size=32)

#prediccion
#se normaliza
x_test = data_test.values
x_test = sc.transform(x_test)

#se reorganiza para crear bloques de 60 datos
x_test = []
for i in range(time_step, len(x_test)):
	x_test.append(x_test[i, - time_step:i, 0])
x_test = np.array(x_test)
x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

#se realiza la prediccion y desnormalizacion
prediccion = modelo.predict(x_test)
prediccion = sc.inverse_transform(prediccion)