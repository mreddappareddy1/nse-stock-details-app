import streamlit as st
import pandas as pd
import json
from nsepython import *
import requests

st.set_page_config(
    page_title="Stock Details",
    layout="wide"  # Use the entire horizontal space
)
pd.options.display.precision = 2
fnourl = "https://www.nseindia.com/api/equity-stockIndices?index=SECURITIES%20IN%20F%26O"
data = 0
tempdata = {}
flat_data = []

def fetch_fnostock_data():
    tempstatus = nsefetch(fnourl)
    return tempstatus

def convert_to_crores(value):
    return value/10000000

top_row = st.container()

with top_row:
    refresh_button = st.button("Refresh NSE Data")

if refresh_button:
    tempdata = fetch_fnostock_data()
    tempdata = tempdata['data']
    data = 1

with st.container():
    if data==1:
        st.header("FnO Stock Details")
        marketData = pd.DataFrame(tempdata)
        fnocols = ['symbol','lastPrice','change','pChange','totalTradedVolume','totalTradedValue','companyName','industry']
        for keys in tempdata:
            symbol = keys['symbol']
            lastPrice = keys['lastPrice']
            change = keys['change']
            pChange = keys['pChange']
            totalTradedVolume = keys['totalTradedVolume']
            totalTradedValue = keys['totalTradedValue']
            chart30dPath = keys['chart30dPath']
            chartTodayPath = keys['chartTodayPath']
            if "meta" in keys:
                meta = keys["meta"]
                if "industry" in meta:
                    industry = meta["industry"]
                    companyName = meta["companyName"]
                    flat_data.append({"Symbol":symbol,
                                      "Company Name":companyName, 
                                      "Last Traded Price": lastPrice,
                                      "Change":change,
                                      "Change in Percent": pChange,
                                      "Traded Volume (in Crores)": totalTradedVolume/1000000,
                                      "Traded Value (in Crores)": totalTradedValue/1000000,
                                      "Industry": industry,
                                      "Chart Today": chartTodayPath,
                                      "Chart 30 Days":chart30dPath
                                      })
        fno_df = pd.DataFrame(flat_data)
        fno_df['Change'] = pd.to_numeric(fno_df['Change'], errors='coerce')
        fno_df['Change'] = fno_df['Change'].round(2)
        fno_df['Change in Percent'] = pd.to_numeric(fno_df['Change in Percent'], errors='coerce')
        fno_df['Change in Percent'] = fno_df['Change in Percent'].round(2)
        fno_df['Traded Volume (in Crores)'] = pd.to_numeric(fno_df['Traded Volume (in Crores)'], errors='coerce')
        fno_df['Traded Volume (in Crores)'] = fno_df['Traded Volume (in Crores)'].round(2)
        fno_df['Traded Value (in Crores)'] = pd.to_numeric(fno_df['Traded Value (in Crores)'], errors='coerce').round(2)
        fno_df['Traded Value (in Crores)'] = fno_df['Traded Value (in Crores)'].round(2)
        #industryOption = st.selectbox("Select an Industry",fno_df["Industry"],on_change=fetch_fnostock_data)
        st.dataframe(
            fno_df,
            column_config={
                "Symbol": st.column_config.TextColumn("Symbol"),
                "Company Name": st.column_config.TextColumn("Company Name",width="medium"),
                "Last Traded Price": st.column_config.NumberColumn("LTP",format="%.2f",width="small"),
                "Change": st.column_config.NumberColumn(
                    "Change",
                    format="%.2f",
                    width="small"
                ),
                "Traded Volume (in Crores)":st.column_config.NumberColumn("Volume(Cr)",format="%.2f"),
                "Traded Value (in Crores)":st.column_config.NumberColumn("Value(Cr)",format="%.2f"),
                "Change in Percent":st.column_config.NumberColumn("Change%",format="%.2f",width="small"),
                "Chart Today": st.column_config.ImageColumn("Chart Today"),
                "Chart 30 Days": st.column_config.ImageColumn("Chart 30 Days")
            },
            hide_index=True,
        )
    else:
        st.info("Click 'Refresh Data' to fetch the latest data.")