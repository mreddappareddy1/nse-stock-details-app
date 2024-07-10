import streamlit as st

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
   border-style: dashed;
}
</style>
""",
    unsafe_allow_html=True,
)

st.metric("Value!", 1.2, 1.0)