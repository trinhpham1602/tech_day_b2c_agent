from fastapi import FastAPI, APIRouter
import uvicorn
from src.routers.recieve_prompt_router import router as recieve_prompt_router
from fastapi.middleware.cors import CORSMiddleware

import asyncio

agent_app = FastAPI()


# Allow all origins
agent_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

agent_app.include_router(recieve_prompt_router)

if __name__ == "__main__":
    uvicorn.run(app=agent_app, reload=True)
