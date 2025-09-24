from pydantic import BaseModel, Field
import pandas as pd
from ..client.http_client import get_b2c_log

class LogParamsOutput(BaseModel):
    serviceNames: list[str] = Field(None)
    actionNames: list[str] = Field(None)
    actionTypes: list[str] = Field(None)
    createdAtFrom: str = Field(None)
    createdAtTo: str = Field(None)
    userId: str = Field(None)


def get_log():
  return get_b2c_log()
