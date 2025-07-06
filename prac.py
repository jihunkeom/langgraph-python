import asyncio
import json
import logging
import os
import time
import traceback
import uuid
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
from ibm_watsonx_ai import APIClient, Credentials
from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    HumanMessage,
    SystemMessage,
    ToolCall,
    ToolMessage,
)
from langchain_ibm import ChatWatsonx
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from config import (
    OPENAI_API_KEY,
    WATSONX_API_KEY,
    WATSONX_PROJECT_ID,
    WATSONX_SPACE_ID,
    WATSONX_URL,
)
from llm_utils import get_llm_stream
from models import (
    AIToolCall,
    ChatCompletionResponse,
    Choice,
    Function,
    Message,
    MessageResponse,
)
from token_utils import get_access_token
from tools import news_search_duckduckgo, tavily_search, web_search_duckduckgo

load_dotenv()

STATE_MODIFIER = "항상 한국어로만 대답하세요."
print(WATSONX_URL)

client_model_instance = APIClient(
    credentials=Credentials(url=WATSONX_URL, token=get_access_token(WATSONX_API_KEY)),
    project_id=WATSONX_PROJECT_ID,
)
model_instance = ChatWatsonx(
    model_id="meta-llama/llama-4-maverick-17b-128e-instruct-fp8",
    watsonx_client=client_model_instance,
)
graph = create_react_agent(
    model_instance,
    tools=[news_search_duckduckgo, web_search_duckduckgo],
    prompt=STATE_MODIFIER,
)


# 방법 1: 단순히 최종 결과만 받기
def simple_invoke():
    print("=== 방법 1: 단순 invoke ===")
    response = graph.invoke(
        {"messages": [{"role": "user", "content": "대한민국의 대통령은 누구인가요?"}]}
    )
    print("최종 답변:")
    print(response["messages"][-1].content)


# 방법 2: 중요한 이벤트만 필터링해서 출력
async def filtered_stream():
    print("\n=== 방법 2: 필터링된 스트림 ===")
    async for event in graph.astream_events(
        {"messages": [{"role": "user", "content": "대한민국의 대통령은 누구인가요?"}]},
        version="v2",
    ):
        kind = event["event"]
        if kind == "on_chat_model_stream":
            content = event["data"]["chunk"].content
            if content:
                print(content, end="", flush=True)
        elif kind == "on_tool_start":
            tool_name = event.get("name", "")
            print(f"\n🔍 도구 사용: {tool_name}")
        elif kind == "on_tool_end":
            print("✅ 도구 완료")


# 방법 3: llm_utils의 스트림 함수 사용
async def use_llm_utils():
    print("\n\n=== 방법 3: llm_utils 사용 ===")
    messages = [Message(role="user", content="대한민국의 대통령은 누구인가요?")]
    model = "meta-llama/llama-4-maverick-17b-128e-instruct-fp8"
    tools = [news_search_duckduckgo, web_search_duckduckgo]

    async for chunk in get_llm_stream(messages, model, "test-thread", tools):
        if chunk.strip():
            # JSON 파싱을 시도해서 content만 추출
            try:
                data = json.loads(
                    chunk.split("data: ")[1] if chunk.startswith("data: ") else chunk
                )
                if "choices" in data and data["choices"]:
                    delta = data["choices"][0].get("delta", {})
                    if "content" in delta:
                        print(delta["content"], end="", flush=True)
            except:
                pass


async def main():
    # 방법 1 실행
    simple_invoke()

    # 방법 2 실행
    await filtered_stream()

    # 방법 3 실행
    await use_llm_utils()


if __name__ == "__main__":
    asyncio.run(main())
