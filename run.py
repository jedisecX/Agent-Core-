# run.py

import uvicorn

from app.config import settings


def main():
    """
    Application launcher

    Starts FastAPI + agent runtime
    """

    print("\n===================================")
    print(f"Starting {settings.APP_NAME}")
    print("===================================")
    print(f"Environment : {settings.ENVIRONMENT}")
    print(f"Model       : {settings.MODEL_NAME}")
    print(f"Ollama URL  : {settings.OLLAMA_URL}")
    print(f"Host        : {settings.API_HOST}")
    print(f"Port        : {settings.API_PORT}")
    print("===================================\n")

    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG
    )


if __name__ == "__main__":
    main()
