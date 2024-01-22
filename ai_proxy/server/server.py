from fastapi import FastAPI, Request, Query
from log.logs import logger
from configs.config import Config
import uvicorn

import utils

app = FastAPI()
CFG = Config()

@app.post("/generate")
async def generate(request: Request):
    json_post_raw = await request.json()
    resp = utils.dingtalk_result(json_post_raw)
    return resp

@app.get("/updatedoc")
async def generate():
    return f'update doc:{utils.update_vector_store()} lines.'

@app.get("/test")
async def local(query=Query(None)):
    return f'answer:{utils.answer(query)}.'

@app.get("/local")
async def local(query=Query(None)):
    return f'answer:{utils.local_test(query)}.'

@app.get("/llm")
async def llm(query=Query(None)):
    return f'answer:{utils.bailian_handler(query)}.'


@app.get("/hello")
async def index():
    return {"message": "Hello World"}

if __name__ == "__main__":
    logger.info("ai proxy start...")
    uvicorn.run("server:app", host="0.0.0.0", port=CFG.WEB_SERVER_PORT, reload=True, log_level="info")