# %%
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import pandas as pd
import os
from IPython.display import display  # Importa la función display para mejorar visualizacion

# Ruta al archivo Excel (ajusta la ruta según tu sistema)
ruta_archivo = "C:/Users/ASUS/OneDrive/Proyectos POWER BI/Dofus Unity/ConsolidadoInicial_BolsaKamas_Dofus.xlsx" # Windows

# Leer datos existentes
df_existente = pd.read_excel(ruta_archivo, engine="openpyxl")
#print(f"Número de datos existentes: {len(df_existente)}")  #len: Cuenta las filas

# URL y headers
url = "https://www.dofus.com/es/compra-kamas/cotizacion-kama-ogrinas"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Obtener datos de la web
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

# Extraer datos de RATES del JavaScript
for script in soup.find_all('script'):
    if script.string and 'RATES' in script.string:
        rates_line = script.string.strip().split('\n')[0]
        rates_json = rates_line.split('RATES = ')[1].rstrip(';')
        rates_data = json.loads(rates_json)
        break

# Crear DataFrame con nuevos datos
df_nuevos = pd.DataFrame([
    {'Fecha': datetime.fromtimestamp(int(ts)/1000), 'Tasa': rate}
    for ts, rate in rates_data.items()
    if ts != 'avg' and rate is not None
])
df_nuevos = df_nuevos.sort_values('Fecha')

# Filtrar df_B para excluir IDs presentes en df_A
df_nuevos_filtrado = df_nuevos[~df_nuevos["Fecha"].isin(df_existente["Fecha"])]
#print(f"Número de datos nuevos: {len(df_nuevos_filtrado)}")

# Combinar datos y eliminar duplicados
df_combined = pd.concat([df_existente, df_nuevos_filtrado])
df_combined = df_combined.drop_duplicates(subset=['Fecha'])
df_combined = df_combined.sort_values('Fecha')

# Guardar actualización
df_combined.to_excel(ruta_archivo, engine="openpyxl", index=False)
#display(df_combined.head(10))

# %%


# %%



