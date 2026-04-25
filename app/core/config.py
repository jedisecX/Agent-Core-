# app/config.py

import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """
    Central configuration layer

    Responsibilities:
    - environment loading
    - runtime settings
    - path management
    - deployment consistency
    """

    def __init__(self):
        # Core runtime
        self.APP_NAME = os.getenv(
            "APP_NAME",
            "AgentCore"
        )

        self.ENVIRONMENT = os.getenv(
            "ENVIRONMENT",
            "development"
        )

        self.DEBUG = self._to_bool(
            os.getenv("DEBUG", "true")
        )

        # Ollama runtime
        self.OLLAMA_URL = os.getenv(
            "OLLAMA_URL",
            "http://localhost:11434"
        )

        self.MODEL_NAME = os.getenv(
            "MODEL_NAME",
            "your-model-name"
        )

        # Memory storage
        self.MEMORY_FILE = os.getenv(
            "MEMORY_FILE",
            "app/database/memory.json"
        )

        # Logging
        self.LOG_PATH = os.getenv(
            "LOG_PATH",
            "app/database/logs/"
        )

        # Security
        self.MAX_TOOL_OUTPUT = int(
            os.getenv(
                "MAX_TOOL_OUTPUT",
                "5000"
            )
        )

        self.REQUIRE_APPROVAL = self._to_bool(
            os.getenv(
                "REQUIRE_APPROVAL",
                "false"
            )
        )

        # API
        self.API_HOST = os.getenv(
            "API_HOST",
            "0.0.0.0"
        )

        self.API_PORT = int(
            os.getenv(
                "API_PORT",
                "8000"
            )
        )

    def _to_bool(
        self,
        value: str
    ) -> bool:
        """
        Safe bool parsing
        """

        return str(value).lower() in [
            "true",
            "1",
            "yes",
            "on"
        ]


settings = Settings()
