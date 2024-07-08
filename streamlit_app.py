import streamlit as st
import pandas as pd
import json
from nsepython import *
import requests

st.title("💹 My new app")
st.write(
    "NSE Stock details app"
)
st.write(
    "Welcome to stock page"
)

json_file = "stock-data-json/equity-stockIndices500.json"
with open(json_file,'r') as f:
    stockData = json.load(f)

metadata = stockData['metadata']
#st.table(metadata)

df_data = []
sector_data = []

data = stockData['data']
for keys in data:
    symbol = keys['symbol']
    price = keys['lastPrice']
    df_data.append({"symbol": symbol,"lastTradedPrice":price})
    
df = pd.DataFrame(df_data)
# st.table(df)

for keys in data:
    symbol = keys['symbol']
    pchange = keys['pChange']
    if "meta" in keys:
        meta = keys['meta']
        if "industry" in meta:
            industry = meta['industry']
            #print(industry)
            sector_data.append({"Symbol":symbol,"Industry": industry,"Change":pchange})
        
sector_df = pd.DataFrame(sector_data)

average_change_by_industry = sector_df.groupby('Industry')['Change'].mean().reset_index()
average_change_by_industry = average_change_by_industry.sort_values('Change', ascending=False)
#st.table(average_change_by_industry)

url = "https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%20500"

nsedata = nsefetch(url)
nsedf  = pd.DataFrame(nsedata['data'])

stockdata = nsedata['data']
for keys in stockdata:
    if "meta" in keys:
        meta = keys["meta"]
        if "industry" in meta:
            st.write(meta["industry"])
#st.table(nsedf[['symbol','pChange']])
#st.table(nsedf)
# nsestockdata = nsedata["data"]
# st.write(nsestockdata)
# nsemeta = json.loads(nsedata['meta'])
# st.write(nsemeta)

