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

# define functions

if 'pred' not in st.session_state:
    st.session_state['pred'] = False

@st.cache_data
def plot_graph(df_hist,df_predict_ori=pd.DataFrame(),check=st.session_state["pred"]):
    
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
        df_predict = pd.concat([df_hist.iloc[-2:], df_predict_ori]).reset_index(drop=True)
        df_predict_plot = pd.concat([df_hist.iloc[-2:], df_predict_ori.iloc[-2:]]).reset_index(drop=True)
        ax.plot(df_predict_plot['Date_timestamp'],df_predict_plot['Close'],label="Prediction",color='red',linewidth=2.5)

        df_predict['daychange'] = df_predict['Close'] - df_hist['Close'].iloc[0]
        df_predict['state'] = df_predict['daychange'].apply(determine_state)    
        pred_change_index,pred_color = state_change(df_predict['state'])
        del pred_change_index[0] # remove first index so that no overlap

        pred_new_index = []
        for r in pred_change_index:
            date_index = df_datetime['Date'][df_datetime['Date'] == df_predict['Date_timestamp'].iloc[r]].index.values[0]
            pred_new_index.append(int(date_index))
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

        plt.fill(x_box, y_box,color=graph_color, alpha=0.15,edgecolor='none')


    ax.set(xlabel='Eastern European Time')  
    ax.set(ylabel='Exchange Rate') 
    plottitle = forex_pair[0:6] + ' Latest Exchange Rate'
    ax.set_title(plottitle)
    ax.set_ylim(y_min,y_max) 
    ax.set_xlim(df_hist['Date_timestamp'].iloc[0], df_datetime['Date'].iloc[-1]) 
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
    ax.legend()
    graph.pyplot(fig)

    last_done_price = df_hist['Close'].iloc[-1]
    last_done_text = "Previous minute's close rate is " + "**" + str(last_done_price) + "**." 
    graph.write(last_done_text)


# @st.cache_data
def prediction_table(df_prediction, check=st.session_state["pred"]):
    table = st.container(border=True)
    table.title("Prediction")
  
    df2 = df_prediction
    df2['Date'] = df2['Date'].str.slice(11,16)
    df2['Close'] = df2['Close'].round(5)

    if pred_toggle:
        table.write("This is the trend prediction for the next 60 minutes.")
        df2_set1 = df2[['Date','Close']][0:10]
        df2_set2 = df2[['Date','Close']][10:20]
        df2_set3 = df2[['Date','Close']][20:30]
        df2_set4 = df2[['Date','Close']][30:40]
        df2_set5 = df2[['Date','Close']][40:50]
        df2_set6 = df2[['Date','Close']][50:60]
        # table.write(st.session_state["pred"])
        table.dataframe(df2_set1.T,width=660)
        table.dataframe(df2_set2.T,width=660)
        table.dataframe(df2_set3.T,width=660)
        table.dataframe(df2_set4.T,width=660)
        table.dataframe(df2_set5.T,width=660)
        table.dataframe(df2_set6.T,width=660)
    else:
        table.write("Prediction function turned off")
        df2['Close'] = '-'

        df2_set1 = df2[['Date','Close']][0:10]
        df2_set2 = df2[['Date','Close']][10:20]
        df2_set3 = df2[['Date','Close']][20:30]
        df2_set4 = df2[['Date','Close']][30:40]
        df2_set5 = df2[['Date','Close']][40:50]
        df2_set6 = df2[['Date','Close']][50:60]

        # table.write(st.session_state["pred"])
        table.dataframe(df2_set1.T,width=660)
        table.dataframe(df2_set2.T,width=660)
        table.dataframe(df2_set3.T,width=660)
        table.dataframe(df2_set4.T,width=660)
        table.dataframe(df2_set5.T,width=660)
        table.dataframe(df2_set6.T,width=660)



         
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

st.set_page_config(layout="wide")

col1, col2 = st.columns([4,2])
col2.title('Forex Learning Materials')
# forex market
st.video('https://www.youtube.com/watch?v=ig_EO805rpA') 
# mitigate risk forex
st.video('https://www.youtube.com/watch?v=Bj7j3iD8bow') 


col1.title('Forex Rate')
col1.write("Hello! Welcome to Forex Rate Prediction page!")

col1.write("According to Triennial Central Bank Survey conducted by Bank for International Settlements (2022), "
         "US dollar is still the world's dominant currency. 88.5% of all trades in April 2022 involve **US dollar**, "
         "followed by **Euro** (30.5%), **Japanese Yen** (16.7%) and **Great Britain Pound** (12.9%).")

col1.write("**Prediction not available.")

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



EURUSD, USDJPY, GBPUSD = col1.tabs(["EURUSD", "USDJPY**", "GBPUSD**"])
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
    plot_graph(df)   

    
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
container = col1.container(border=True)

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

