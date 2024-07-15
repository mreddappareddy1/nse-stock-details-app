import streamlit as st
from nsepython import *
from datetime import date
from jugaad_data.nse import stock_csv, stock_df
import plotly.graph_objects as go

st.set_page_config(
    page_title="Stock Historical Data",
    layout="wide"  # Use the entire horizontal space
)

def stock_selection_change():
    data = 1

nifty500url = "https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%20500"
data = 0
tempdata = {}
stocksList =[]
flat_data = []
def fetch_marketstatus_data():
    tempstatus = nsefetch(nifty500url)
    return tempstatus

tempdata = fetch_marketstatus_data()
tempdata = tempdata['data']
marketData = pd.DataFrame(tempdata)
marketData.drop(0,axis=0,inplace=True)
for keys in tempdata:
    symbol = keys["symbol"]
    if symbol != "NIFTY 500":
        stocksList.append(symbol)
stocksListDF = pd.DataFrame(stocksList,columns=["Symbol"])
stocksListDF = stocksListDF.sort_values(by=["Symbol"],ascending=True)
selectedStock = st.selectbox(label="Stocks List",options=stocksListDF,placeholder="Select a stock")
df = stock_df(symbol=selectedStock, from_date=date(2024,4,1),
            to_date=date(2024,7,15), series="EQ")
fig = go.Figure(data=[go.Candlestick(x=df['DATE'],
                open=df['OPEN'], high=df['HIGH'],
                low=df['LOW'], close=df['CLOSE'])
                     ])

fig.update_layout(xaxis_rangeslider_visible=False)
st.plotly_chart(fig, use_container_width=True)