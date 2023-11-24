import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
#import plotly.express as px
#import subprocess

#subprocess.run(["pip", "install", "pandas", "folium", "streamlit_folium", "geopandas", "ipyleaflet", "Map", "GeoJSON", "Marker", "MarkerCluster"])
#import folium
#from streamlit_folium import folium_static
#import geopandas as gpd
#from ipyleaflet import Map, GeoJSON, Marker, MarkerCluster

@st.cache_data
def cargar_df():
    df = pd.read_csv('./data/Consolidado-Monitoreo-Miraflores-QAIRA-1.csv', na_values='')
    df['Fecha'] = pd.to_datetime(df['Fecha'], format='%d/%m/%Y %H:%M')
    return df

#@st.cache_data() 
def get_data():
    df_raw = geopandas.read_file('./data/peru_distrital_simple.geojson')
    df_raw = df_raw[df_raw.Start_bouw!=0]
    return df_raw

st.title('Calidad de aire en Miraflores')
st.write('Realiza tus consultas y descarga la información')

df = cargar_df()
# Determina el rango mínimo y máximo de fechas
fecha_min = df['Fecha'].min().date()
fecha_max = df['Fecha'].max().date()

# Sidebar para filtros
st.sidebar.header('Filtros')
estacion = st.sidebar.selectbox(
    'Elige una Estación de Monitoreo:', 
	df['Estación de monitoreo'].unique(),
	index=1
)
contaminante = st.sidebar.selectbox(
	'Elige un Contaminante:', 
	['PM2.5 (ug/m3)', 'CO (ug/m3)', 'NO2 (ug/m3)', 'O3 (ug/m3)'],
	index=2
)
fecha_seleccionada = st.sidebar.slider(
    'Selecciona un rango de fechas:',
    min_value=fecha_min,
    max_value=fecha_max,
    value=(pd.to_datetime('2020-11-01').date(), pd.to_datetime('2020-11-30').date())
)


# Filtrar los datos
df_filtrado = df[(df['Estación de monitoreo'] == estacion) & 
                 (df['Fecha'].dt.date >= fecha_seleccionada[0]) & 
                 (df['Fecha'].dt.date <= fecha_seleccionada[1])]

# Añadir columna de hora
df_filtrado['Fecha'] = pd.to_datetime(df_filtrado['Fecha'])
df_filtrado['Hora'] = df_filtrado['Fecha'].dt.hour

#Crear una DataFrame por media de hora
df_hora = df_filtrado.groupby(['Hora'])[contaminante].mean()
df_hora = df_hora.reset_index()

#Crear una DataFrame por Temperatura
df_temperatura = df_filtrado.groupby(['Temperatura (C)'])[contaminante].mean()
df_temperatura = df_temperatura.reset_index()

#Crear una DataFrame por Humedad
df_humedad = df_filtrado.groupby(['Hora'])['Humedad (%)'].mean()
df_humedad = df_humedad.reset_index()

#Crear una DataFrame del Ruido Promedio por hora
df_hora_Ruido = df_filtrado.groupby(['Hora'])['Ruido (dB)'].mean().reset_index()

df_miraflores = df_filtrado.groupby(['Estación de Monitoreo'])[contaminante].mean().reset_index()

# Crear el gráfico
plt.figure(figsize=(10, 6))
sns.lineplot(data=df_filtrado, x='Fecha', y=contaminante)
plt.xticks(rotation=45)
plt.title(f'Concentración de {contaminante} en {estacion} a lo Largo del Tiempo')
st.pyplot(plt)

# Gráfico 2
plt.figure(figsize=(10, 4))
sns.barplot(x='Hora', y=contaminante, data=df_hora, palette='plasma')
plt.title(f"Promedio por horas de emisiones de {contaminante} en {estacion}")
plt.xticks(rotation=0)
st.pyplot(plt)


st.write(df_filtrado) 

# Gráfico 3
plt.figure(figsize=(10, 4))
sns.barplot(x='Temperatura (C)', y=contaminante, data=df_temperatura, palette='plasma')
plt.title(f"Promedio de Temperatura de emisiones de {contaminante} en {estacion}")
plt.xticks(rotation=90)
st.pyplot(plt)


