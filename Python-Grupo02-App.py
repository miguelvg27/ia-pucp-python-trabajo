import streamlit as st
import pandas as pd
import numpy as np

@st.cache_data
def cargar_df():
    df = pd.read_csv('./data/Consolidado-Monitoreo-Miraflores-QAIRA-1.csv', na_values='')
    return df
	
df = cargar_df()
st.write(df)