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
hora_seleccionada = st.sidebar.slider("Selecciona la hora", min_value=0, max_value=23, step=1, value=12)


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

#df_miraflores = df[(df['Estación de monitoreo'] == estacion) & 
 #                (df['PM2.5 (ug/m3)']) & 
  #               (df['CO (ug/m3)'])]

df_miraflores = df[(df['Estación de monitoreo'] == estacion)][['Estación de monitoreo','Latitud','Longitud', 'PM2.5 (ug/m3)', 'CO (ug/m3)', 'NO2 (ug/m3)', 'O3 (ug/m3)','Fecha']]
df_miraflores['Hora'] = df_miraflores['Fecha'].dt.hour

df_miraflores_hora = df[(df['Estación de monitoreo'] == estacion) & (df['Fecha'].dt.hour == hora_seleccionada)]

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



#Dataset
st.write(df_miraflores) 

fecha_inicio = fecha_seleccionada[0].strftime("%d/%m/%Y")
fecha_fin = fecha_seleccionada[1].strftime("%d/%m/%Y")


# Mapa automatico que cambia con el Slide de contaminantes y Estacion
#Grafico 7
st.subheader(f'Mapa interactivo de emisiones de {contaminante} en {estacion} a las {hora_seleccionada} horas en las fechas desde {fecha_inicio} hasta {fecha_fin}')
st.map(df_miraflores_hora,
    latitude='Latitud',
    longitude='Longitud',
    color = "#3333FF",
    size = 200,
       zoom =12,
    use_container_width=True)

# Mapa manual
#Grafico 8
#Ovalo Manuel Bonilla
mi_latitud1 = -12.109997654778994
mi_longitud1 = -77.0528653

#Ovalo Miraflores
mi_latitud2 = -12.119238450116725
mi_longitud2 = -77.02906493158211

num_repeticiones = 1000
latitudes = [mi_latitud1, mi_latitud2] * (num_repeticiones // 2)
longitudes = [mi_longitud1, mi_longitud2] * (num_repeticiones // 2)

df5 = pd.DataFrame({
    "col11": latitudes,
    "col22": longitudes,
    "col33": np.random.randn(num_repeticiones) * 100,
    "col44": np.random.rand(num_repeticiones, 4).tolist(),
})
st.subheader('Latitud y Longitud de estaciones de los contaminantes en Miraflores')
st.map(df5,
    latitude='col11',
    longitude='col22',
    size='col33',
    color='col44')







