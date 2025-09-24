from langchain.prompts import ChatPromptTemplate
from langchain import hub
from langchain.agents import AgentExecutor, create_structured_chat_agent
from langchain_community.chat_models import ChatOllama

# Your existing tools
from .tools.extract_phone_tool import extract_phone_tool
from .tools.extract_datetime_tool import extract_datetime_tool
from .tools.extract_log_v2 import extract_log_params_tool
from .tools.extract_current_time import extract_current_time_tool


from pathlib import Path

tools = [extract_log_params_tool]
doc_text = """
Bạn là một AI agent hỗ trợ cho việc trích xuất các tham số để để gọi API lấy log từ database.
Các thuộc tính cần để trace log:
- userId: là số điện thoại của user (cũng được gọi là debitor hoặc user_id) 
- createdAtFrom: thời gian (ngày giờ) nếu format không đúng thì chỉnh lại cho đúng với format.
    Giá trị hợp lệ là thời gian phải trước giá trị của thuộc tính createdAtTo.
    format: YYYY-MM-DD'T'HH:mm:ss
    Nếu không tìm thấy thì giá trị mặt định là null
- createdAtTo thời gian (ngày giờ) nếu format không đúng thì chỉnh lại cho đúng với format.
    Giá trị hợp lệ là thời gian phải sau giá trị của thuộc tính createdAtFrom.
    format: YYYY-MM-DD'T'HH:mm:ss
    Nếu không tìm thấy thì giá trị mặt định là null
- serviceNames: là cách đặt tên của từng service, hay còn được gọi là các hãng, đối tác (partner) đôi khi có gắn thêm action như (search, api)
- actionNames: là tên gọi của action của api ví dụ như: booking, search, calfare, reserve, payment,...
- actionTypes: là loại log đầu ra đầu vào của của hệ thống. Ví dụ như request, response. khi đi qua từng service thường gắn thêm tiền tố đại diện cho service: ví dụ (partner_response, gateway_response)

Observation của những tool điều là dạng JSON và có thể parse được từ schema của nó 

Final Answer là một định dạng json
có các field sau:
  userId: str,
  createdAtFrom: datetime
  createdAtTo: datetime
  serviceNames: list[str] (không có thì trả về mãng rỗng)  
  actionNames: list[str] (không có thì trả về mãng rỗng)  
  actionTypes: list[str] (không có thì trả về mãng rỗng)
"""

# -----------------------
# 3. Create LLM
# -----------------------
llm = ChatOllama(
    model="sailor2",
    temperature=0,
    num_ctx=2048,
    num_gpu=10
)
base_prompt = hub.pull("hwchase17/structured-chat-agent")
custom_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            f"You are an assistant with the following background knowledge:n{doc_text}nn"
            "Always use this information when relevant."
        ),
        *base_prompt.messages,
    ]
)
agent = create_structured_chat_agent(llm, tools, custom_prompt)

agent_instance = AgentExecutor(agent=agent, tools=tools, verbose=True)
