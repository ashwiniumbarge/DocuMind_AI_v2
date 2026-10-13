from rag.pdf_processor import pdf_processor
from rag.vector_store import vector_store_manager
from rag.retriever import hybrid_retriever
from rag.prompt_builder import prompt_builder

documents = pdf_processor.load_pdf(
    "uploads/BigData.pdf"
)

vector_db = vector_store_manager.create(
    "BigData",
    documents
)

hybrid_retriever.build(documents)

results = hybrid_retriever.hybrid_search(
    vector_store=vector_db,
    query="Explain the 5Vs of Big Data",
    top_k=5
)

prompt = prompt_builder.build_prompt(
    query="Explain the 5Vs of Big Data",
    documents=results,
    history=""
)

print(prompt)