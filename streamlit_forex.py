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

# define functions

@st.cache_data
def plot_graph(df,df_pred=pd.DataFrame()):
         fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(15,8))
         ax.plot(df['Date_timestamp'],df['Close'],label="Historical",color=plotcolor) # marker='x' marker='.'

         if radio_forex == "EURUSD":
                  df_pred = pd.concat([df.iloc[-1], df_pred]).reset_index(drop=True)
                  ax.plot(df_pred['Date_timestamp'],df_pred['Close'],label="Prediction",color='red',linewidth=2.5)
         
         ax.set(xlabel='Time')  
         ax.set(ylabel='Exchange Rate') 
         plottitle = radio_forex[0:6] + 'Latest Exchange Rate'
         ax.set_title(plottitle)
         ax.set_xlim(df['Date_timestamp'].iloc[0], df_datetime['Date'].iloc[-1]) 
         ax.legend()
         st.pyplot(fig)


@st.cache_data
def prediction_table(df):
         df['Date'] = df['Date'].str.slice(0, 10)
         df = df.drop(['Date_timestamp'])
         st.write(df.T)

         
@st.cache_data
def datetime_list(str_date):
         df = pd.DataFrame()
         df['Date'] = pd.date_range(str_date, periods=1440, freq="T")
         return df

st.title('Forex Pair Graphs')

st.sidebar.title("Forex Pair")
radio_forex = st.sidebar.radio("Pick the interested forex pair.", ["EURUSD", "GBPUSD**", "USDJPY**"], key='forex')
st.sidebar.write("** Prediction not available.")

st.write("Hello! Welcome to Forex Prediction page!")

if radio_forex == "EURUSD":
         st.write("this is EURUSD")
         hist_file = radio_forex[0:6] + "_historical.txt"
         plotcolor = 'royalblue'

         pred_file = radio_forex[0:6] + "_prediction.txt"
         df_pred = pd.read_csv(pred_file, delimiter=',', index_col=False)
         df_pred['Date_timestamp'] = pd.to_datetime(df_pred['Date'])


elif radio_forex == "GBPUSD**":
         st.write("this is GBPUSD")
         # hist_file = radio_forex[0:6] + "_historical.txt"
         plotcolor = 'salmon'
         
elif radio_forex == "USDJPY**":
         st.write("this is USDJPY")
         # hist_file = radio_forex[0:6] + "_historical.txt"
         plotcolor = 'forestgreen'

hist_file = radio_forex[0:6] + "_historical.txt"
df = pd.read_csv(hist_file, delimiter=',', index_col=False)
df['Date_timestamp'] = pd.to_datetime(df['Date'])

# Prepare for plot
str_datetime = df['Date'].iloc[0]
str_date = str_datetime[0:10]

df_datetime = datetime_list(str_date)
if radio_forex == "EURUSD":
         plot_graph(df,df_pred)
         prediction_table(df_pred)
else:
         plot_graph(df)






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



