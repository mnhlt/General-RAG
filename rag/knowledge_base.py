from abc import ABC, abstractmethod
from typing import List
import chromadb
from chromadb.config import Settings

class KnowledgeBase(ABC):
    @abstractmethod
    def add_documents(self, documents: List[str]):
        pass

    @abstractmethod
    def update_documents(self, documents: List[str]):
        pass

    @abstractmethod
    def get_documents(self, query: str) -> List[str]:
        pass

class ChromaDBKnowledgeBase(KnowledgeBase):
    def __init__(self):
        self.client = chromadb.PersistentClient(path="./storage")
        try:
            self.collection = self.client.get_collection("knowledge_base")
        except:
            self.collection = self.client.create_collection("knowledge_base")

    def add_documents(self, documents: List[str]):
        # Add documents with unique IDs
        current_count = len(self.collection.get()['ids']) if self.collection.get()['ids'] else 0
        self.collection.add(
            documents=documents,
            ids=[f"doc_{current_count + i}" for i in range(len(documents))]
        )

    def update_documents(self, documents: List[str]):
        # For simplicity, we'll just add new documents
        self.add_documents(documents)

    def get_documents(self, query: str) -> List[str]:
        results = self.collection.query(
            query_texts=[query],
            n_results=5
        )
        return results['documents'][0] if results['documents'] else [] 