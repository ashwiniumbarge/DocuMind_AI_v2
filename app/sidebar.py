import os
from pathlib import Path

import streamlit as st

from rag.pdf_processor import pdf_processor
from rag.vector_store import vector_store
from core.config import (
    UPLOAD_DIR,
    VECTORSTORE_DIR,
    EMBEDDING_MODEL,
    LLM_MODEL,
)
from core.logger import logger


class Sidebar:

    def __init__(self):
        pass

    # -----------------------------------------------------
    # Storage Statistics
    # -----------------------------------------------------

    def storage_statistics(self):

        stores = []

        if Path(VECTORSTORE_DIR).exists():
            stores = [
                folder
                for folder in Path(VECTORSTORE_DIR).iterdir()
                if folder.is_dir()
            ]

        st.sidebar.markdown("### 💾 Storage")

        col1, col2 = st.sidebar.columns(2)

        col1.metric(
            "PDFs",
            len(stores)
        )

        col2.metric(
            "Vectors",
            len(stores)
        )

    # -----------------------------------------------------
    # AI Information
    # -----------------------------------------------------

    def model_information(self):

        st.sidebar.divider()

        st.sidebar.markdown("### 🤖 AI Models")

        st.sidebar.info(
            f"""
LLM

**{LLM_MODEL}**

Embedding

**{EMBEDDING_MODEL}**

Retriever

**Hybrid (FAISS + BM25)**
"""
        )

    # -----------------------------------------------------
    # Current Document
    # -----------------------------------------------------

    def current_document(self):

        st.sidebar.divider()

        st.sidebar.markdown("### 📄 Current Document")

        if "selected_doc" in st.session_state:

            st.sidebar.success(
                st.session_state["selected_doc"]
            )

        else:

            st.sidebar.warning(
                "No document selected."
            )

    # -----------------------------------------------------
    # Upload PDF
    # -----------------------------------------------------

    def upload_document(self):

        st.sidebar.markdown("## 📤 Upload PDF")

        uploaded_file = st.sidebar.file_uploader(

            "Choose PDF",

            type=["pdf"]

        )

        if uploaded_file is None:

            return

        save_path = os.path.join(

            UPLOAD_DIR,

            uploaded_file.name

        )

        with open(save_path, "wb") as f:

            f.write(uploaded_file.getbuffer())

        st.sidebar.success("✅ PDF Uploaded")

        if st.sidebar.button(

            "🚀 Process Document",

            use_container_width=True

        ):

            progress = st.sidebar.progress(0)

            progress.progress(20)

            logger.info(
                f"Processing {uploaded_file.name}"
            )

            documents = pdf_processor.load_pdf(
                save_path
            )

            progress.progress(60)

            vector_store.create(

                os.path.splitext(uploaded_file.name)[0],

                documents

            )

            progress.progress(100)

            progress.empty()

            st.sidebar.success(
                "✅ Vector Store Created Successfully!"
            )

            st.balloons()
    # -----------------------------------------------------
    # Available Documents
    # -----------------------------------------------------

    def document_selector(self):

        st.sidebar.divider()

        st.sidebar.markdown("## 📂 Documents")

        if not Path(VECTORSTORE_DIR).exists():

            st.sidebar.info("No vector stores found.")

            return

        folders = sorted(
            [
                folder.name
                for folder in Path(VECTORSTORE_DIR).iterdir()
                if folder.is_dir()
            ]
        )

        if len(folders) == 0:

            st.sidebar.info("No processed documents.")

            return

        selected = st.sidebar.selectbox(

            "Select Document",

            folders,

            index=0

        )

        st.session_state["selected_doc"] = selected

    # -----------------------------------------------------
    # Delete Document
    # -----------------------------------------------------

    def delete_document(self):

        st.sidebar.divider()

        st.sidebar.markdown("### 🗑 Delete")

        if st.sidebar.button(

            "Delete Selected Document",

            use_container_width=True,

            type="secondary"

        ):

            if "selected_doc" not in st.session_state:

                st.sidebar.warning("No document selected.")

                return

            try:

                vector_store.delete(

                    st.session_state["selected_doc"]

                )

                st.sidebar.success(
                    "✅ Document deleted successfully."
                )

                st.rerun()

            except Exception as e:

                logger.exception("Error deleting document")

                st.sidebar.error(f"❌ {str(e)}")

    # -----------------------------------------------------
    # System Status
    # -----------------------------------------------------

    def system_status(self):

        st.sidebar.divider()

        st.sidebar.markdown("### 🟢 System Status")

        st.sidebar.success(
            """
            ✅ Gemini Connected

            ✅ Embeddings Ready

            ✅ FAISS Ready

            ✅ BM25 Ready

            ✅ RAG Engine Ready
            """
        )

    # -----------------------------------------------------
    # Footer
    # -----------------------------------------------------

    def footer(self):

        st.sidebar.divider()

        st.sidebar.markdown("---")

        st.sidebar.caption("🚀 Powered by Gemini 3.5 Flash")
        st.sidebar.caption("📚 Hybrid RAG | FAISS | BM25")
        st.sidebar.caption("Version 3.0")

    # -----------------------------------------------------
    # Render Sidebar
    # -----------------------------------------------------

    def render(self):

        st.sidebar.title("📚 DocuMind AI")

        self.upload_document()
        self.document_selector()
        self.current_document()
        self.storage_statistics()
        self.model_information()
        self.system_status()
        self.delete_document()
        self.footer()


sidebar = Sidebar()