# import libraries
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from github import Github
import pytz
import base64

import time
import warnings

# warnings.simplefilter('ignore')


# set condition for state 
if 'pred' not in st.session_state:
    st.session_state['pred'] = False


## define functions
# function to plot graphs on main page
@st.cache_data
def plot_graph(df_hist,df_predict_ori=pd.DataFrame(),check=st.session_state["pred"]):
    
    # df_hist['state'] = df_hist['daychange'].apply(determine_state)    
    # change_index_list,color_list = state_change(df_hist['state'])
 
    y_max = max(df_hist['Close'])
    y_min = min(df_hist['Close'])
        
    graph = st.container(border=True)
    plotcolor = 'dimgrey'
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10,5))
    ax.plot(df_hist['Date_timestamp'],df_hist['Close'],label="Historical",color=plotcolor,linewidth=0.8)
    ax.plot([df_hist['Date_timestamp'].iloc[0], df_datetime['Date'].iloc[-1]],
            [df_hist['Close'].iloc[0],df_hist['Close'].iloc[0]],color='black', linestyle='dotted',label='Day Open Rate')

    if forex_pair[0:6] == "EURUSD" and pred_toggle:

        # "Date" "ChangePercent_1m" "Close"        
        # ax.scatter(df_predict_ori['Date'], df_predict_ori['Close'], color='red', marker='x', s=5)
        ax.plot(df_predict_ori['Date'], df_predict_ori['Close'], color='purple', linewidth=0.8)


    ax.set(xlabel='Coordinated Universal Time, UTC')  
    ax.set(ylabel='Exchange Rate') 
    plottitle = forex_pair[0:6] + ' Latest Exchange Rate'
    ax.set_title(plottitle)
    ax.set_ylim(y_min,y_max) 
    ax.set_xlim(df_hist['Date_timestamp'].iloc[0], df_datetime['Date'].iloc[-1]) 
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
    ax.legend()
    graph.pyplot(fig)

    last_tick = df_hist['Date_timestamp'].iloc[-1]
    last_done_price = df_hist['Close'].iloc[-1]
    last_tick_text = "Last updated at " + "**" + str(last_tick) + "**, close rate is " + "**" + str(last_done_price) + "**." 
    graph.write(last_tick_text)

    # last_done_text = "Previous minute's close rate is " + "**" + str(last_done_price) + "**." 
    # graph.write(last_done_text)


# function to create list of time throughout the day based on period (1 min = 1440 data points)
@st.cache_data
def datetime_list(str_date):
    df_fulldate = pd.DataFrame()
    period = 1
    frequency = str(period) + "T"
    df_fulldate['Date'] = pd.date_range(str_date, periods=1440/period, freq=frequency)
    return df_fulldate

def determine_state(col):
    if col >= 0:
        return True
    else:
        return False

# function to determine the color of the graph
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
# start defining the page here
st.set_page_config(layout="wide")

st.title('Forex Rate Prediction')
st.write("Hello! Welcome to Forex Rate Prediction page!")

st.write("According to Triennial Central Bank Survey conducted by Bank for International Settlements (2022), "
         "US dollar is still the world's dominant currency. 88.5% of all trades in April 2022 involve **US dollar**, "
         "followed by **Euro** (30.5%), **Japanese Yen** (16.7%) and **Great Britain Pound** (12.9%).")

st.write("**Prediction not available.")

# col1, col2 = st.columns([4,2], gap="medium")
# col2.title('Learning Materials')
# # forex market
# col2.video('https://www.youtube.com/watch?v=ig_EO805rpA') 
# # mitigate risk forex
# col2.video('https://www.youtube.com/watch?v=Bj7j3iD8bow') 
# # george soros and pound
# col2.video('https://www.youtube.com/watch?v=KVBuUYXsSRM') 


# col1.title('Forex Rate Prediction')
# col1.write("Hello! Welcome to Forex Rate Prediction page!")

# col1.write("According to Triennial Central Bank Survey conducted by Bank for International Settlements (2022), "
#          "US dollar is still the world's dominant currency. 88.5% of all trades in April 2022 involve **US dollar**, "
#          "followed by **Euro** (30.5%), **Japanese Yen** (16.7%) and **Great Britain Pound** (12.9%).")

# col1.write("**Prediction not available.")

st.sidebar.title('Forex Rate Prediction')
pred_toggle = st.sidebar.toggle("Enable Prediction",key='pred')
for space in range(17):
    st.sidebar.write(" ")

st.sidebar.write("Creator: Wee Hin Sheik")
st.sidebar.write("Email: hswee92@gmail.com")

st.sidebar.markdown( 
    """<a href="https://www.github.com/hswee92/ForexPrediction/">
    <img src="data:image/png;base64,{}" width="150">
    </a>""".format(
        base64.b64encode(open("GitHub logo.png", "rb").read()).decode()
    ),
    unsafe_allow_html=True,
)

st.sidebar.markdown( 
    """<a href="https://www.linkedin.com/in/hin-sheik-wee-9855704b/">
    <img src="data:image/png;base64,{}" width="150">
    </a>""".format(
        base64.b64encode(open("Linkedin-Logo.png", "rb").read()).decode()
    ),
    unsafe_allow_html=True,
)


## main program here!
EURUSD, USDJPY, GBPUSD = st.tabs(["EURUSD", "USDJPY**", "GBPUSD**"])
with EURUSD:
    forex_pair = "EURUSD"    
    
    # plotcolor = 'royalblue'
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
        # prediction_table(df_pred)
    else:
        plot_graph(df)
        # prediction_table(df_pred)


with USDJPY:
    forex_pair = "USDJPY"

    # plotcolor = 'forestgreen'
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
    # plot_graph(df)   

    
with GBPUSD:
    forex_pair = "GBPUSD"

    # plotcolor = 'salmon'
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


# container for information below
container = st.container(border=True)

MT4_timezone = pytz.timezone('UTC') 
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

