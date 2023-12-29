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
    
    df_hist['state'] = df_hist['daychange'].apply(determine_state)    
    change_index_list,color_list = state_change(df_hist['state'])
    ymax = max(df_hist['Close'])
    ymin = min(df_hist['Close'])
        
    graph = st.container(border=True)
    plotcolor = 'dimgrey'
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10,5))
    ax.plot(df_hist['Date_timestamp'],df_hist['Close'],label="Historical",color=plotcolor,linewidth=0.8)
    ax.plot([df_hist['Date_timestamp'].iloc[0], df_datetime['Date'].iloc[-1]],
            [df_hist['Close'].iloc[0],df_hist['Close'].iloc[0]],color='black', linestyle='dotted',label='Day Open Rate')

    if forex_pair[0:6] == "EURUSD" and pred_toggle:
        df_predict = pd.concat([df_hist.iloc[-2:], df_predict]).reset_index(drop=True)
        ax.plot(df_predict['Date_timestamp'],df_predict['Close'],label="Prediction",color='red',linewidth=2.5)

        df_predict['daychange'] = df_predict['Close'] - df_hist['Close'].iloc[0]
        df_predict['state'] = df_predict['daychange'].apply(determine_state)    
        pred_change_index,pred_color = state_change(df_predict['state'])
        del pred_change_index[0] # remove first index so that no overlap

        pred_new_index = []
        for r in pred_change_index:
            date_index = df_datetime['Date'][df_datetime['Date'] == df_predict['Date_timestamp'].iloc[r]].index.values[0]
            pred_new_index.append(date_index)
        change_index_list = change_index_list + pred_new_index
        color_list = color_list + pred_color
        ymax_temp = max(df_predict['Close'])
        ymin_temp = min(df_predict['Close'])
        if ymax_temp > ymax: ymax = ymax_temp
        if ymin_temp < ymin: ymin = ymin_temp

    y_max = ymax + ymax*0.0005
    y_min = ymin - ymin*0.0005

    #draw box
    for q in range(len(change_index_list)-1):
        x_min = df_datetime['Date'].iloc[change_index_list[q]]
        x_max = df_datetime['Date'].iloc[change_index_list[q+1]]
        graph_color = color_list[q] 
        x_box = [x_min, x_min, x_max, x_max] 
        y_box = [y_min,y_max,y_max,y_min]

        # plt.plot(x_box, y_box , 'red', linewidth=1.5)
        plt.fill(x_box, y_box,color=graph_color, alpha=0.2,edgecolor='none')


    ax.set(xlabel='EET Time')  
    ax.set(ylabel='Exchange Rate') 
    plottitle = forex_pair[0:6] + ' Latest Exchange Rate'
    ax.set_title(plottitle)
    ax.set_ylim(y_min,y_max) 
    ax.set_xlim(df_hist['Date_timestamp'].iloc[0], df_datetime['Date'].iloc[-1]) 
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
    ax.legend()
    graph.pyplot(fig)



@st.cache_data
def prediction_table(df_prediction):
    table = st.container(border=True)
    table.title("Prediction")

    df2 = df_prediction
    df2['Date'] = df2['Date'].str.slice(11,16)
    df2['Close'] = df2['Close'].round(5)

    if pred_toggle:
        table.write("This is the trend prediction for the next 30 minutes.")
        df2_set1 = df2[['Date','Close']][0:10]
        df2_set2 = df2[['Date','Close']][10:20]
        df2_set3 = df2[['Date','Close']][20:30]
        
        table.write(df2_set1.T)
        table.write(df2_set2.T)
        table.write(df2_set3.T)
    else:
        table.write("Prediction function turned off")
        df2['Close NULL'] = '-'

        df2_set1 = df2[['Date','Close NULL']][0:10]
        df2_set2 = df2[['Date','Close NULL']][10:20]
        df2_set3 = df2[['Date','Close NULL']][20:30]
        
        table.write(df2_set1.T)
        table.write(df2_set2.T)
        table.write(df2_set3.T)



         
@st.cache_data
def datetime_list(str_date):
    df_fulldate = pd.DataFrame()
    df_fulldate['Date'] = pd.date_range(str_date, periods=1440, freq="T")
    return df_fulldate

def determine_state(col):
    if col >= 0:
        return True
    else:
        return False
    
def state_change(dataframe):
    change_index = []
    color = []
    change_index.append(0)
    if dataframe.iloc[0] == True: 
        color.append('green')
    else:
        color.append('red')

    for p in range(1,len(dataframe)):
        if dataframe.iloc[p] != dataframe.iloc[p - 1]:
            change_index.append(p) 
            if dataframe.iloc[p] == True: 
                color.append('green')
            else:
                color.append('red')
    change_index.append(len(dataframe)-1)
    return change_index, color

# --------------------------------------------------------------------------------------------------------------------

placeholder = st.empty()
placeholder.title('Forex Rate')

st.write("Hello! Welcome to Forex Rate Prediction page!")

st.write("According to Triennial Central Bank Survey conducted by Bank for International Settlements (2022), "
         "US dollar is still the world's dominant currency. 88.5% of all trades in April 2022 involve **US dollar**, "
         "followed by **Euro** (30.5%), **Japanese Yen** (16.7%) and **Great Britain Pound** (12.9%).")

st.write("**Prediction not available.")

st.sidebar.title('Forex Rate Prediction')
pred_toggle = st.sidebar.toggle("Enable Prediction",key='pred')

EURUSD, GBPUSD, USDJPY = st.tabs(["EURUSD", "GBPUSD**", "USDJPY**"])
with EURUSD:
    forex_pair = "EURUSD"    
    
    plotcolor = 'royalblue'
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

    pred_file = forex_pair[0:6] + "_prediction.txt"
    df_pred = pd.read_csv(pred_file, delimiter=',', index_col=False)
    df_pred['Date_timestamp'] = pd.to_datetime(df_pred['Date'])

    if pred_toggle: 
        plot_graph(df,df_pred)      
        prediction_table(df_pred)
    else:
        plot_graph(df)
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




