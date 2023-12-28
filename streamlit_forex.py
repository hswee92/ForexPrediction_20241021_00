# import libraries
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import requests
from github import Github

import time
import warnings

# warnings.simplefilter('ignore')

initial_state = 0
st.title('Forex Pair Graphs')

st.sidebar.title("Forex Pair")
radio_forex = st.sidebar.radio("Pick the interested forex pair.", ["EURUSD", "GBPUSD**", "USDJPY**"], key='forex')
st.sidebar.write("** Prediction not available.")

st.write("Hello! Welcome to Forex Prediction page!")

if radio_forex == "EURUSD":
         st.write("this is EURUSD")
         hist_file = radio_forex[0:6] + "_historical.txt"
         plotcolor = 'royalblue'

elif radio_forex == "GBPUSD**":
         st.write("this is GBPUSD")
         # hist_file = radio_forex[0:6] + "_historical.txt"
         plotcolor = 'salmon'
         
elif radio_forex == "USDJPY**":
         st.write("this is USDJPY")
         # hist_file = radio_forex[0:6] + "_historical.txt"
         plotcolor = 'forestgreen'

hist_file = radio_forex[0:6] + "_historical.txt"
path = "./" + hist_file
df = pd.read_csv(hist_file, delimiter=',', index_col=False)

# Prepare for plot
str_datetime = df['Date'].iloc[0]
str_date = str_datetime[0:10].replace('-', '.')
st.write(str_date)

df_datetime = pd.DataFrame()
df_datetime['Date'] = pd.date_range(str_date, periods=1440, freq="T")


# Plot
@st.cache_data
def plot_graph(df):
         fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(25,15))
         ax.plot(df['Date'],df['Close'],label="silhouette score",color=plotcolor) # marker='x' marker='.'
         ax.set(xlabel='Time')  
         ax.set(ylabel='Exchange Rate') 
         plottitle = radio_forex[0:6] + 'Latest Exchange Rate'
         ax.set_title(plottitle)
         
         ax.set_xlim(df['Date'].iloc[0], df_datetime['Date'].iloc[-1]) 
         st.pyplot(fig)

plot_graph(df)

st.table(df)





now = datetime.now()
current_time = now.strftime("%H:%M:%S")
cur_time = "Current Time = " + current_time
st.write(cur_time)


st.write("**:red[Disclaimer: Trading involves risk. \n"
         "As a general rule, you should only trade in financial products that "
         "you are familiar with and understand the risk associated with them. \n"
         "Trade at your own risk.]**")

st.write("st.session_state")
st.session_state

time.sleep(5)
st.rerun()

         
# path = "https://raw.githubusercontent.com/hswee92/ForexPrediction/main/" + hist_file
# st.write(path)
# response = requests.get(path)
# df = pd.read_csv(path, delimiter=',', index_col=False)
# st.table(df)



