# import libraries
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime


st.write("Hello! Welcome to Forex Prediction page!")

st.sidebar.title("Forex Pair")
st.sidebar.radio("Pick the interested forex pair.", ["EURUSD", "GBPUSD", "USDJPY"])

rand = np.random.normal(1, 2, size=20)
fig, ax = plt.subplots()
ax.hist(rand, bins=15)
st.pyplot(fig)

st.write("Disclaimer: Trading involves risk. \n"
         "As a general rule, you should only trade in financial products that "
         "you are familiar with and understand the risk associated with them. \n"
         "Trade at your own risk.")

while True:
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    time = "Current Time = " + current_time
    st.write(time)






