# app/core/vector_memory.py

from datetime import datetime

try:
    import chromadb
except ImportError:
    chromadb = None


class VectorMemory:
    """
    ChromaDB vector memory layer

    Responsibilities:
    - semantic memory retrieval
    - long-term contextual recall
    - similarity search
    - persistent memory upgrade from JSON storage

    Fallback behavior:
    if ChromaDB is unavailable,
    system safely degrades without crashing
    """

    def __init__(self):
        self.enabled = chromadb is not None
        self.collection_name = "agent_memory"

        if self.enabled:
            self.client = chromadb.PersistentClient(
                path="app/database/chroma"
            )

            self.collection = self.client.get_or_create_collection(
                name=self.collection_name
            )
        else:
            self.client = None
            self.collection = None

    def add_memory(
        self,
        user_input: str,
        assistant_response: str
    ):
        """
        Store semantic interaction memory
        """

        if not self.enabled:
            return

        memory_text = (
            f"User: {user_input}\n"
            f"Assistant: {assistant_response}"
        )

        memory_id = datetime.utcnow().isoformat()

        try:
            self.collection.add(
                documents=[memory_text],
                ids=[memory_id],
                metadatas=[{
                    "type": "conversation"
                }]
            )
        except Exception:
            pass

    def search_memory(
        self,
        query: str,
        limit: int = 5
    ) -> str:
        """
        Semantic similarity lookup
        """

        if not self.enabled:
            return "Vector memory unavailable."

        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=limit
            )

            documents = results.get(
                "documents",
                [[]]
            )[0]

            if not documents:
                return "No semantic memory found."

            return "\n\n".join(documents)

        except Exception:
            return "Vector memory lookup failed."
