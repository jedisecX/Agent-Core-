# app/main.py

from fastapi import FastAPI
from pydantic import BaseModel

from app.config import settings
from app.core.agent import AgentCore

# API routers
from app.api.routes import router as api_router
from app.dashboard.dashboard import router as dashboard_router

# Background scheduler
from app.tasks.scheduler import scheduler


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


@app.on_event("startup")
def startup_event():
    """
    Boot scheduler + runtime services
    """

    scheduler.start()

    print("Agent runtime initialized.")


@app.on_event("shutdown")
def shutdown_event():
    """
    Clean shutdown
    """

    scheduler.stop()

    print("Agent runtime stopped.")


@app.get("/")
def root():
    """
    Root identity endpoint
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
    Service health endpoint
    """

    return {
        "status": "healthy"
    }


@app.post("/agent/run")
def run_agent(request: UserRequest):
    """
    Direct execution endpoint
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


# Attach modular routers
app.include_router(api_router)
app.include_router(dashboard_router)
