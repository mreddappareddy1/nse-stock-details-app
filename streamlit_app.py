import streamlit as st
import pandas as pd
import json
from nsepython import *
import requests

# Set page title and layout
st.set_page_config(
    page_title="NSE Stock Data",
    layout="wide"  # Use the entire horizontal space
)

nifty50url = "https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%2050"
nifty500url = "https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%20500"
niftyfnourl = "https://www.nseindia.com/api/equity-stockIndices?index=SECURITIES%20IN%20F%26O"
nsemarketstatusurl = "https://nseindia.com/api/marketStatus"
# Initially empty dictionary to store fetched data
data = 0
fiidiidata = []

def fetch_marketstatus_data():
    tempstatus = nse_index()
    return tempstatus

def fetch_fiidii_data():
    fiidiitemp = nse_fiidii()
    return fiidiitemp

def fetch_top_gainers():
    topgainers = nse_get_top_gainers()
    return topgainers

def fetch_top_losers():
    toplosers = nse_get_top_losers()
    return toplosers

empty_row1, _ = st.columns(2)
empty_row2, _ = st.columns(2)
top_row = st.container()

col1, col2 = st.columns(2) 
col3, col4 = st.columns(2)

# Button to trigger data refresh
with top_row:
    refresh_button = st.button("Refresh NSE Data")

if refresh_button:
    tempdata = fetch_marketstatus_data()
    data = 1

#Nifty summary
with col1:
    st.header("Market Summary")
    if data:
        filterlist = ['NIFTY 50','NIFTY BANK','INDIA VIX','NIFTY MIDCAP 50','NIFTY MID SELECT','NIFTY FIN SERVICE']
        filtered_data = tempdata[tempdata['indexName'].isin(filterlist)]
        neworder = ['indexName','last','previousClose','percChange']
        filtered_data = filtered_data[neworder]
        filtered_data = filtered_data.reset_index(drop=True)
        st.write(filtered_data)
    else:
        st.info("Click 'Refresh Data' to fetch the latest data.")
   
# # Advances vs. Declines
with col2:
    st.header("Advances vs. Declines")
    # Add code to fetch and display advances/declines data
    if data:
        fiidiidata = fetch_fiidii_data()
        fiicols = ['category','buyValue','sellValue','netValue']
        fiidiidata = fiidiidata.reset_index(drop=True)
        st.write(fiidiidata[fiicols])
    else:
        st.info("Click 'Refresh Data' to fetch the latest data.")

with col3:
    st.header("Top Gainers")
    # Add code to fetch and display advances/declines data
    if data:
        topgainers = fetch_top_gainers()
        cols = ['symbol','change','pChange','totalTradedVolume']
        st.write(topgainers[cols])
    else:
        st.info("Click 'Refresh Data' to fetch the latest data.")
with col4:
    st.header("Top Losers")
    # Add code to fetch and display advances/declines data
    if data:
        toplosers = fetch_top_losers()
        cols = ['symbol','change','pChange','totalTradedVolume']
        st.write(toplosers[cols])
    else:
        st.info("Click 'Refresh Data' to fetch the latest data.")



