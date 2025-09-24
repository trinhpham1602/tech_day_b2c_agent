from pydantic import BaseModel
from fastapi import APIRouter
from ..service.ai_agent_service import agent_instance
from ..service.ai_agent_service_v2 import agent_instance as agent_instance_v2
from ..service.ai_agent_service_v3 import agent_instance as agent_instance_v3
from langchain.prompts import ChatPromptTemplate
import json

router = APIRouter()

# Request model
class PromptRequest(BaseModel):
    prompt: str


@router.post("/agent/chat")
async def run_agent(req: PromptRequest):
    result = await agent_instance_v3.ainvoke({"input": req.prompt})
    return result
