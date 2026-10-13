"""
============================================================
DocuMind AI v2
Prompt Builder
============================================================
"""

from typing import List

from langchain_core.documents import Document

from core.logger import logger


class PromptBuilder:
    """
    Builds structured prompts for Gemini.
    """

    SYSTEM_PROMPT = """
You are DocuMind AI, an intelligent document assistant.

Your responsibilities:

1. Answer ONLY using the supplied document context.
2. Never invent facts.
3. If the answer is unavailable, say:
   "The uploaded document does not contain enough information."

4. If the document contains assignment questions,
   solve them step by step.

5. If code is requested:
   • Explain first
   • Then provide code
   • Explain the output

6. Always write clean Markdown.

7. Mention document page numbers whenever possible.

8. Keep answers clear, professional and detailed.

9. Never say:
   "I cannot access the uploaded document."

You already have the document context.

10. If multiple chunks contain the answer,
combine them into one coherent response.
"""

    # -----------------------------------------------------

    def build_context(
        self,
        documents: List[Document]
    ) -> str:

        context = []

        for doc in documents:

            source = doc.metadata.get("source", "Unknown")

            page = doc.metadata.get("page", "-")

            context.append(

                f"""
Source : {source}
Page   : {page}

{doc.page_content}
"""
            )

        return "\n\n".join(context)

    # -----------------------------------------------------

    def build_chat_history(
        self,
        history: str
    ) -> str:

        if not history:
            return "No previous conversation."

        return history

    # -----------------------------------------------------

    def build_prompt(
        self,
        query: str,
        documents: List[Document],
        history: str = ""
    ) -> str:

        logger.info("Building Prompt...")

        context = self.build_context(documents)

        chat_history = self.build_chat_history(history)

        prompt = f"""
================ SYSTEM ================

{self.SYSTEM_PROMPT}

================ CHAT HISTORY ================

{chat_history}

================ DOCUMENT CONTEXT ================

{context}

================ USER QUESTION ================

{query}

================ RESPONSE ================

Answer:
"""

        logger.info("Prompt Built Successfully.")

        return prompt


prompt_builder = PromptBuilder()