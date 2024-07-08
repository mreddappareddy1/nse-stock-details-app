import streamlit as st
import pandas as pd
import json
from nsepython import *
import requests

# Define a CSS class for the border
border_style = """
<style>
.metric-card {
  border: 1px solid #ddd;  /* Adjust border style (width, color) */
  padding: 5px;           /* Adjust padding for spacing inside the border */
  border-radius: 5px;     /* Optional: Add rounded corners
}
</style>
"""
st.set_page_config(
    page_title="Industry wise change",
    layout="wide"  # Use the entire horizontal space
)

nifty500url = "https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%20500"
data = 0
tempdata = {}
flat_data = []
def fetch_marketstatus_data():
    tempstatus = nsefetch(nifty500url)
    return tempstatus

def flatten_json(data):
  """
  Flattens a nested JSON dictionary, extracting industry from "metadata".

  Args:
      data: A nested JSON dictionary.

  Returns:
      A flattened dictionary with extracted industry information.
  """
  flattened_data = {}
  if isinstance(data, dict):
    for key, value in data.items():
      if key == "meta":
        flattened_data["industry"] = value.get("industry")  # Get industry if available
      else:
        # Copy other key-value pairs
        flattened_data[key] = value
      # Recursively flatten nested elements
      if isinstance(value, (dict, list)):
        flattened_data.update(flatten_json(value))
  elif isinstance(data, list):
    for i, item in enumerate(data):
      flattened_data[f"item_{i}"] = flatten_json(item)  # Flatten list elements
  return flattened_data

empty_row1, _ = st.columns(2)
empty_row2, _ = st.columns(2)
top_row = st.container()

with top_row:
    refresh_button = st.button("Refresh NSE Data")

if refresh_button:
    tempdata = fetch_marketstatus_data()
    tempdata = tempdata['data']
    data = 1
    
st.markdown(
    """
<style>
div[data-testid="metric-container"] > label[data-testid="stMetricLabel"] > div {
   overflow-wrap: break-word;
   white-space: break-spaces;
   color: red;
}
div[data-testid="metric-container"] > label[data-testid="stMetricLabel"] > div p {
   font-size: 200% !important;
}
</style>
""",
    unsafe_allow_html=True,
)
with st.container():
    if data==1:
        st.header("Industry wise Summary")
        marketData = pd.DataFrame(tempdata)
        for keys in tempdata:
            symbol = keys['symbol']
            pchange = keys['pChange']
            if "meta" in keys:
                meta = keys["meta"]
                if "industry" in meta:
                    industry = meta["industry"]
                    flat_data.append({"Symbol":symbol,"Industry": industry,"Change":pchange})
        sector_df = pd.DataFrame(flat_data)
        industry_movement = sector_df.groupby('Industry')['Change'].mean().reset_index()
        industry_movement['Change'] = industry_movement['Change'].round(2)
        industry_movement = industry_movement.sort_values("Change",ascending=False)  # Optional: specify ascending order
        num_cols = 3
        cols = st.columns(num_cols)
        metric_card_container = st.container()
        i=0
        for industry, change_value in industry_movement[['Industry', 'Change']].itertuples(index=False):
            col = cols[i % num_cols]
            i+=1
            with col:
                st.metric(label=industry, value=change_value,delta=change_value)

    else:
       st.info("Click 'Refresh Data' to fetch the latest data.")
    