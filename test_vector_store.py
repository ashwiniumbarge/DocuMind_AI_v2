from rag.pdf_processor import pdf_processor
from rag.vector_store import vector_store_manager

documents = pdf_processor.load_pdf("uploads/BigData.pdf")

vector_db = vector_store_manager.create(
    "sample",
    documents
)

results = vector_store_manager.similarity_search(
    vector_db,
    "What is Machine Learning?",
    k=3
)

print("\nTop Results:\n")

for i, doc in enumerate(results, start=1):

    print("=" * 60)

    print(f"Result {i}")

    print(doc.page_content[:300])

    print(doc.metadata)