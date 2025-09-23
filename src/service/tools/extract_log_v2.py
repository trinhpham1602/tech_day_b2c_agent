from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field, field_validator
from datetime import datetime, timedelta
from typing import Optional, List
from .extract_datetime_tool import extract_datetime_tool
from .extract_phone_tool import extract_phone_tool
import asyncio
import json
from ..log_service import get_log


createdAtFrom_desc = """
    'từ' (from) thời gian (ngày giờ) nếu format không đúng thì chỉnh lại cho đúng với format.
    Giá trị hợp lệ là thời gian phải trước giá trị của thuộc tính to_datetime.
    Giá trị trích xuất được giữ nguyên ở giờ
    format: YYYY-MM-DD HH:mm:ss 
    Nếu không tìm thấy thì giá trị mặt định là null
"""
createdAtTo_desc = """
    'đến' (to) thời gian (ngày giờ) nếu format không đúng thì chỉnh lại cho đúng với format.
    Giá trị hợp lệ là thời gian phải sau giá trị của thuộc tính from_datetime.
    Giá trị trích xuất được giữ nguyên ở giờ
    format: YYYY-MM-DD HH:mm:ss
    Nếu không tìm thấy thì giá trị mặt định là null
"""

serviceNames_desc = """
    là cách đặt tên của từng service, hay còn được gọi là các hãng (partner) đôi khi có gắn thêm action như (search, api)
"""
actionNames_desc = """
    là tên gọi của action của api ví dụ như: booking, search, calfare, reserve, payment,...
"""
actionTypes_desc = """
    là loại log đầu ra đầu vào của của hệ thống. Ví dụ như request, response. khi đi qua từng service thường gắn thêm tiền tố đại diện cho service: ví dụ(partner_response, gateway_response)
"""


class LogParamsInput(BaseModel):
    userId: str = Field(None,
                        description=f"Trích xuất số điện thoại từ câu mà user nhập")
    createdAtFrom: datetime = Field(None,
                                    description=f"Trích xuất {createdAtFrom_desc}")
    createdAtTo: datetime = Field(None,
                                  description=f"Trích xuất {createdAtTo_desc}")
    serviceNames: list[str] = Field(
        default_factory=list, description=f"Trích xuất {serviceNames_desc}")
    actionNames: list[str] = Field(
        default_factory=list, description=f"Trích xuất {actionNames_desc}")
    actionTypes: list[str] = Field(
        default_factory=list, description=f"Trích xuất {actionTypes_desc}")
    

class LogParamsOutput(BaseModel):
    serviceNames: list[str] = Field(None)
    actionNames: list[str] = Field(None)
    actionTypes: list[str] = Field(None)
    createdAtFrom: str = Field(None)
    createdAtTo: str = Field(None)
    userId: str = Field(None)

async def extract_log_params(createdAtFrom: datetime = None,
                             createdAtTo: datetime = None,
                             userId: str = None,
                             serviceNames: List[str] = [],
                             actionNames: List[str] = [],
                             actionTypes: List[str] = [],
                             ):
    try:
        now = datetime.now()
        if createdAtFrom is None:
            createdAtFrom = now

        if createdAtTo is None:
            createdAtTo = now + timedelta(minutes=5)
        # format
        createdAtFromStr = createdAtFrom.strftime("%Y-%m-%d %H:%M:%S")
        createdAtToStr = createdAtTo.strftime("%Y-%m-%d %H:%M:%S")
        payload = LogParamsOutput(
            serviceNames=serviceNames,
            actionNames=actionNames,
            actionTypes=actionTypes,
            createdAtFrom=createdAtFromStr,
            createdAtTo=createdAtToStr,
            userId=userId
        )
    
        return get_log(payload)

    except Exception:
        return {"start_hour": None, "end_hour": None, "day": None, "suggestion": "Không parse được thời gian"}

extract_log_params_tool = StructuredTool.from_function(
    coroutine=extract_log_params,
    name="extract_log_params",
    description=f"Trích xuất cái giá trị tham số bao gồm số điện thoại, ngày bắt đầu, ngày kết thúc, đối tác (nếu có), thao tác (nếu có), loại log (nếu có) từ câu mà user nhập",
    args_schema=LogParamsInput,
    return_direct=True
)
