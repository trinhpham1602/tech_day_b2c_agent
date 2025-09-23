from typing import Optional
from pydantic import BaseModel, Field
from langchain.tools import StructuredTool, Tool

from datetime import datetime


from_datetime_desc = """
    'từ' (from) thời gian (ngày giờ) nếu format không đúng thì chỉnh lại cho đúng với format.
    Giá trị hợp lệ là thời gian phải trước giá trị của thuộc tính to_datetime.
    Nếu không tìm thấy thì phải dùng giá trị của hàm datetime.now() của python.
    format: YYYY-MM-DD HH:mm:ss
"""
to_datetime_desc = """
    'đến' (to) thời gian (ngày giờ) nếu format không đúng thì chỉnh lại cho đúng với format.
    Giá trị hợp lệ là thời gian phải sau giá trị của thuộc tính from_datetime.
    Nếu không tìm thấy thì phải dùng giá trị của hàm datetime.now() của python + 5phút.
    format: YYYY-MM-DD HH:mm:ss
"""


class DatetimeInput(BaseModel):
    observation_str: str = Field(
        None, description="Giá trị trích xuất thời gian")
    

class DatetimeOutput(BaseModel):
    from_datetime: Optional[str] = Field(
        None, description="Ngày giờ bắt đầu có định dạng (format) là: YYYY-MM-DD HH:mm:ss, có thời gian UTC nhỏ hơn giá trị của to_datetime (nếu tìm thấy)")
    to_datetime: Optional[str] = Field(
        None, description="giá trị ngày giờ chặn trên có định dạng (format) là: YYYY-MM-DD HH:mm:ss, có thời gian UTC lớn hơn giá trị của from_datetime (nếu tìm thấy)")
    

async def extract_datetime(observation_str: str) -> dict:
    return {}


extract_datetime_tool = StructuredTool.from_function(
    coroutine=extract_datetime,
    name="extract_datetime",
    description=f"Trích xuất được khoảng thời gian {from_datetime_desc} {to_datetime_desc} dưới dạng JSON hoặc dict trong python từ văn bản user nhập",
    args_schema=DatetimeInput,
    return_direct=True
)
