"""
============================================================
DocuMind AI v2
Hybrid Retriever
============================================================
"""

from typing import List

from langchain_core.documents import Document
from rank_bm25 import BM25Okapi

from core.config import TOP_K
from core.logger import logger
from rag.reranker import reranker

class HybridRetriever:
    """
    Hybrid Retriever using:
    1. FAISS (Semantic Search)
    2. BM25 (Keyword Search)
    3. CrossEncoder Reranking
    """

    def __init__(self):

        self.documents: List[Document] = []
        self.bm25 = None

    # =====================================================
    # Build BM25 Index
    # =====================================================

    def build(self, documents: List[Document]):

        logger.info("Building BM25 index...")

        self.documents = documents

        corpus = [
            doc.page_content.lower().split()
            for doc in documents
        ]

        self.bm25 = BM25Okapi(corpus)

        logger.info(
            f"BM25 index created for {len(documents)} chunks."
        )

    # =====================================================
    # BM25 Search
    # =====================================================

    def bm25_search(
        self,
        query: str,
        top_k: int = TOP_K
    ) -> List[Document]:

        if self.bm25 is None:
            raise RuntimeError(
                "BM25 index has not been created."
            )

        query_tokens = query.lower().split()

        scores = self.bm25.get_scores(query_tokens)

        ranked = sorted(
            enumerate(scores),
            key=lambda x: x[1],
            reverse=True
        )

        results = []

        for index, score in ranked[:top_k]:
            results.append(self.documents[index])

        return results

    # =====================================================
    # FAISS Search
    # =====================================================

    def semantic_search(
        self,
        vector_store,
        query: str,
        top_k: int = TOP_K
    ) -> List[Document]:

        return vector_store.similarity_search(
            query=query,
            k=top_k
        )

    # =====================================================
    # Remove Duplicate Documents
    # =====================================================

    @staticmethod
    def remove_duplicates(
        documents: List[Document]
    ) -> List[Document]:

        unique_docs = []

        seen = set()

        for doc in documents:

            key = (
                doc.metadata.get("source"),
                doc.metadata.get("page"),
                doc.metadata.get("chunk")
            )

            if key not in seen:

                seen.add(key)

                unique_docs.append(doc)

        return unique_docs

    # =====================================================
    # Hybrid Search
    # =====================================================

    def hybrid_search(
        self,
        vector_store,
        query: str,
        top_k: int = TOP_K
    ) -> List[Document]:

        logger.info(
            f"Hybrid Retrieval: {query}"
        )

        # --------------------------
        # FAISS
        # --------------------------

        semantic_results = self.semantic_search(
            vector_store,
            query,
            top_k
        )

        logger.info(
            f"Semantic Results : {len(semantic_results)}"
        )

        # --------------------------
        # BM25
        # --------------------------

        keyword_results = self.bm25_search(
            query,
            top_k
        )

        logger.info(
            f"Keyword Results : {len(keyword_results)}"
        )

        # --------------------------
        # Merge
        # --------------------------

        merged = semantic_results + keyword_results

        merged = self.remove_duplicates(merged)

        logger.info(
            f"Unique Results : {len(merged)}"
        )

        # --------------------------
        # CrossEncoder
        # --------------------------

        reranked = reranker.rerank(
            query=query,
            documents=merged,
            top_k=top_k
        )

        logger.info(
            f"Final Results : {len(reranked)}"
        )

        return reranked


hybrid_retriever = HybridRetriever()