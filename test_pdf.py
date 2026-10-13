from pathlib import Path
from rag.pdf_processor import pdf_processor

pdf_path = Path("uploads/BigData.pdf")

if not pdf_path.exists():
    print(f"PDF not found: {pdf_path}")
else:
    documents = pdf_processor.load_pdf(str(pdf_path))

    print("Total Chunks:", len(documents))

    if documents:
        print("\nFirst Chunk:\n")
        print(documents[0].page_content)

        print("\nMetadata:")
        print(documents[0].metadata)