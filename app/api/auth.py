# app/api/auth.py

import os
from fastapi import Header, HTTPException
from dotenv import load_dotenv

load_dotenv()


class APIAuth:
    """
    Lightweight API key authentication layer

    Responsibilities:
    - protect execution endpoints
    - validate operator access
    - provide upgrade path for RBAC later

    Current mode:
    simple static API key validation
    """

    def __init__(self):
        self.api_key = os.getenv(
            "AGENT_API_KEY",
            "change-this-immediately"
        )

    def validate_key(
        self,
        x_api_key: str
    ) -> bool:
        """
        Validate incoming API key
        """

        if not x_api_key:
            return False

        return x_api_key == self.api_key


auth_engine = APIAuth()


def require_api_key(
    x_api_key: str = Header(
        default=None,
        alias="X-API-Key"
    )
):
    """
    FastAPI dependency injection auth gate

    Usage:
    Depends(require_api_key)
    """

    if not auth_engine.validate_key(
        x_api_key
    ):
        raise HTTPException(
            status_code=401,
            detail="Unauthorized access"
        )

    return True
