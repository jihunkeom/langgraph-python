import logging
import time
import uuid
from typing import Any, Dict, Optional

from fastapi import Depends, FastAPI, Header
from fastapi.responses import JSONResponse, StreamingResponse

from llm_utils import get_llm_stream, get_llm_sync
from models import (
    DEFAULT_MODEL,
    ChatCompletionRequest,
    ChatCompletionResponse,
    Choice,
    MessageResponse,
)
from security import get_current_user
from tools import news_search_duckduckgo, tavily_search, web_search_duckduckgo

logger = logging.getLogger()
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

app = FastAPI()


@app.post("/chat/completions")
async def chat_completions(
    request: ChatCompletionRequest,
    X_IBM_THREAD_ID: Optional[str] = Header(
        None,
        alias="X-IBM-THREAD-ID",
        description="Optional header to specify the thread ID",
    ),
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    logger.info(
        f"Received POST /chat/completions ChatCompletionRequest: {request.json()}"
    )
    thread_id = ""
    if X_IBM_THREAD_ID:
        thread_id = X_IBM_THREAD_ID
    if request.extra_body and request.extra_body.thread_id:
        thread_id = request.extra_body.thread_id
    logger.info("thread_id: " + thread_id)
    model = DEFAULT_MODEL
    # if request.model:
    #     model = request.model
    # selected_tools = [web_search_duckduckgo, news_search_duckduckgo]
    selected_tools = [tavily_search]
    if request.stream:
        return StreamingResponse(
            get_llm_stream(request.messages, model, thread_id, selected_tools),
            media_type="text/event-stream",
        )
    else:
        last_message, all_messages = get_llm_sync(
            request.messages, model, thread_id, selected_tools
        )
        id = str(uuid.uuid4())
        response = ChatCompletionResponse(
            id=id,
            object="chat.completion",
            created=int(time.time()),
            # model=request.model,
            model=model,
            choices=[
                Choice(
                    index=0,
                    message=MessageResponse(role="assistant", content=last_message),
                    finish_reason="stop",
                )
            ],
        )
        return JSONResponse(content=response.dict())


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
