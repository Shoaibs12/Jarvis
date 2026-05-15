import sqlite3
import os

class MemoryManager:
    def __init__(self, db_path="database/jarvis_memory.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS memory (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    topic TEXT NOT NULL,
                    information TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()

    def store_memory(self, topic: str, information: str) -> str:
        """
        Stores important user preferences, habits, or context for long-term memory.

        Args:
            topic: The category or subject of the memory (e.g., 'user_name', 'favorite_ide').
            information: The detail to remember.
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO memory (topic, information) VALUES (?, ?)",
                    (topic, information)
                )
                conn.commit()
            return f"Successfully stored memory under topic '{topic}'."
        except Exception as e:
            return f"Failed to store memory: {e}"

    def retrieve_memory(self, topic: str) -> str:
        """
        Retrieves long-term memory information regarding a specific topic.

        Args:
            topic: The category or subject of the memory to fetch.
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT information FROM memory WHERE topic LIKE ? ORDER BY timestamp DESC",
                    (f"%{topic}%",)
                )
                results = cursor.fetchall()
                if results:
                    return "\n".join([r[0] for r in results])
                return "No memory found for that topic."
        except Exception as e:
            return f"Failed to retrieve memory: {e}"

    def get_all_context(self) -> str:
        """
        Fetches a summary of all recent memories to inject into the system prompt.
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT topic, information FROM memory ORDER BY timestamp DESC LIMIT 20")
                results = cursor.fetchall()
                if not results:
                    return "No prior context available."
                context = "Relevant User Context/Memory:\n"
                for topic, info in results:
                    context += f"- {topic}: {info}\n"
                return context
        except Exception as e:
            return ""
