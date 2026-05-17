import chromadb
import os
import uuid
import datetime
from core.logger import get_logger

logger = get_logger("MemoryManager")

class MemoryManager:
    def __init__(self, db_path="database/chroma_db"):
        self.db_path = db_path
        os.makedirs(self.db_path, exist_ok=True)
        try:
            self.client = chromadb.PersistentClient(path=self.db_path)
            # Create or get the collection
            self.collection = self.client.get_or_create_collection(
                name="jarvis_memory",
                metadata={"hnsw:space": "cosine"} # Default L2, cosine is fine for semantic
            )
            logger.info("ChromaDB MemoryManager initialized.")
        except Exception as e:
            logger.error(f"Failed to initialize ChromaDB: {e}")
            self.client = None
            self.collection = None

    def store_memory(self, topic: str, information: str) -> str:
        """
        Stores important user preferences, habits, or context as a semantic vector in ChromaDB.
        """
        if not self.collection:
            return "Memory storage is offline."

        try:
            mem_id = str(uuid.uuid4())
            timestamp = datetime.datetime.now().isoformat()

            # For ChromaDB, we embed the information (or a combination of topic and information)
            # ChromaDB uses a default all-MiniLM-L6-v2 embedding model automatically if none provided.
            self.collection.add(
                documents=[information],
                metadatas=[{"topic": topic, "timestamp": timestamp}],
                ids=[mem_id]
            )
            logger.info(f"Stored memory: [{topic}] {information}")
            return f"Successfully stored memory under topic '{topic}'."
        except Exception as e:
            logger.error(f"Failed to store memory: {e}")
            return f"Failed to store memory: {e}"

    def retrieve_memory(self, topic: str) -> str:
        """
        Retrieves long-term memory information regarding a specific topic using semantic search.
        """
        if not self.collection:
            return "Memory retrieval is offline."

        try:
            # Semantic search querying the topic
            results = self.collection.query(
                query_texts=[topic],
                n_results=3
            )

            if results and results['documents'] and results['documents'][0]:
                retrieved_docs = results['documents'][0]
                return "\n".join(retrieved_docs)

            return "No memory found for that topic."
        except Exception as e:
            logger.error(f"Failed to retrieve memory: {e}")
            return f"Failed to retrieve memory: {e}"

    def get_all_context(self) -> str:
        """
        Fetches recent memories to inject into the system prompt.
        """
        if not self.collection:
            return "No prior context available."

        try:
            # ChromaDB currently doesn't easily support "fetch all ordered by time" via basic query without custom metadata filtering.
            # As a fallback, we fetch the most recent items.
            results = self.collection.get(
                limit=10
            )

            if not results or not results['documents']:
                return "No prior context available."

            context = "Relevant User Context/Memory:\n"
            for doc, meta in zip(results['documents'], results['metadatas']):
                topic = meta.get("topic", "General")
                context += f"- {topic}: {doc}\n"
            return context
        except Exception as e:
            logger.error(f"Failed to get context: {e}")
            return ""
