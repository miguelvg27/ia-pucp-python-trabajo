import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
import geopandas as gpd
from ipyleaflet import Map, GeoJSON, Marker, MarkerCluster

@st.cache_data
def cargar_df():
    df = pd.read_csv('./data/Consolidado-Monitoreo-Miraflores-QAIRA-1.csv', na_values='')
    df['Fecha'] = pd.to_datetime(df['Fecha'], format='%d/%m/%Y %H:%M')
    return df

#@st.cache_data() 
def get_data():
    df_raw = gpd.read_file('./data/peru_distrital_simple.geojson')
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

# Cargar el GeoJSON del distrito de Miraflores

#geojson_path = './data/peru_distrital_simple.geojson'
#miraflores_geojson = gpd.read_file(geojson_path)

# Agregar el GeoJSON del distrito de Miraflores al mapa
geojson_layer = GeoJSON(data=dr_raw.__geo_interface__)
m.add_layer(geojson_layer)

# Crear un grupo de marcadores
#marker_cluster = MarkerCluster()

st.map(m)

#latitud_promedio = df_filtrado['Latitud'].mean()
#longitud_promedio = df_filtrado['Longitud'].mean()
#st.map(df_filtrado, zoom=12, center=(latitud_promedio, longitud_promedio)) 

