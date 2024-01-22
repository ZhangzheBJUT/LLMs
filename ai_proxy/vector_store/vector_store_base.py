from abc import ABC, abstractmethod
from typing import List
from langchain.docstore.document import Document

class VectorStoreBase(ABC):
    """base class for vector store database"""

    @abstractmethod
    def load_document(self, documents) -> None:
        """load document in vector database."""
        pass

    @abstractmethod
    def similar_search(self, text, topk) -> List[Document]:
        """similar search in vector database."""
        pass

    @abstractmethod
    def vector_name_exists(self, text, topk) -> None:
        """is vector store name exist."""
        pass
