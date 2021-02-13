# se reabren los modelos guardados en formato pickle como objetos serializados
# se pueden volver a abrir para ejecutar sobre otro scirpt y pasarle datos nuevos
# evitar volver a reentrenar y procesar los datos nuevo 
import pandas as pd
import yfinance as yf
from datos_y_funciones.naragon_ml_model_functions import *

#para utilizar agumentos desde fuera
import sys 
#primero se comprueba si se pasan argumentos, si no se cogen por defecto los del else
if len(sys.argv) > 1:
	ticker = sys.argv[1]
	dias_diferencia = int(sys.argv[2])
	model_type = sys.argv[3]
else:
	ticker = 'IDR.MC'
	#dias de diferencia desde el dia en curso para leer
	dias_diferencia = 3
	#modelo
	model_type = 'regresion_lineal_simple'

#las fechas del dia en curso (end) menos el parametro dias_diferencia
end, start = get_current_date_minus_n_day_difference(dias_diferencia)

#parametros para nueva inferencia
data_pred_dir = 'datos_y_funciones/predicted_data'
ticker_simple = ticker.replace('.MC','')

#datos de fechas de entrenamiento
fechas_train = '200001_201812'
#nombre de la carpeta donde esta el pickle
model_pickle_file = 'modelos_desarrollados'
#nombre del objeto pickle - tiene las fechas de los datos con los que se ha entrenado
model_pickle_name = '{}_{}_{}'.format(ticker_simple, model_type, fechas_train)
#nombre del objeto de resultados de la prediccion - se le pone la fecha fin de los datos
model_result_name = '{}_{}_{}'.format(ticker, model_type, end)

#leemos nuevos datos de Yfinance para predecir
df = yf.download(ticker, start=start, end=end)
#se toma solo la columan Adj Close
df_close = get_adj_close_col(df)
#transformarmos el dataframe de origen en un array numpy para predecir con el modelo
x_test = df_close.to_numpy()

#abrimos los modelos guardados en formato pickle
restored_model = open_model_in_pickle_object(model_pickle_file + '/' +model_pickle_name)
#con los nuevos datos se realizan predicciones con el modelo reabierto
y_pred = modelo_predict_new_data(restored_model, x_test)

#guardamos los resultados en un fichero csv
join_test_df_with_pred_array_to_csv(y_pred, df_close, ticker, data_pred_dir, model_result_name)

