import streamlit as st
import pandas as pd
from nsepython import *
from st_pages import Page, show_pages, add_page_title

st.set_page_config(
    page_title="NSE Stock Data",
    layout="wide"  # Use the entire horizontal space
)
add_page_title()

# Specify what pages should be shown in the sidebar, and what their titles and icons
# should be
show_pages(
    [
        Page("streamlit_app.py", "Summary Page", "🏠"),
        Page("pages/Industry_Wise_Change.py", "Industry Wise Change", ":books:"),
        Page("pages/Individual_Stock_details.py", "Individual Stock Details", ":chart:")
    ]
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

top_row = st.container()

# Button to trigger data refresh
with top_row:
    refresh_button = st.button("Refresh NSE Data")

if refresh_button:
    tempdata = fetch_marketstatus_data()
    data = 1

#Nifty summary
with st.container():
    st.header("Market Summary")
    if data:
        filterlist = ['NIFTY 50','NIFTY BANK','INDIA VIX'] #,'NIFTY MIDCAP 50','NIFTY MID SELECT','NIFTY FIN SERVICE']
        filtered_data = tempdata[tempdata['indexName'].isin(filterlist)]
        neworder = ['indexName','last','percChange']
        filtered_data = filtered_data[neworder]
        filtered_data = filtered_data.reset_index(drop=True)
        num_cols = 3
        i =0
        cols = st.columns(num_cols)
        metric_card_container = st.container()
        for indexName, last, percChange  in filtered_data[neworder].itertuples(index=False):
            col = cols[i % num_cols]
            i+=1
            with col:
                st.metric(label=indexName, value=last,delta=percChange)
    else:
        st.info("Click 'Refresh Data' to fetch the latest data.")
   
# # Advances vs. Declines
with st.container():
    st.header("FII / DII Data")
    # Add code to fetch and display advances/declines data
    if data:
        fiidiidata = fetch_fiidii_data()
        fiicols = ['category','buyValue','sellValue','netValue']
        fiidiidata = fiidiidata.reset_index(drop=True)
        fiidiidata['buyValue'] = pd.to_numeric(fiidiidata['buyValue'], errors='coerce')
        fiidiidata['sellValue'] = pd.to_numeric(fiidiidata['sellValue'], errors='coerce')
        fiidiidata['netValue'] = pd.to_numeric(fiidiidata['netValue'], errors='coerce')
        #st.write(fiidiidata[fiicols])
        num_cols = 3
        i =0
        cols = st.columns(num_cols)
        metric_card_container = st.container()
        for category, buyValue, sellValue,netValue  in fiidiidata[fiicols].itertuples(index=False):
            col = cols[i % num_cols]
            i+=1
            #netchange = ((buyValue - sellValue)/(sellValue))
            with col:
                st.metric(label=category, value=buyValue,delta=netValue)
    else:
        st.info("Click 'Refresh Data' to fetch the latest data.")

with st.container():
    st.header("Top Gainers")
    # Add code to fetch and display advances/declines data
    if data:
        topgainers = fetch_top_gainers()
        cols = ['symbol','lastPrice','change','pChange','totalTradedVolume']
        st.write(topgainers[cols])
    else:
        st.info("Click 'Refresh Data' to fetch the latest data.")
with st.container():
    st.header("Top Losers")
    # Add code to fetch and display advances/declines data
    if data:
        toplosers = fetch_top_losers()
        cols = ['symbol','lastPrice','change','pChange','totalTradedVolume']
        st.write(toplosers[cols])
    else:
        st.info("Click 'Refresh Data' to fetch the latest data.")



