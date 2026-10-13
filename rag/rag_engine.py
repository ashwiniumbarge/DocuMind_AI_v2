"""
============================================================
DocuMind AI v3
RAG Engine
============================================================
"""

import time
from typing import List

from google import genai
from google.genai import types
from langchain_core.documents import Document

from core.config import (
    GOOGLE_API_KEY,
    LLM_MODEL,
    TEMPERATURE,
    MAX_OUTPUT_TOKENS,
)

from core.logger import logger
from rag.retriever import hybrid_retriever
from rag.vector_store import vector_store


class RAGEngine:
    """
    Main Hybrid RAG Engine
    """

    def __init__(self):

        if not GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY not found.")

        self.client = genai.Client(
            api_key=GOOGLE_API_KEY
        )

    # ---------------------------------------------------------
    # Build Context
    # ---------------------------------------------------------

    def build_context(
        self,
        documents: List[Document]
    ) -> str:

        context = ""

        for i, doc in enumerate(documents, start=1):

            source = doc.metadata.get("source", "Unknown")

            page = doc.metadata.get("page", "N/A")

            context += f"""
==============================
Document Chunk {i}

Source : {source}

Page : {page}

Content:

{doc.page_content}

"""

        return context

    # ---------------------------------------------------------
    # Build Conversation History
    # ---------------------------------------------------------

    def build_history(
        self,
        chat_history
    ):

        if chat_history is None:
            return ""

        if len(chat_history) == 0:
            return ""

        history = ""

        recent_history = chat_history[-3:]

        for item in recent_history:

            history += f"""

User:
{item["question"]}

Assistant:
{item["answer"]}

"""

        return history

    # ---------------------------------------------------------
    # Ask Question
    # ---------------------------------------------------------

    def ask(
    self,
    vector_store_name,
    question,
    chat_history=None,
    ):

        logger.info(f"Question: {question}")

        if chat_history is None:
            chat_history = []

        # ---------------------------------------------------------
        # Load Vector Store
        # ---------------------------------------------------------

        retrieval_start = time.time()

        db = vector_store.load(vector_store_name)

        if db is None:
            raise ValueError(
                f"Vector store '{vector_store_name}' not found."
            )

        all_documents = list(db.docstore._dict.values())

        hybrid_retriever.build(all_documents)

        documents = hybrid_retriever.hybrid_search(
            vector_store=db,
            query=question,
        )

        retrieval_time = round(
            time.time() - retrieval_start,
            2,
        )

        if not documents:
            return {
                "answer": "I couldn't find any relevant information in the uploaded document.",
                "documents": [],
                "sources": [],
                "prompt": "",
                "retrieval_time": retrieval_time,
                "generation_time": 0,
                "total_time": retrieval_time,
                "context": "",
                "history": "",
            }

        # ---------------------------------------------------------
        # Build Prompt
        # ---------------------------------------------------------

        context = self.build_context(documents)

        history = self.build_history(chat_history)

        prompt = f"""
    You are DocuMind AI, an intelligent document assistant.

    Answer ONLY using the provided document context.

    If the answer is not available in the context, say:

    "I couldn't find the answer in the uploaded document."

    ==============================
    PREVIOUS CONVERSATION
    ==============================

    {history}

    ==============================
    DOCUMENT CONTEXT
    ==============================

    {context}

    ==============================
    QUESTION
    ==============================

    {question}

    ==============================
    RULES
    ==============================

    1. Use only the document.
    2. Don't make up information.
    3. Use previous conversation when needed.
    4. Answer clearly.
    5. Use bullet points whenever appropriate.
    """

        # ---------------------------------------------------------
        # Gemini Generation
        # ---------------------------------------------------------

        logger.info("Sending request to Gemini...")

        generation_start = time.time()

        try:

            response = self.client.models.generate_content(

                model=LLM_MODEL,

                contents=prompt,

                config=types.GenerateContentConfig(

                    temperature=TEMPERATURE,

                    max_output_tokens=MAX_OUTPUT_TOKENS,

                ),

            )

            answer = (
                response.text.strip()
                if getattr(response, "text", None)
                else "No response generated."
            )

        except Exception as e:

            logger.exception("Gemini Error")

            answer = f"Error while generating response:\n\n{str(e)}"

        generation_time = round(
            time.time() - generation_start,
            2,
        )

        logger.info("Response generated successfully.")

        return {

            "answer": answer,

            "documents": documents,

            "sources": [
                doc.metadata
                for doc in documents
            ],

            "prompt": prompt,

            "retrieval_time": retrieval_time,

            "generation_time": generation_time,

            "total_time": round(
                retrieval_time + generation_time,
                2,
            ),

            "context": context,

            "history": history,

        }


# ---------------------------------------------------------
# Singleton
# ---------------------------------------------------------

rag_engine = RAGEngine()