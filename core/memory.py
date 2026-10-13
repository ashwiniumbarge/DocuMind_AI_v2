"""
============================================================
DocuMind AI v2
Conversation Memory
============================================================
"""

from collections import deque
from typing import Dict, List

from core.config import MAX_CHAT_HISTORY


class ConversationMemory:
    """
    Stores recent conversation messages for the LLM.
    """

    def __init__(self, max_history: int = MAX_CHAT_HISTORY):
        self.messages = deque(maxlen=max_history)

    def add_user_message(self, message: str):
        self.messages.append({
            "role": "user",
            "content": message
        })

    def add_assistant_message(self, message: str):
        self.messages.append({
            "role": "assistant",
            "content": message
        })

    def get_messages(self) -> List[Dict]:
        return list(self.messages)

    def clear(self):
        self.messages.clear()

    def to_prompt(self) -> str:
        """
        Convert conversation into prompt format.
        """

        prompt = []

        for msg in self.messages:
            role = msg["role"].capitalize()
            prompt.append(f"{role}: {msg['content']}")

        return "\n".join(prompt)


memory = ConversationMemory()