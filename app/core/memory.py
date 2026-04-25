# app/core/memory.py

import json
import os
from datetime import datetime
from app.config import settings


class MemoryManager:
    """
    Persistent memory layer

    Responsibilities:
    - store interaction history
    - retrieve relevant context
    - maintain lightweight persistence
    - prepare future upgrade path to ChromaDB
    """

    def __init__(self):
        self.memory_file = settings.MEMORY_FILE
        self.max_context_items = 10

        self._ensure_memory_file()

    def _ensure_memory_file(self):
        """
        Create memory store if missing
        """

        directory = os.path.dirname(self.memory_file)

        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)

        if not os.path.exists(self.memory_file):
            with open(self.memory_file, "w", encoding="utf-8") as f:
                json.dump([], f, indent=2)

    def _load_memory(self) -> list:
        """
        Load stored interaction history
        """

        try:
            with open(self.memory_file, "r", encoding="utf-8") as f:
                return json.load(f)

        except Exception:
            return []

    def _save_memory(self, data: list):
        """
        Persist memory safely
        """

        try:
            with open(self.memory_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

        except Exception:
            pass

    def retrieve_context(
        self,
        user_input: str = ""
    ) -> str:
        """
        Retrieve recent contextual memory

        Later:
        this becomes vector similarity search
        via ChromaDB
        """

        memory = self._load_memory()

        if not memory:
            return "No prior memory available."

        recent_items = memory[-self.max_context_items:]

        formatted = []

        for item in recent_items:
            user = item.get("user_input", "")
            response = item.get("assistant_response", "")

            formatted.append(
                f"User: {user}\nAssistant: {response}"
            )

        return "\n\n".join(formatted)

    def store_interaction(
        self,
        user_input: str,
        assistant_response: str,
        plan: dict = None,
        reflection: str = None
    ):
        """
        Store interaction after execution
        """

        memory = self._load_memory()

        record = {
            "timestamp": datetime.utcnow().isoformat(),
            "user_input": user_input,
            "assistant_response": assistant_response,
            "plan": plan or {},
            "reflection": reflection or ""
        }

        memory.append(record)

        # Prevent unbounded growth
        if len(memory) > 1000:
            memory = memory[-1000:]

        self._save_memory(memory)

    def clear_memory(self):
        """
        Manual reset utility
        """

        self._save_memory([])
