#Modelo de Prediccion de valores de acciones de empresas cotizadas

Utilizo el modulo de Yfinance para descargar datos historicos de Yahoo Finance de cualquier ticker o empresa de cualquier mercado.

Por lo general, el dataset historico para el entrenamiento es de casi dos decadas, de 2000 hasta 2018.
En dos decadas los mercados han ido cambiando, han salido nuevas empresas y otras desaparecido. 

1.Entrenamiento de diferentes modelos con scikit-learn sobre como se moverá una empresa en función de como se mueve el resto.
2.Ajuste del modelo
3.Realizar predicciones diarias clasificando para cada empresa tres valores: comprar, vender, mantenerse
4. Sentiment Analysis de noticias diarias para predicciones sobre lo mismo
