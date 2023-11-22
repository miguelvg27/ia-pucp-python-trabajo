import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

@st.cache_data
def cargar_df():
    df = pd.read_csv('./data/Consolidado-Monitoreo-Miraflores-QAIRA-1.csv', na_values='')
	df['Fecha'] = pd.to_datetime(df['Fecha'])
    return df
	
df = cargar_df()

# Sidebar para filtros
st.sidebar.header('Filtros')
estacion = st.sidebar.selectbox('Elige una Estación de Monitoreo:', df['Estación de monitoreo'].unique())
contaminante = st.sidebar.selectbox('Elige un Contaminante:', ['PM2.5 (ug/m3)', 'CO (ug/m3)', 'NO2 (ug/m3)', 'O3 (ug/m3)'])

# Filtrar los datos
df_filtrado = df[df['Estación de monitoreo'] == estacion]

# Crear el gráfico
plt.figure(figsize=(10, 6))
sns.lineplot(data=df_filtrado, x='Fecha', y=contaminante)
plt.xticks(rotation=45)
plt.title(f'Concentración de {contaminante} en {estacion} a lo Largo del Tiempo')
st.pyplot(plt)

st.write(df_filtrado)