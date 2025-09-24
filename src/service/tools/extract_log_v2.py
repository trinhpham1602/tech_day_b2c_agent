from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field
from datetime import datetime, timedelta
from typing import List, Optional
import pandas as pd
import numpy as np
from ..log_service import get_b2c_log

# ---------------------
# 1. Descriptions
# ---------------------
createdAtFrom_desc = """
'from' datetime. Format: YYYY-MM-DD HH:mm:ss
Nếu không tìm thấy thì mặc định là null
"""
createdAtTo_desc = """
'to' datetime. Format: YYYY-MM-DD HH:mm:ss
Nếu không tìm thấy thì mặc định là null
"""
serviceNames_desc = "Danh sách tên service (partner), ví dụ: ota_airline_vna"
actionNames_desc = "Danh sách action: book, search, calfare, reserve..."
actionTypes_desc = "Danh sách loại log: REQUEST_IN, RESPONSE_IN, REQUEST_PARTNER,RESPONSE_PARTNER..."

# ---------------------
# 2. Service name mapping
# ---------------------
SERVICE_MAP = {
    "vietnam airline": "ota_airline_vna",
    "vietnam airlines": "ota_airline_vna",
    "vietnam air": "ota_airline_vna",
    "vna": "ota_airline_vna",
    "vnair": "ota_airline_vna",
    "viet nam airline": "ota_airline_vna",
    "viet nam airlines": "ota_airline_vna",
    "vn air": "ota_airline_vna",
    "hãng vn": "ota_airline_vna",
    "tìm vé vietnam airline": "ota_airline_vna",
    "vé máy bay vietnam airline": "ota_airline_vna",
    "vietnam air line": "ota_airline_vna",
}


def normalize_service_names(names: Optional[List[str]]) -> List[str]:
    mapped = []
    for name in names or []:
        key = name.strip().lower()
        mapped.append(SERVICE_MAP.get(key, name))
    return mapped

# ---------------------
# 3. Input / Output schemas
# ---------------------


class LogParamsInput(BaseModel):
    userId: Optional[str] = Field(None, description="Số điện thoại user")
    createdAtFrom: Optional[datetime] = Field(
        None, description=createdAtFrom_desc)
    createdAtTo: Optional[datetime] = Field(None, description=createdAtTo_desc)
    serviceNames: List[str] = Field(
        default_factory=list, description=serviceNames_desc)
    actionNames: List[str] = Field(
        default_factory=list, description=actionNames_desc)
    actionTypes: List[str] = Field(
        default_factory=list, description=actionTypes_desc)


class LogParamsOutput(BaseModel):
    userId: Optional[str]
    createdAtFrom: str
    createdAtTo: str
    serviceNames: List[str]
    actionNames: List[str]
    actionTypes: List[str]

# ---------------------
# 4. Main tool function
# ---------------------


async def extract_log_params(
    createdAtFrom: Optional[datetime] = None,
    createdAtTo: Optional[datetime] = None,
    userId: Optional[str] = None,
    serviceNames: Optional[List[str]] = None,
    actionNames: Optional[List[str]] = None,
    actionTypes: Optional[List[str]] = None,
):

    # Normalize service names
    serviceNames = normalize_service_names(serviceNames)

    # Default time handling
    now = datetime.now()
    if createdAtFrom is None:
        createdAtFrom = now
    if createdAtTo is None:
        createdAtTo = now + timedelta(minutes=5)

    # If year < now.year, shift lên 2025
    if createdAtFrom < now:
        createdAtFrom = createdAtFrom.replace(year=2025)
    if createdAtTo < now:
        createdAtTo = createdAtTo.replace(year=2025)

    payload = LogParamsOutput(
        userId=userId,
        createdAtFrom=createdAtFrom.strftime("%Y-%m-%d %H:%M:%S"),
        createdAtTo=createdAtTo.strftime("%Y-%m-%d %H:%M:%S"),
        serviceNames=serviceNames,
        actionNames=actionNames or [],
        actionTypes=actionTypes or [],
    )

    print("✅ Normalized payload:", payload.model_dump())
    return get_b2c_log(payload=payload.model_dump())

# ---------------------
# 5. LangChain Tool
# ---------------------
extract_log_params_tool = StructuredTool.from_function(
    coroutine=extract_log_params,
    name="extract_log_params",
    description="Trích xuất tham số để gọi API log (phone, time range, partner/service, action, type)",
    args_schema=LogParamsInput,
    return_direct=True,
)
