"""
============================================================
DocuMind AI v2
Embeddings Module
============================================================
"""

from functools import lru_cache
from typing import Optional

from langchain_huggingface import HuggingFaceEmbeddings

from core.config import EMBEDDING_MODEL
from core.logger import logger


class EmbeddingManager:
    """
    Singleton manager for HuggingFace embedding model.
    """

    def __init__(self):
        self._model: Optional[HuggingFaceEmbeddings] = None

    @staticmethod
    @lru_cache(maxsize=1)
    def _create_model():

        logger.info(
            f"Loading embedding model: {EMBEDDING_MODEL}"
        )

        model = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL,
            model_kwargs={
                "device": "cpu"
            },
            encode_kwargs={
                "normalize_embeddings": True
            }
        )

        logger.info("Embedding model loaded successfully.")

        return model

    @property
    def model(self):

        if self._model is None:
            self._model = self._create_model()

        return self._model

    def embed_documents(self, documents):

        return self.model.embed_documents(documents)

    def embed_query(self, query):

        return self.model.embed_query(query)


embedding_manager = EmbeddingManager()