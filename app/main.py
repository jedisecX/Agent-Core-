# app/main.py

from fastapi import FastAPI
from pydantic import BaseModel

from app.config import settings
from app.core.agent import AgentCore


app = FastAPI(
    title=settings.APP_NAME,
    description="Autonomous AI Agent Runtime",
    version="1.0.0"
)

agent = AgentCore()


class UserRequest(BaseModel):
    """
    Incoming API request body
    """
    message: str


@app.get("/")
def root():
    """
    Health + identity check
    """
    return {
        "service": settings.APP_NAME,
        "status": "online",
        "model": settings.MODEL_NAME,
        "environment": settings.ENVIRONMENT
    }


@app.get("/health")
def health_check():
    """
    Basic health endpoint
    """
    return {
        "status": "healthy"
    }


@app.post("/agent/run")
def run_agent(request: UserRequest):
    """
    Main agent execution endpoint

    POST /agent/run

    {
        "message": "scan current directory"
    }
    """

    if not request.message.strip():
        return {
            "status": "error",
            "message": "Empty request"
        }

    result = agent.process(
        user_input=request.message
    )

    return result
