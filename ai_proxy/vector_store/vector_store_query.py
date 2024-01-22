import os,shutil

from vector_store.chroma_store import ChromaStore
from langchain.document_loaders import TextLoader
from langchain.docstore.document import Document
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
import sentence_transformers

from singleton import Singleton
from log.logs import logger
from configs.config import Config

"""Chroma文档：https://docs.trychroma.com/getting-started
"""

class VectorStoreQuery(metaclass=Singleton):

    DOC_SEPARATOR_INNER = '##'
    DOC_SEPARATOR_OUTER = '\n'

    def __init__(self, doc_file_path: str,
                 vector_persist_path: str,
                 vector_store_name: str,
                 model_name: str,
                 is_store_override: bool = True):

        self._doc_file_path = doc_file_path
        self._vector_store_name = vector_store_name
        self._vector_persist_path = vector_persist_path
        self._model_name = model_name

        if os.path.exists(os.path.join(vector_persist_path, vector_store_name + ".vectordb")) and is_store_override:
            shutil.rmtree(os.path.join(vector_persist_path, vector_store_name + ".vectordb"))

        embeddings = HuggingFaceEmbeddings(model_name=model_name)
        embeddings.client = sentence_transformers.SentenceTransformer(embeddings.model_name)

        self.chroma_store = ChromaStore(embeddings, vector_persist_path, vector_store_name)
        self._generate_doc()

    def _generate_doc(self) -> int:

        if not os.path.exists(self._doc_file_path):
            logger.error(f"{self._doc_file_path} not exist")
            return 0

        loader = TextLoader(self._doc_file_path)
        lines = loader.load()
        if len(lines) <= 0:
            logger.error(f"{self._doc_file_path} is empty.")
            return 0

        docs = lines[0].page_content.split(self.DOC_SEPARATOR_OUTER)
        documents = []
        for doc in docs:
            key_value = doc.split(self.DOC_SEPARATOR_INNER, maxsplit=3)
            if len(key_value) == 3:
                document = Document(page_content=key_value[1],
                                    metadata={'theme': key_value[0], 'detail': key_value[2]})
                documents.append(document)

        logger.info(f"====== split doc done, size = {len(documents)} ======")
        self.chroma_store.load_document(documents)

        return len(documents)

    def similarity_result(self, query: str) -> str:
        similar_docs = self.chroma_store.similar_search(query, 3)
        detail = ''
        if len(similar_docs) >= 1:
            detail = similar_docs[0][0].metadata.get('detail')

        logger.debug(f"local search query={query}, result={similar_docs},")
        return detail


CFG = Config()
vector_store_query = VectorStoreQuery(CFG.doc_file_path, CFG.vector_persist_path,CFG.vector_store_name, CFG.model_name)

if __name__ == '__main__':
    vector_store_query = VectorStoreQuery('../doc_data/docs.txt', '../doc_data/umeng_doc_vector', 'uapp_v1',
                                          '/ai/models/sentence_transformers/shibing624_text2vec-base-chinese')
    length = vector_store_query._generate_doc()
    print(f"doc length = {length}.")

    result = vector_store_query.similarity_result('是否支持返还到自建的kafka')
    print(result)

