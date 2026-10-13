import streamlit as st

from app.sidebar import sidebar
from app.chat import chat_ui


class AppUI:

    def run(self):

        st.set_page_config(
            page_title="DocuMind AI",
            page_icon="📚",
            layout="wide"
        )

        if "selected_doc" not in st.session_state:
            st.session_state.selected_doc = None

        sidebar.render()

        chat_ui.render()


app_ui = AppUI()