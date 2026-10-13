from rag.pdf_processor import pdf_processor
from rag.vector_store import vector_store_manager
from rag.retriever import hybrid_retriever

documents = pdf_processor.load_pdf(
    "uploads/BigData.pdf"
)

vector_db = vector_store_manager.create(
    "sample",
    documents
)

hybrid_retriever.build(documents)

results = hybrid_retriever.hybrid_search(
    vector_db,
    "Explain Random Forest",
    top_k=5
)

print()

for i, doc in enumerate(results):

    print("=" * 60)

    print("Rank", i + 1)

    print(doc.metadata)

    print(doc.page_content[:250])