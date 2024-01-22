from alibabacloud_bailian20230601.client import Client
from alibabacloud_bailian20230601.models import CreateTextEmbeddingsRequest
from alibabacloud_tea_openapi.models import Config

import broadscope_bailian
from configs.config import Config as MyConfig
from typing import List

CFG = MyConfig()


def createEmbedding(input : List[str]) -> List[List[float]]:

    config = Config(access_key_id=CFG.access_key_id,
                    access_key_secret=CFG.access_key_secret,
                    endpoint=broadscope_bailian.pop_endpoint)

    client = Client(config=config)

    request = CreateTextEmbeddingsRequest(agent_key=CFG.agent_key,
                                          input=input,
                                          text_type="query")
    response = client.create_text_embeddings(request=request)
    if response.status_code != 200 or response.body is None:
        raise RuntimeError("create token error, code=%d" % response.status_code)

    body = response.body
    # if not body.success:
    #     raise RuntimeError("create token error, code=%s, message=%s" % (body.code, body.message))
    #
    # for embedding in body.data.embeddings:
    #     print("index: %s, embeddings: %s\n" % (embedding.text_index, embedding.embedding))

    res = [x.embedding for x in body.data.embeddings]
    print(res)

    return res


#   createEmbedding(input = ["今天天气怎么样", "我想去北京"])

    # list[float][float]
    # x = [for embedding in body.data.embeddings]
    #
    # for r in range(M):
    #     print(x[r])
    #
    # return body.data.embeddings

import chromadb
from chromadb.api.types import Documents, EmbeddingFunction, Embeddings


class MyEmbeddingFunction(EmbeddingFunction):
    def __call__(self, texts: Documents) -> Embeddings:
        #embeddings = [model.encode(x) for x in texts]
        embeddings = createEmbedding(texts)
        return embeddings

chroma_client = chromadb.PersistentClient('./test_chroma')
collection = chroma_client.get_or_create_collection(name="my_collection", embedding_function=MyEmbeddingFunction())
# collection.add(
#     documents=["统计分析事件行为路径分析功能介绍，在什么场景下使用事件行为路径分析","统计分析事件行为路径分析如何使用，请详细说明操作步骤","U-App 统计分析留存分析功能介绍，如何使用"], # we handle tokenization, embedding, and indexing automatically. You can skip that and add your own embeddings as well
#     metadatas=[{"source": "notion"}, {"source": "google-docs"},{"source": "notion1"}], # filter on these!
#     ids=["doc1", "doc2","doc3"], # unique for each doc
# )
results = collection.query(
    query_texts=["讲解下行为路径分析功能"],
    n_results=3,
    # where={"metadata_field": "is_equal_to_this"}, # optional filter
)

print(results)
