# app/core/tools.py

import os
import subprocess
import requests


class ToolDispatcher:
    """
    Controlled execution layer for external tools

    Supported tools:
    - shell
    - file
    - web

    Security principle:
    deny by default
    """

    def __init__(self):
        self.allowed_shell_commands = [
            "ls",
            "pwd",
            "whoami",
            "cat",
            "echo",
            "find"
        ]

        self.allowed_read_paths = [
            "./",
            "./data/",
            "./logs/",
            "./workspace/"
        ]

    def execute(
        self,
        tool_name: str,
        payload: dict
    ) -> str:
        """
        Central dispatch
        """

        if tool_name == "shell":
            return self._run_shell(
                payload.get("command", "")
            )

        elif tool_name == "file":
            return self._read_file(
                payload.get("command", "")
            )

        elif tool_name == "web":
            return self._basic_web_fetch(
                payload.get("command", "")
            )

        return "Unknown tool requested."

    def _run_shell(
        self,
        command: str
    ) -> str:
        """
        Strictly controlled shell access
        """

        if not command.strip():
            return "Empty shell command."

        base_command = command.split()[0]

        if base_command not in self.allowed_shell_commands:
            return f"Blocked shell command: {base_command}"

        try:
            result = subprocess.check_output(
                command,
                shell=True,
                stderr=subprocess.STDOUT,
                text=True,
                timeout=20
            )

            return result.strip()

        except subprocess.TimeoutExpired:
            return "Shell command timed out."

        except Exception as e:
            return f"Shell execution error: {str(e)}"

    def _read_file(
        self,
        file_path: str
    ) -> str:
        """
        Safe file read only
        """

        if not file_path.strip():
            return "No file path provided."

        normalized = os.path.abspath(file_path)

        allowed = any(
            normalized.startswith(
                os.path.abspath(path)
            )
            for path in self.allowed_read_paths
        )

        if not allowed:
            return "Access denied: path outside allowed scope."

        if not os.path.exists(normalized):
            return "File does not exist."

        try:
            with open(
                normalized,
                "r",
                encoding="utf-8"
            ) as f:
                content = f.read(5000)

            return content

        except Exception as e:
            return f"File read error: {str(e)}"

    def _basic_web_fetch(
        self,
        url: str
    ) -> str:
        """
        Minimal safe HTTP GET fetch

        Future:
        replace with proper search tool integration
        """

        if not url.startswith(("http://", "https://")):
            return "Invalid URL format."

        try:
            response = requests.get(
                url,
                timeout=15
            )

            return response.text[:5000]

        except Exception as e:
            return f"Web fetch error: {str(e)}"
