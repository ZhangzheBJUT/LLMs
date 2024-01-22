import json

from dingtalkchatbot.chatbot import DingtalkChatbot
from model.broadscope_bailian_llm import BroadscopeBailian
from configs.config import Config
from log.logs import logger
from vector_store.vector_store_query import vector_store_query

CFG = Config()

def update_vector_store() -> int:
    return vector_store_query._generate_doc()


def local_store_handler(prompt: str) -> str:
    return vector_store_query.similarity_result(prompt)

def bailian_handler(prompt: str) -> str:

    llm = BroadscopeBailian(access_key_id=CFG.access_key_id,
                            access_key_secret=CFG.access_key_secret,
                            agent_key=CFG.agent_key,
                            app_id=CFG.app_id) 

    res = llm(prompt=prompt)  #history=chat_history

    return res

def answer(prompt: str) -> str:
    # get llm result
    result = local_store_handler(prompt)
    if result == '':
        logger.info("local vector store not match.")
        result = bailian_handler(prompt) + ' (来自：通义千问 + 知识库)'
    else:
        result = result + ' (来自：本地知识库)'

    return result

def dingtalk_result(request_json_raw_data: dict) -> str:
    json_post = json.dumps(request_json_raw_data)
    json_post_list = json.loads(json_post)

    prompt = json_post_list.get('text').get('content')

    result = answer(prompt)

    # return final result
    session_webhook = json_post_list.get('sessionWebhook')

    logger.debug(f'session_webhook:{session_webhook},prompt:{prompt},result={result}')

    dingtalk_chatbot = DingtalkChatbot(session_webhook)
    resp = dingtalk_chatbot.send_markdown(title='智能助手', text=result)
    return resp

def local_test(prompt: str) -> str:
    result = local_store_handler(prompt)
    if result == '':
        logger.info("local vector store not match.")
        result = bailian_handler(prompt)

    return result

if __name__ == '__main__':
    prompt = '你好,介绍下自己'

    update_vector_store()
    resp = local_store_handler(prompt)
    print(resp)