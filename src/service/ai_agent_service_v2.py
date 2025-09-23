from langchain.output_parsers import PydanticOutputParser, OutputFixingParser
from langchain import hub
from langchain.tools import StructuredTool
from langchain.agents import AgentExecutor, create_structured_chat_agent
from pydantic import BaseModel, Field
import re
import asyncio
from langchain_community.chat_models import ChatOllama
from langchain.agents import initialize_agent, AgentType, Tool
from langchain.tools import Tool
from .tools.extract_phone_tool import extract_phone_tool
from .tools.extract_datetime_tool import extract_datetime_tool
from .tools.extract_log import extract_log_params_tool
from .tools.extract_log_v2 import extract_log_params_tool as extract_log_params_tool_v2

import json

tools = [extract_log_params_tool_v2, extract_phone_tool,
         extract_datetime_tool]

# tools = [extract_phone_tool,
#          extract_datetime_tool]

llm = ChatOllama(
    model="qwen2.5",
    temperature=0,
    num_ctx=2048,  # context window size
)
prompt = hub.pull("hwchase17/structured-chat-agent")

agent = create_structured_chat_agent(llm, tools, prompt)

agent_instance = AgentExecutor(
    agent=agent, tools=tools, verbose=True)
