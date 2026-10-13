from rag.pdf_processor import pdf_processor
from rag.vector_store import vector_store_manager
from rag.retriever import hybrid_retriever

print("Step 1")

documents = pdf_processor.load_pdf("uploads/BigData.pdf")

print("Step 2")

vector_db = vector_store_manager.create(
    "BigData",
    documents
)

print("Step 3")

hybrid_retriever.build(documents)

print("Step 4")

results = hybrid_retriever.hybrid_search(
    vector_store=vector_db,
    query="Explain Random Forest",
    top_k=5
)

print("Step 5")

print("\n========== RESULTS ==========\n")

for i, doc in enumerate(results, start=1):

    print("=" * 80)
    print(f"Rank : {i}")
    print(doc.metadata)
    print()
    print(doc.page_content[:400])