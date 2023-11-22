import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

@st.cache_data
def cargar_df():
    df = pd.read_csv('./data/Consolidado-Monitoreo-Miraflores-QAIRA-1.csv', na_values='')
    df['Fecha'] = pd.to_datetime(df['Fecha'], format='%d/%m/%Y %H:%M')
    return df

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
    value=(pd.to_datetime('2021-06-01').date(), pd.to_datetime('2021-06-30').date())
)


# Filtrar los datos
df_filtrado = df[(df['Estación de monitoreo'] == estacion) & 
                 (df['Fecha'].dt.date >= fecha_seleccionada[0]) & 
                 (df['Fecha'].dt.date <= fecha_seleccionada[1])]

# Crear el gráfico
plt.figure(figsize=(10, 6))
sns.lineplot(data=df_filtrado, x='Fecha', y=contaminante)
plt.xticks(rotation=45)
plt.title(f'Concentración de {contaminante} en {estacion} a lo Largo del Tiempo')
st.pyplot(plt)

st.write(df_filtrado)