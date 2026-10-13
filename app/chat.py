import time
import streamlit as st

from rag.rag_engine import rag_engine
from core.logger import logger


# ==========================================================
# Page Configuration
# ==========================================================

st.set_page_config(
    page_title="DocuMind AI",
    page_icon="📚",
    layout="wide"
)


# ==========================================================
# Custom CSS
# ==========================================================

st.markdown("""
<style>

.block-container{
    padding-top:2rem;
    padding-bottom:2rem;
}

.user-card{
    background:#E3F2FD;
    padding:15px;
    border-radius:12px;
    margin-bottom:10px;
}

.bot-card{
    background:#F7F7F7;
    padding:15px;
    border-radius:12px;
    margin-bottom:15px;
}

.metric-card{
    border:1px solid #ddd;
    border-radius:10px;
    padding:10px;
}

.source-card{
    border-left:5px solid #4CAF50;
    padding:12px;
    background:#fafafa;
    margin-bottom:10px;
    border-radius:8px;
}

.question-btn button{
    width:100%;
}

</style>
""", unsafe_allow_html=True)


# ==========================================================
# Session State
# ==========================================================

# NOTE: session state is created in ChatUI.init_session_state(), which runs on every page load.


# ==========================================================
# Chat UI
# ==========================================================

class ChatUI:

    def __init__(self):

        self.app_name = "📚 DocuMind AI"

    # --------------------------------------------------
    # Session State (runs for every new browser session)
    # --------------------------------------------------

    def init_session_state(self):

        defaults = {
            "messages": [],
            "chat_history": [],
            "current_answer": "",
            "question": "",
        }

        for key, value in defaults.items():

            if key not in st.session_state:

                st.session_state[key] = value

    # --------------------------------------------------
    # Header
    # --------------------------------------------------

    def show_header(self):

        st.title("📚 DocuMind AI")

        st.caption(
            "Hybrid RAG using FAISS + BM25 + Gemini 3.5 Flash"
        )

        st.markdown(
            """
            <style>
            .doc-card{
                border-left:6px solid #4CAF50;
                padding:15px;
                background:#f7f7f7;
                border-radius:10px;
                margin-bottom:15px;
            }
            </style>
            """,
            unsafe_allow_html=True
        )


        st.divider()

    # --------------------------------------------------
    # Document Information
    # --------------------------------------------------

    def show_document_info(self):

        if "selected_doc" not in st.session_state:

            st.warning(
                "👈 Upload a PDF from the sidebar."
            )

            st.stop()

        document = st.session_state["selected_doc"]

        st.markdown(
            f"""
            <div class="doc-card">

            <h4>📄 Current Document</h4>

            <b>{document}</b>

            </div>
            """,
            unsafe_allow_html=True
        )

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Status",
            "Ready"
        )

        col2.metric(
            "Retriever",
            "Hybrid"
        )

        col3.metric(
            "LLM",
            "Gemini"
        )

        st.divider()

    # ------------------------------------------------------

    def suggested_questions(self):
        st.subheader("💡 Suggested Questions")

        questions = [

            "What is Big Data?",

            "Summarize this document.",

            "Explain this in simple language.",

            "Generate 10 interview questions.",

            "Generate MCQs.",

            "What are the important points?"

        ]

        col1, col2 = st.columns(2)

        for i, question in enumerate(questions):

            if i % 2 == 0:

                if col1.button(
                    question,
                    use_container_width=True,
                    key=f"q{i}"
                ):

                    st.session_state.question = question

            else:

                if col2.button(
                    question,
                    use_container_width=True,
                    key=f"q{i}"
                ):

                    st.session_state.question = question

        st.divider()

        
    # ------------------------------------------------------

    def display_chat(self):

        if len(st.session_state.messages) == 0:

            st.info(
                "👋 Ask a question about your uploaded document."
            )

            return

        for msg in st.session_state.messages:

            with st.chat_message(msg["role"]):

                st.markdown(msg["content"])

    # ------------------------------------------------------
        # ------------------------------------------------------
    # Typing Animation
    # ------------------------------------------------------

    def type_writer(self, text):

        placeholder = st.empty()

        output = ""

        for word in text.split():

            output += word + " "

            placeholder.markdown(output)

            time.sleep(0.02)

        return placeholder

    # ------------------------------------------------------
    # Performance Metrics
    # ------------------------------------------------------

    def show_performance(self, result):

        retrieval = result.get("retrieval_time", 0)

        generation = result.get("generation_time", 0)

        total = result.get("total_time", retrieval + generation)

        with st.expander("📊 Performance", expanded=False):

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Retrieval",
                f"{retrieval:.2f} sec"
            )

            col2.metric(
                "Generation",
                f"{generation:.2f} sec"
            )

            col3.metric(
                "Total",
                f"{total:.2f} sec"
            )

            if "documents" in result:

                st.metric(
                    "Chunks Retrieved",
                    len(result["documents"])
                )

    # ------------------------------------------------------
    # Source Viewer
    # ------------------------------------------------------

    def show_sources(self, result):

        documents = result.get("documents", [])

        if len(documents) == 0:
            return

        with st.expander("📚 Retrieved Sources", expanded=False):

            for index, doc in enumerate(documents, start=1):

                st.markdown(
                    f"""
                    <div class="source-card">

                    ### 📄 Source {index}

                    **Document**

                    {doc.metadata.get("source","Unknown")}

                    **Page**

                    {doc.metadata.get("page","N/A")}

                    </div>
                        """,
                    unsafe_allow_html=True
                )

                st.code(
                    doc.page_content,
                    language="text"
                )

    # ------------------------------------------------------
    # Ask Question
    # ------------------------------------------------------

    def ask_question(self, prompt):

    # ---------------------------------------------------
    # Save User Message
    # ---------------------------------------------------

        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt
            }
        )

        with st.chat_message("user"):
            st.markdown(prompt)

        # ---------------------------------------------------
        # Assistant Response
        # ---------------------------------------------------

        with st.chat_message("assistant"):

            with st.spinner("🤖 Thinking..."):

                try:

                    logger.info(f"Question : {prompt}")

                    # Make sure a document is selected
                    if "selected_doc" not in st.session_state:

                        st.error("Please select a document.")

                        return

                    result = rag_engine.ask(

                        vector_store_name=st.session_state["selected_doc"],

                        question=prompt,

                        chat_history=st.session_state.chat_history

                    )

                    answer = result["answer"]

                    # ---------------------------------------
                    # Save Conversation Memory
                    # ---------------------------------------

                    st.session_state.chat_history.append(

                        {

                            "question": prompt,

                            "answer": answer

                        }

                    )

                    # Keep only the last 10 conversations
                    if len(st.session_state.chat_history) > 10:

                        st.session_state.chat_history = (
                            st.session_state.chat_history[-10:]
                        )

                    # ---------------------------------------
                    # Typing Animation
                    # ---------------------------------------

                    placeholder = self.type_writer(answer)

                    placeholder.markdown(answer)

                    # ---------------------------------------
                    # Save Assistant Message
                    # ---------------------------------------

                    st.session_state.messages.append(

                        {

                            "role": "assistant",

                            "content": answer

                        }

                    )

                    st.session_state.current_answer = answer

                    # ---------------------------------------
                    # Show Sources
                    # ---------------------------------------

                    self.show_sources(result)

                    # ---------------------------------------
                    # Performance
                    # ---------------------------------------

                    self.show_performance(result)

                except Exception as e:

                    logger.exception("Chat Error")

                    st.error(f"❌ {str(e)}")


    def render(self):

        self.init_session_state()

        self.show_header()

        self.show_document_info()

        self.suggested_questions()

        # -----------------------------
        # Clear Chat Button
        # -----------------------------

        col1, col2 = st.columns([1, 5])

        with col1:

            if st.button("🗑 Clear Chat"):

                st.session_state.messages = []

                st.session_state.chat_history = []

                st.rerun()

        with col2:

            if (
                "current_answer" in st.session_state
                and st.session_state.current_answer
            ):

                st.download_button(

                    "📥 Download Answer",

                    st.session_state.current_answer,

                    file_name="answer.txt",

                    mime="text/plain"

                )

        self.display_chat()

        prompt = st.chat_input(
            "Ask anything about your document..."
        )

        if st.session_state.get("question"):

            prompt = st.session_state.question

            st.session_state.question = ""

        if prompt:

            self.ask_question(prompt)


chat_ui = ChatUI()