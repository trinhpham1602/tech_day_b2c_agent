from langchain_community.chat_models import ChatOllama
from langchain.agents import initialize_agent, AgentType, Tool
from langchain.tools import Tool
from .tools.extract_phone_tool import extract_phone_tool
from .tools.extract_datetime_tool import extract_datetime_tool
from .tools.extract_log import extract_log_params_tool

tools = [extract_log_params_tool]

class LogAIagent():
    model = None
    tools = []
    agent_type = None

    def __init__(self, model, tools, agent_type):
        self.tools = tools
        self.model = model
        self.agent_type = agent_type

    def add_tools(self, tools: list[Tool]) -> None:
        self.tools.append(*tools)

    def build_log_agent(self):
        log_agent = initialize_agent(
            tools=self.tools,
            llm=self.model,
            agent=self.agent_type,
            verbose=True
        )

        return log_agent


_model = ChatOllama(model="sailor2", temperature=0, num_gpu=8, num_ctx=4096)
_log_agent_skeleton = LogAIagent(
    model=_model, tools=tools, agent_type=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION)

agent_instance = _log_agent_skeleton.build_log_agent()
