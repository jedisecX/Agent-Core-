# app/core/planner.py

import json


class Planner:
    """
    Responsible for converting user intent into
    structured executable plans.

    Input:
        user request + memory context

    Output:
        normalized execution plan
    """

    def __init__(self, runtime):
        self.runtime = runtime

        self.fallback_plan = {
            "action": "direct_response",
            "tool": "none",
            "command": "",
            "reasoning": "Fallback response due to planner parse failure"
        }

    def create_plan(
        self,
        user_input: str,
        memory_context: str
    ) -> dict:
        """
        Main planner interface
        """

        raw_plan = self.runtime.generate_plan(
            user_input=user_input,
            memory_context=memory_context
        )

        parsed = self._safe_parse(raw_plan)

        validated = self._normalize_plan(parsed)

        return validated

    def _safe_parse(self, raw_plan: str) -> dict:
        """
        Prevent malformed model output
        from breaking execution flow
        """

        try:
            parsed = json.loads(raw_plan)

            if not isinstance(parsed, dict):
                return self.fallback_plan

            return parsed

        except Exception:
            return self.fallback_plan

    def _normalize_plan(self, plan: dict) -> dict:
        """
        Enforce valid structure and defaults
        """

        allowed_actions = [
            "tool",
            "direct_response"
        ]

        allowed_tools = [
            "shell",
            "file",
            "web",
            "none"
        ]

        action = plan.get("action", "direct_response")
        tool = plan.get("tool", "none")
        command = plan.get("command", "")
        reasoning = plan.get(
            "reasoning",
            "No reasoning provided"
        )

        if action not in allowed_actions:
            action = "direct_response"

        if tool not in allowed_tools:
            tool = "none"

        # Prevent invalid mixed states
        if action == "direct_response":
            tool = "none"
            command = ""

        if action == "tool" and tool == "none":
            action = "direct_response"
            command = ""

        return {
            "action": action,
            "tool": tool,
            "command": command,
            "reasoning": reasoning
        }
