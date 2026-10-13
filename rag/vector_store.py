"""
============================================================
DocuMind AI v2
Vector Store Manager
============================================================
"""

import shutil
from pathlib import Path
from typing import List

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

from core.config import VECTORSTORE_DIR
from core.logger import logger
from rag.embeddings import embedding_manager


class VectorStoreManager:
    """
    Handles creation, saving, loading,
    searching and deletion of FAISS indexes.
    """

    def __init__(self):
        self.base_dir = VECTORSTORE_DIR

    def _get_store_path(self, document_name: str) -> Path:
        """
        Return folder path for a document index.
        """
        return self.base_dir / document_name

    def create(self, document_name: str, documents: List[Document]):
        """
        Create FAISS index.
        """

        logger.info(f"Creating FAISS index for {document_name}")

        vector_store = FAISS.from_documents(
            documents=documents,
            embedding=embedding_manager.model
        )

        store_path = self._get_store_path(document_name)

        store_path.mkdir(parents=True, exist_ok=True)

        vector_store.save_local(str(store_path))

        logger.info("Vector store created successfully.")

        return vector_store

    def load(self, document_name: str):
        """
        Load existing FAISS index.
        """

        store_path = self._get_store_path(document_name)

        if not store_path.exists():
            raise FileNotFoundError(
                f"Vector store not found: {document_name}"
            )

        logger.info(f"Loading vector store: {document_name}")

        return FAISS.load_local(
            str(store_path),
            embedding_manager.model,
            allow_dangerous_deserialization=True
        )

    def similarity_search(
        self,
        vector_store,
        query: str,
        k: int = 5
    ):
        """
        Retrieve top-k similar chunks.
        """

        return vector_store.similarity_search(
            query=query,
            k=k
        )

    def similarity_search_with_score(
        self,
        vector_store,
        query: str,
        k: int = 5
    ):
        """
        Retrieve chunks with similarity scores.
        """

        return vector_store.similarity_search_with_score(
            query=query,
            k=k
        )

    def delete(self, document_name: str):
        """
        Delete vector store.
        """

        store_path = self._get_store_path(document_name)

        if store_path.exists():

            shutil.rmtree(store_path)

            logger.info(
                f"Deleted vector store: {document_name}"
            )


vector_store = VectorStoreManager()