from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field, field_validator
from datetime import datetime, timedelta
from typing import Optional, List
from .extract_datetime_tool import extract_datetime_tool
from .extract_phone_tool import extract_phone_tool
import asyncio
import json
from ..log_service import get_log
import pandas as pd

class ExtraInfoInput(BaseModel):
    field: str
    

class LogParamsOutput(BaseModel):
    serviceNames: list[str] = Field(None)
    actionNames: list[str] = Field(None)
    actionTypes: list[str] = Field(None)
    createdAtFrom: str = Field(None)
    createdAtTo: str = Field(None)
    userId: str = Field(None)


async def extract_extra_data(field: str):
    # fareGroup
    df = pd.read_json("src/service/tools/log_result.json")
    result = df["data"].map(lambda x: x["content"][field])
    print(result)
    return {"data": result.to_dict()}

extract_extra_data_tool = StructuredTool.from_function(
    coroutine=extract_extra_data,
    name="extract_extra_data",
    description=f"Trích xuất một số field cụ thể như, bookingCode,... và đưa chúng vào một danh sách",
    args_schema=ExtraInfoInput,
    return_direct=True
)
