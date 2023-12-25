# import libraries
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from schedule import every, repeat, run_pending
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import time


st.write("Hello! Welcome to Forex Prediction page!")

st.sidebar.title("Forex Pair")
st.sidebar.radio("Pick the interested forex pair.", ["EURUSD", "GBPUSD", "USDJPY"])

rand = np.random.normal(1, 2, size=20)
fig, ax = plt.subplots()
ax.hist(rand, bins=15)
st.pyplot(fig)


# with st.empty():
#     @repeat(every(5).seconds)
#     now = datetime.now()
#     current_time = now.strftime("%H:%M:%S")
#     time = "Current Time = " + current_time
#     st.write(time)
#
#     while True:
#       run_pending()
#       time.sleep(1)
#
def update_time():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    time = "Current Time = " + current_time
    st.write(time)

scheduler = BackgroundScheduler()
scheduler.add_job(update_time, 'interval', seconds=5)
scheduler.start()
st.title('Displaying Time')




st.write("Disclaimer: Trading involves risk. \n"
         "As a general rule, you should only trade in financial products that "
         "you are familiar with and understand the risk associated with them. \n"
         "Trade at your own risk.")







