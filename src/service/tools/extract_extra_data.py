from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field, field_validator
from datetime import datetime, timedelta
from typing import Optional, List
from .extract_datetime_tool import extract_datetime_tool
from .extract_phone_tool import extract_phone_tool
import asyncio
import json
from ..log_service import get_log


class ExtraInfoInput(BaseModel):
    field: str
    

class LogParamsOutput(BaseModel):
    serviceNames: list[str] = Field(None)
    actionNames: list[str] = Field(None)
    actionTypes: list[str] = Field(None)
    createdAtFrom: str = Field(None)
    createdAtTo: str = Field(None)
    userId: str = Field(None)

async def extract_extra_data(user_input):
    try:
        return get_log(user_input)

    except Exception:
        return {"start_hour": None, "end_hour": None, "day": None, "suggestion": "Không parse được thời gian"}

extract_extra_data_tool = StructuredTool.from_function(
    coroutine=extract_extra_data,
    name="extract_extra_data",
    description=f"Sau khi response từ một tool thì trích xuất thêm thông tin liên quan tới field đó nếu user yêu cầu",
    args_schema=ExtraInfoInput,
    return_direct=True
)
