import os
from typing import Any, List, Tuple

from langchain.vectorstores import Chroma
from langchain.docstore.document import Document

from log.logs import logger
from vector_store.vector_store_base import VectorStoreBase


class ChromaStore(VectorStoreBase):
    """chroma database"""

    def __init__(self, embeddings: Any, chroma_persist_path: str , vector_store_name:str ) -> None:
        self.embeddings = embeddings
        self.persist_dir = os.path.join(
            chroma_persist_path, vector_store_name + ".vectordb"
        )
        self.vector_store_client = Chroma(
            persist_directory=self.persist_dir, embedding_function=self.embeddings
        )

    def similar_search(self, text, topk) -> List[Tuple[Document,float]]:
        logger.info("ChromaStore similar search")
        return self.vector_store_client.similarity_search_with_score(text, topk)

    def vector_name_exists(self) -> bool:
        return (
            os.path.exists(self.persist_dir) and len(os.listdir(self.persist_dir)) > 0
        )

    def load_document(self, documents):
        logger.info("ChromaStore load document")
        texts = [doc.page_content for doc in documents]
        metadatas = [doc.metadata for doc in documents]
        ids = self.vector_store_client.add_texts(texts=texts, metadatas=metadatas)
        self.vector_store_client.persist()
        return ids

    def delete_by_ids(self, ids):
        collection = self.vector_store_client._collection
        collection.delete(ids=ids)
