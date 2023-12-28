# import libraries
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from github import Github
import pytz

import time
import warnings

# warnings.simplefilter('ignore')

# define functions

@st.cache_data
def plot_graph(df_hist,df_predict=pd.DataFrame()):
    
    # identify index that change state
    # for i in range(1, len(df)):
    #     if df['state'].iloc[i] != df['state'].iloc[i - 1]:
    #     change_indices.append(i)
    

    # get day change
    # get boolean of positive or negative
    # get change indices


    def find_state_changes(dataframe):
    change_indices=""
    for i in range(1, len(data)):
        if data.iloc[i] != data.iloc[i - 1]:
            change_indices.append(i)
    return change_indices

    # Use apply() along the column 'state' to find state changes
    change_indices = df_hist['state'].apply(lambda x: find_state_changes(df_hist['state']))

    graph.write(change_indices)
    
    
    
    graph = st.container(border=True)
    
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10,5))
    ax.plot(df_hist['Date_timestamp'],df_hist['Close'],label="Historical",color=plotcolor) # marker='x' marker='.'
    ax.plot([df_hist['Date_timestamp'].iloc[0], df_datetime['Date'].iloc[-1]],
            [df_hist['Close'].iloc[0],df_hist['Close'].iloc[0]],color='black', linestyle='dotted')

    if forex_pair[0:6] == "EURUSD":
        df_predict = pd.concat([df_hist.iloc[-2:], df_predict]).reset_index(drop=True)
        ax.plot(df_predict['Date_timestamp'],df_predict['Close'],label="Prediction",color='red',linewidth=2.5)

    ax.set(xlabel='EET Time')  
    ax.set(ylabel='Exchange Rate') 
    plottitle = forex_pair[0:6] + ' Latest Exchange Rate'
    ax.set_title(plottitle)
    ax.set_xlim(df_hist['Date_timestamp'].iloc[0], df_datetime['Date'].iloc[-1]) 
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
    ax.legend()
    graph.pyplot(fig)



@st.cache_data
def prediction_table(df_prediction):
    table = st.container(border=True)
    table.write("This is the trend prediction for the next 30 minutes.")

    df2 = df_prediction
    df2['Date'] = df2['Date'].str.slice(11,16)
    df2['Close'] = df2['Close'].round(5)
    df2_set1 = df2[['Date','Close']][0:10]
    df2_set2 = df2[['Date','Close']][10:20]
    df2_set3 = df2[['Date','Close']][20:30]

    table.write(df2_set1.T)
    table.write(df2_set2.T)
    table.write(df2_set3.T)


         
@st.cache_data
def datetime_list(str_date):
    df_fulldate = pd.DataFrame()
    df_fulldate['Date'] = pd.date_range(str_date, periods=1440, freq="T")
    return df_fulldate



placeholder = st.empty()
placeholder.title('Forex Pair')

st.write("Hello! Welcome to Forex Prediction page!")

st.write("According to Triennial Central Bank Survey conducted by Bank for International Settlements (2022), "
         "US dollar is still the world's dominant currency. 88.5% of all trades in April 2022 involve **US dollar**, "
         "followed by **Euro** (30.5%), **Japanese Yen** (16.7%) and **Great Britain Pound** (12.9%).")

st.write("**Prediction not available.")


EURUSD, GBPUSD, USDJPY = st.tabs(["EURUSD", "GBPUSD**", "USDJPY**"])
with EURUSD:
    forex_pair = "EURUSD"    
    
    plotcolor = 'royalblue'
    pred_file = forex_pair[0:6] + "_prediction.txt"
    df_pred = pd.read_csv(pred_file, delimiter=',', index_col=False)
    df_pred['Date_timestamp'] = pd.to_datetime(df_pred['Date'])

    hist_file = forex_pair[0:6] + "_historical.txt"
    df = pd.read_csv(hist_file, delimiter=',', index_col=False)
    df['Date_timestamp'] = pd.to_datetime(df['Date'])

    # Prepare for plot
    str_datetime = df['Date'].iloc[0]
    str_date = str_datetime[0:10]

    df_datetime = datetime_list(str_date)

    st.write("EURUSD pair is the **MOST** traded currency pair. \n"
             "In April 2022, EURUSD makes up 22.7% of total trades.")
    st.write("This is the today's graph (" + str_date + ") for " + forex_pair[0:6] + ".")
    plot_graph(df,df_pred)
    prediction_table(df_pred)


with GBPUSD:
    forex_pair = "GBPUSD"

    plotcolor = 'salmon'
    hist_file = forex_pair[0:6] + "_historical.txt"
    df = pd.read_csv(hist_file, delimiter=',', index_col=False)
    df['Date_timestamp'] = pd.to_datetime(df['Date'])

    # Prepare for plot
    str_datetime = df['Date'].iloc[0]
    str_date = str_datetime[0:10]

    df_datetime = datetime_list(str_date)

    st.write("GBPUSD pair is the **THIRD** most traded currency pair. \n"
             "In April 2022, GBPUSD makes up 9.6% of total trades.")
    st.write("This is the today's graph (" + str_date + ") for " + forex_pair[0:6] + ".")
    plot_graph(df)


with USDJPY:
    forex_pair = "USDJPY"

    plotcolor = 'forestgreen'
    hist_file = forex_pair[0:6] + "_historical.txt"
    df = pd.read_csv(hist_file, delimiter=',', index_col=False)
    df['Date_timestamp'] = pd.to_datetime(df['Date'])

    # Prepare for plot
    str_datetime = df['Date'].iloc[0]
    str_date = str_datetime[0:10]

    df_datetime = datetime_list(str_date)

    st.write("USDJPY pair is the **SECOND** most traded currency pair. \n"
             "In April 2022, USDJPY makes up 13.2% of total trades.")
    st.write("This is the today's graph (" + str_date + ") for " + forex_pair[0:6] + ".")
    plot_graph(df)



# container for information below
container = st.container(border=True)

MT4_timezone = pytz.timezone('EET') 
MT4_now = datetime.now(MT4_timezone)
str_MT4 = MT4_now.strftime("%d-%m-%Y %H:%M:%S")
container.write("**Server time:** " + str_MT4)

local_timezone = pytz.timezone('Asia/Kuala_Lumpur') 
local_now = datetime.now(local_timezone)
str_local = local_now.strftime("%d-%m-%Y %H:%M:%S")
container.write("**Malaysia time:** "+  str_local)

container.write("**:red[Disclaimer: Trading involves risk. \n"
                "As a general rule, you should only trade in financial products that "
                "you are familiar with and understand the risk associated with them. \n"
                "Trade at your own risk.]**")

# st.write("st.session_state")
# st.session_state

time.sleep(5)
st.rerun()




