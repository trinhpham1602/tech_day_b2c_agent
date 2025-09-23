import re
from typing import Optional
from pydantic import BaseModel, Field
from langchain.tools import StructuredTool
import json
from datetime import datetime


class CurrentTimeInput(BaseModel):
    user_input: Optional[str] = Field(
        None, description="Văn bản do người dùng nhập vào để trích xuất thời gian hiện tại")


class CurrentTimeOutput(BaseModel):
    now: Optional[str] = Field(
        None, description="giá trị ngày giờ hiện tại")
    suggestion: Optional[str] = Field(
        None, description="Gợi ý nếu số không hợp lệ hoặc không tìm thấy")


async def extract_current_time(user_input: str) -> dict:
    print("aloooooooooooooooooooooo")
    now = datetime.now()
    from_datetime = now.strftime("%Y-%m-%d %H:%M:%S")
    return CurrentTimeOutput(now=from_datetime).model_dump()

extract_current_time_tool = StructuredTool.from_function(
    coroutine=extract_current_time,
    name="extract_current_time",
    description="Trích xuất thời gian hiện tại của của câu truy vấn từ người dùng nếu không cung cấp ngày giờ cụ thể",
    args_schema=CurrentTimeInput,
    return_direct=True
)
