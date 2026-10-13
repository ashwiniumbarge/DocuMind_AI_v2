from rag.pdf_processor import pdf_processor
from rag.vector_store import vector_store_manager
from rag.retriever import hybrid_retriever
from rag.rag_engine import rag_engine

# Load PDF
documents = pdf_processor.load_pdf("uploads/BigData.pdf")

# Create Vector Store
vector_db = vector_store_manager.create(
    "BigData",
    documents
)

# Build BM25 Index
hybrid_retriever.build(documents)

# Ask Question
response = rag_engine.ask(
    vector_store=vector_db,
    question="Explain the 5Vs of Big Data."
)

print("\n========== ANSWER ==========\n")
print(response["answer"])

print("\n========== SOURCES ==========\n")
for source in response["sources"]:
    print(source)