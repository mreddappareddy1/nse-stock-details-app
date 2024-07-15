import streamlit as st
from nsepython import *

tempdata = nse_events()
st.write(tempdata)