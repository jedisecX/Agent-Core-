# app/api/routes.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.core.agent import AgentCore

router = APIRouter(
    prefix="/api",
    tags=["Agent API"]
)

agent = AgentCore()


class AgentRequest(BaseModel):
    """
    Standard agent request body
    """
    message: str


class MemoryClearRequest(BaseModel):
    """
    Optional future extension
    """
    confirm: bool = False


@router.get("/status")
def api_status():
    """
    API status endpoint
    """

    return {
        "status": "online",
        "service": "Agent API"
    }


@router.post("/run")
def run_agent(request: AgentRequest):
    """
    Execute agent request

    Example:
    {
        "message": "list files in workspace"
    }
    """

    if not request.message.strip():
        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty"
        )

    try:
        result = agent.process(
            user_input=request.message
        )

        return result

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Execution failure: {str(e)}"
        )


@router.post("/memory/clear")
def clear_memory(request: MemoryClearRequest):
    """
    Manual memory wipe
    """

    if not request.confirm:
        raise HTTPException(
            status_code=400,
            detail="Confirmation required"
        )

    try:
        agent.memory.clear_memory()

        return {
            "status": "success",
            "message": "Memory cleared"
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Memory clear failure: {str(e)}"
        )
