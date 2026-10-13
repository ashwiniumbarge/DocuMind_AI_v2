import streamlit as st
from app.sidebar import sidebar

st.set_page_config(
    page_title="Sidebar Test",
    layout="wide"
)

sidebar.render()