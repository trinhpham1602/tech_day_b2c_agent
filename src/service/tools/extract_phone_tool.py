import re
from typing import Optional
from pydantic import BaseModel, Field
from langchain.tools import StructuredTool
import json



PHONE_REGEX = re.compile(r"(\+?\d[\d\s\-]{7,15}\d)")


def validate_phone(phone: str) -> bool:
    digits = re.sub(r"\D", "", phone)
    return 8 <= len(digits) <= 15

class PhoneInput(BaseModel):
    user_input: Optional[str] = Field(None, description="Văn bản do người dùng nhập vào để trích xuất số điện thoại")


class PhoneOutput(BaseModel):
    target: Optional[str] = Field(
        None, description="Số điện thoại hợp lệ (nếu bắt đầu là +84 thì chuyển thành kiểu 10 số) nếu tìm thấy")
    suggestion: Optional[str] = Field(
        None, description="Gợi ý nếu số không hợp lệ hoặc không tìm thấy")


async def extract_phone(user_input: str) -> dict:
    match = PHONE_REGEX.search(user_input)
    if not match:
        return PhoneOutput(
            target=None,
            suggestion="Không tìm thấy số điện thoại. Vui lòng nhập số hợp lệ."
        ).model_dump()

    phone = match.group(1).strip()
    if validate_phone(phone):
        return PhoneOutput(target=phone, suggestion=None).model_dump()
    else:
        return PhoneOutput(
            target=None,
            suggestion=f"Số '{phone}' không hợp lệ. Hãy nhập theo định dạng: +84123456789 hoặc 0912345678."
        ).model_dump()


extract_phone_tool = StructuredTool.from_function(
    coroutine=extract_phone,
    name="extract_phone",
    description="Trích xuất và kiểm tra số điện thoại Việt Nam từ văn bản người dùng. Trả về số hợp lệ (+84...) hoặc gợi ý.",
    args_schema=PhoneInput,
    return_direct=True
)
