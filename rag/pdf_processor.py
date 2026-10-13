"""
============================================================
DocuMind AI v2
PDF Processor
============================================================
"""

from pathlib import Path
from typing import List

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader

from core.config import CHUNK_SIZE, CHUNK_OVERLAP
from core.logger import logger
from core.utils import clean_text


class PDFProcessor:
    """
    Reads PDF files, extracts text, cleans it,
    and converts it into LangChain Documents.
    """

    def __init__(self):

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            separators=[
                "\n\n",
                "\n",
                ". ",
                " ",
                ""
            ]
        )

    def load_pdf(self, pdf_path: str) -> List[Document]:
        """
        Read a PDF and split it into chunks.

        Parameters
        ----------
        pdf_path : str
            Path to PDF file.

        Returns
        -------
        List[Document]
            LangChain Document objects.
        """

        pdf_path = Path(pdf_path)

        # ---------------------------------------------------
        # Check file exists
        # ---------------------------------------------------

        if not pdf_path.exists():
            raise FileNotFoundError(
                f"PDF file not found: {pdf_path}"
            )

        # ---------------------------------------------------
        # Check extension
        # ---------------------------------------------------

        if pdf_path.suffix.lower() != ".pdf":
            raise ValueError(
                "Only PDF files are supported."
            )

        logger.info(f"Reading PDF: {pdf_path.name}")

        documents = []

        try:

            reader = PdfReader(str(pdf_path))

            total_pages = len(reader.pages)

            logger.info(f"Total Pages: {total_pages}")

            for page_number, page in enumerate(reader.pages):

                try:

                    text = page.extract_text()

                    if not text:
                        logger.warning(
                            f"No text found on page {page_number + 1}"
                        )
                        continue

                    text = clean_text(text)

                    chunks = self.splitter.split_text(text)

                    for chunk_number, chunk in enumerate(chunks):

                        documents.append(

                            Document(

                                page_content=chunk,

                                metadata={

                                    "source": pdf_path.name,

                                    "page": page_number + 1,

                                    "chunk": chunk_number,

                                    "total_pages": total_pages

                                }

                            )

                        )

                except Exception as page_error:

                    logger.error(
                        f"Error processing page {page_number + 1}: {page_error}"
                    )

            logger.info(
                f"Generated {len(documents)} chunks."
            )

            return documents

        except Exception as e:

            logger.exception("Failed to process PDF.")

            raise RuntimeError(
                f"Unable to process PDF: {e}"
            )


pdf_processor = PDFProcessor()