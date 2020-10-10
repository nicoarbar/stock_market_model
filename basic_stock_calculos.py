#manipulacion de datos
import pandas as pd
import pandas_datareader.data as web 
import datetime as dt

#graficos
import matplotlob.pyplot as plt
from matplotlib import style 
import matplotlib.dates as mdates
from matplotlib.finance import candlestick_ohlc

#datos historicos
start = dt.datetime(2000,1,1)
end = dt.datetime(2019,12,31)

#scrapeamos el valor TSLA - TESLA
#hay que recordar que el campo 'Date' sera el INDICE del dataframe
df = web.DataReader('TSLA','yahoo', start, end)
#se puede ver el valor
print(df.head())
#podemos guardar para cada ticker los diferentes valores
df.to_csv('tsla.csv')
#leer del csv
df = pd.read_csv('tsla.csv')
columnas = df.columns

#moving average
df['100ma'] = df['Adj Close'].rolling(window=100).mean()
print(df.tail())

#metodo 'resample' coge frecuencias de periodo que se le indique agrupando
#necesita una funcion de agregacion como la suma o 'ohlc' que calcula minimos y maximos cada 10 dias
df_ohlc = df['Adj Close'].resample('10D').ohlc()
df_volume = df['Volume'].resample('10D').sum()
