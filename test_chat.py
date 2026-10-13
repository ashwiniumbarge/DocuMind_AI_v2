import streamlit as st

from app.sidebar import sidebar
from app.chat import chat_ui

st.set_page_config(
    page_title="DocuMind AI",
    page_icon="📄",
    layout="wide"
)

sidebar.render()

chat_ui.render()