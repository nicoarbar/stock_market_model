echo "ejecutando el script build_ml_models para modelo elegido"

set /p ticker="Nombre del ticker a analizar"
set /p dias_diferencia_dia_curso="Diferencia de dias con el dia en curso"
set /p modelo="Nombre del modelo a probar"

call "C:\\Users\naragon\Anaconda3\Scripts\activate.bat"

python build_ml_models.py %ticker% %dias_diferencia_dia_curso% %modelo%

timeout 20 


