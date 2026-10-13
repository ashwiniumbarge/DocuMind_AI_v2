"""
============================================================
DocuMind AI v2
Cross Encoder Reranker
============================================================
"""

from functools import lru_cache
from typing import List

from sentence_transformers import CrossEncoder
from langchain_core.documents import Document

from core.config import RERANKER_MODEL
from core.logger import logger


class Reranker:

    def __init__(self):

        self.model = self.load_model()

    @staticmethod
    @lru_cache(maxsize=1)
    def load_model():

        logger.info(
            f"Loading CrossEncoder: {RERANKER_MODEL}"
        )

        model = CrossEncoder(RERANKER_MODEL)

        logger.info("CrossEncoder loaded successfully.")

        return model

    def rerank(
        self,
        query: str,
        documents: List[Document],
        top_k: int = 5
    ) -> List[Document]:

        if not documents:
            return []

        sentence_pairs = [
            (query, doc.page_content)
            for doc in documents
        ]

        scores = self.model.predict(sentence_pairs)

        ranked = sorted(
            zip(scores, documents),
            key=lambda x: x[0],
            reverse=True
        )

        return [
            doc
            for score, doc in ranked[:top_k]
        ]


reranker = Reranker()