# Gráfico 4
plt.figure(figsize=(10, 4))
sns.barplot(x='Hora', y='Humedad (%)', data=df_humedad, palette='plasma')
plt.title(f"Promedio de Humedad en % por hora en {estacion}")
plt.xticks(rotation=90)
st.pyplot(plt)

# Gráfico 5
plt.figure(figsize=(10, 4))
sns.heatmap(df_filtrado[['Temperatura (C)', 'Humedad (%)']].corr(), annot=True)
plt.title(f"Correlación entre Humedad y Temperatura por  {estacion}")
plt.xticks(rotation=0)
st.pyplot(plt)

# Gráfico 6
plt.figure(figsize=(10, 4))
sns.lineplot(x="Hora", y="Ruido (dB)", marker='o', data=df_hora_Ruido, c='green')
plt.title(f"Ruido (dB) promedio por hora en {estacion}")
st.pyplot(plt)


df = pd.DataFrame(
     np.random.randn(1000, 2) / [1, 1] + [-12.0727, -77.0827],
     columns=['lat', 'lon'])

# Centro de las coordenadas
centro_lat = -12.0727
centro_lon = -77.0827

# Mostrar el mapa centrado en las coordenadas específicas
#st.map(df, lat=centro_lat, lon=centro_lon, zoom=12)

st.map(df)

import streamlit as st
import pandas as pd
import numpy as np

df2 = pd.DataFrame({
    "col1": np.random.randn(1000) / 50 + -12.0727,
    "col2": np.random.randn(1000) / 50 + -77.0827,
    "col3": np.random.randn(1000) * 100,
    "col4": np.random.rand(1000, 4).tolist(),
})

st.map(df2,
    latitude='col1',
    longitude='col2',
    size='col3',
    color='col4')

import streamlit as st
import pandas as pd
import numpy as np

import streamlit as st
import pandas as pd
import numpy as np

# Definir latitud y longitud específicas
mi_latitud = -12.0727
mi_longitud = -77.0827

# Crear un DataFrame con latitudes y longitudes específicas repetidas
num_repeticiones = 1000
latitudes = [mi_latitud] * num_repeticiones + list(np.random.randn(num_repeticiones) / 50 + mi_latitud)
longitudes = [mi_longitud] * num_repeticiones + list(np.random.randn(num_repeticiones) / 50 + mi_longitud)

df3 = pd.DataFrame({
    "col1": latitudes,
    "col2": longitudes,
    "col3": np.random.randn(2 * num_repeticiones) * 100,
    "col4": np.random.rand(2 * num_repeticiones, 4).tolist(),
})

# Añadir una columna 'contaminante' para demostración
df3['contaminante'] = np.random.randn(2 * num_repeticiones)

# Crear el mapa en Streamlit
st.map(df3,
    latitude='col1',
    longitude='col2',
    size='contaminante',
    color='col4')

st.write(df_miraflores) 

#st.map(df_miraflores, 
 #   latitude='Latitud', 
 #   longitude='Longitud',
  #  color=contaminante,  
   # cmap='viridis',
    #use_container_width=True  
#) 

import pandas as pd
import numpy as np
import streamlit as st

# Definir latitud y longitud específicas

#Ovalo Manuel Bonilla
mi_latitud = -12.119250414642934
mi_longitud = --77.0528653

#Ovalo Miraflores
mi_latitud = -12.119250414642934
mi_longitud = -77.02904771266907

# Crear un DataFrame con latitudes y longitudes específicas
num_repeticiones = 1000

df4 = pd.DataFrame({
    "col1": [mi_latitud] * num_repeticiones,
    "col2": [mi_longitud] * num_repeticiones,
    "col3": np.random.randn(num_repeticiones) * 100,
    "col4": np.random.rand(num_repeticiones, 4).tolist(),
})

# Añadir una columna 'contaminante' para demostración
df4['contaminante'] = np.random.randn(num_repeticiones)

# Crear el mapa en Streamlit
st.map(df4,
    latitude='col1',
    longitude='col2',
    size='contaminante',
    color='col4')

