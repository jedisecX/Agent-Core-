# app/core/executor.py

import requests
from app.config import settings


class OllamaRuntime:
    """
    Handles all communication with Ollama runtime

    Responsibilities:
    - planning prompts
    - direct response generation
    - tool result synthesis
    - system prompt enforcement
    """

    def __init__(self):
        self.base_url = settings.OLLAMA_URL
        self.model = settings.MODEL_NAME
        self.timeout = 120

        self.system_prompt = """
You are an autonomous AI agent operating inside a controlled environment.

Rules:
- Be accurate
- Be concise
- Never invent tool results
- Never claim actions were completed if they were not
- Use tools only when necessary
- Respect policy restrictions
- Prioritize safe and correct execution
"""

    def _call_ollama(self, prompt: str) -> str:
        """
        Low-level Ollama API request
        """

        payload = {
            "model": self.model,
            "prompt": f"{self.system_prompt}\n\n{prompt}",
            "stream": False
        }

        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=self.timeout
            )

            response.raise_for_status()

            data = response.json()
            return data.get("response", "").strip()

        except requests.exceptions.RequestException as e:
            return f"Ollama connection error: {str(e)}"

        except Exception as e:
            return f"Runtime execution error: {str(e)}"

    def generate_plan(
        self,
        user_input: str,
        memory_context: str
    ) -> str:
        """
        Used by planner.py to determine next action
        """

        prompt = f"""
Conversation Context:
{memory_context}

User Request:
{user_input}

Return ONLY valid JSON in this exact structure:

{{
    "action": "tool OR direct_response",
    "tool": "shell/file/web/none",
    "command": "command if needed",
    "reasoning": "brief explanation"
}}

No markdown.
No explanation outside JSON.
"""

        return self._call_ollama(prompt)

    def generate_response(
        self,
        user_input: str,
        tool_output: str,
        memory_context: str
    ) -> str:
        """
        Final response after tool execution
        """

        prompt = f"""
Conversation Context:
{memory_context}

Original User Request:
{user_input}

Tool Output:
{tool_output}

Generate the best final response for the user.

Rules:
- Be truthful
- Use tool results only
- No hallucinations
- No fake success messages
"""

        return self._call_ollama(prompt)

    def generate_direct_response(
        self,
        user_input: str,
        memory_context: str
    ) -> str:
        """
        Direct answer without tool execution
        """

        prompt = f"""
Conversation Context:
{memory_context}

User Request:
{user_input}

Respond directly and accurately.
"""

        return self._call_ollama(prompt)
