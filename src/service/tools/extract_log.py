from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

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


class LogParamsInput(BaseModel):
    phone_number: Optional[str] = Field(None,
                              description="Trích xuất và kiểm tra số điện thoại Việt Nam từ văn bản người dùng. Trả về số hợp lệ (+84...) hoặc gợi ý.")
    from_datetime: Optional[datetime] = Field(None,
                                              description=from_datetime_desc)
    to_datetime: Optional[datetime] = Field(None,
                                            description=to_datetime_desc)

async def extract_log_params(phone_number: Optional[str],
                             from_datetime: Optional[datetime],
                             to_datetime: Optional[datetime],
                             ) -> dict:
    try:
        
        return {"phone_number": phone_number,
                "from_datetime": from_datetime,
                "to_datetime": to_datetime, 
                }
    except Exception:
        return {"start_hour": None, "end_hour": None, "day": None, "suggestion": "Không parse được thời gian"}

extract_log_params_tool = StructuredTool.from_function(
    coroutine=extract_log_params,
    name="extract_log_params",
    description=f"Trích xuất cái giá trị tham số bao gồm số điện thoại, {from_datetime_desc} {to_datetime_desc}, từ câu mà user nhập",
    args_schema=LogParamsInput,
    return_direct=True
)
