import streamlit as st
import pandas as pd
import numpy as np
from datetime import time
appointment = st.slider(
"Programe la asesoria:",
value=(time(11, 30), time(12, 45)))
st.write("Esta agendado para:", appointment)