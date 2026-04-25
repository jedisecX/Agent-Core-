# app/core/policies.py

import re


class PolicyEngine:
    """
    Governance + execution safety layer

    Responsibilities:
    - validate execution plans
    - prevent dangerous actions
    - enforce deny-by-default rules
    - provide human approval hooks later

    This is the firewall between
    model intent and system action.
    """

    def __init__(self):
        self.blocked_shell_patterns = [
            r"rm\s+-rf",
            r"shutdown",
            r"reboot",
            r"mkfs",
            r"dd\s+if=",
            r"chmod\s+777",
            r"chown\s+-R",
            r"sudo",
            r"passwd",
            r"userdel",
            r"usermod",
            r"iptables",
            r"ufw",
            r"systemctl\s+stop",
            r"kill\s+-9",
            r"curl\s+.*\|\s*sh",
            r"wget\s+.*\|\s*sh"
        ]

        self.allowed_tools = [
            "shell",
            "file",
            "web",
            "none"
        ]

    def validate(
        self,
        plan: dict
    ) -> tuple:
        """
        Validate plan before execution

        Returns:
            (approved: bool, reason: str)
        """

        action = plan.get("action", "")
        tool = plan.get("tool", "")
        command = plan.get("command", "")

        if action not in ["tool", "direct_response"]:
            return False, "Invalid action type"

        if tool not in self.allowed_tools:
            return False, f"Tool not allowed: {tool}"

        if action == "direct_response":
            return True, "Approved"

        if action == "tool":
            return self._validate_tool_action(
                tool,
                command
            )

        return False, "Unknown validation failure"

    def _validate_tool_action(
        self,
        tool: str,
        command: str
    ) -> tuple:
        """
        Tool-specific validation
        """

        if tool == "shell":
            return self._validate_shell(command)

        if tool == "file":
            return self._validate_file(command)

        if tool == "web":
            return self._validate_web(command)

        return False, "Unsupported tool"

    def _validate_shell(
        self,
        command: str
    ) -> tuple:
        """
        Shell execution restrictions
        """

        if not command.strip():
            return False, "Empty shell command"

        lowered = command.lower()

        for pattern in self.blocked_shell_patterns:
            if re.search(pattern, lowered):
                return False, (
                    f"Blocked dangerous shell pattern: {pattern}"
                )

        return True, "Approved"

    def _validate_file(
        self,
        file_path: str
    ) -> tuple:
        """
        Prevent sensitive file access
        """

        blocked_paths = [
            "/etc/",
            "/root/",
            "/home/",
            ".env",
            "id_rsa",
            "authorized_keys"
        ]

        lowered = file_path.lower()

        for item in blocked_paths:
            if item.lower() in lowered:
                return False, (
                    f"Blocked sensitive file access: {item}"
                )

        return True, "Approved"

    def _validate_web(
        self,
        url: str
    ) -> tuple:
        """
        Prevent malformed requests
        """

        if not url.startswith(
            ("http://", "https://")
        ):
            return False, "Invalid URL"

        blocked_domains = [
            "localhost",
            "127.0.0.1",
            "0.0.0.0"
        ]

        lowered = url.lower()

        for domain in blocked_domains:
            if domain in lowered:
                return False, (
                    f"Blocked internal network access: {domain}"
                )

        return True, "Approved"
