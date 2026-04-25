# app/core/reflection.py

from datetime import datetime


class ReflectionEngine:
    """
    Post-execution review layer

    Responsibilities:
    - inspect execution quality
    - identify failures
    - improve future decisions
    - generate lightweight audit notes

    This is not hidden reasoning.
    It is operational review.
    """

    def __init__(self):
        self.failure_keywords = [
            "error",
            "failed",
            "denied",
            "timeout",
            "blocked",
            "exception",
            "not found",
            "does not exist"
        ]

    def review(
        self,
        user_input: str,
        plan: dict,
        tool_result,
        final_response: str
    ) -> str:
        """
        Review completed execution

        Returns:
            short reflection note for memory/logging
        """

        notes = []

        notes.append(
            f"Review timestamp: {datetime.utcnow().isoformat()}"
        )

        action = plan.get("action", "unknown")
        tool = plan.get("tool", "none")

        notes.append(
            f"Execution path: action={action}, tool={tool}"
        )

        if tool_result:
            tool_analysis = self._analyze_tool_result(
                str(tool_result)
            )
            notes.append(tool_analysis)

        response_quality = self._analyze_response(
            final_response
        )
        notes.append(response_quality)

        if not final_response.strip():
            notes.append(
                "Issue detected: empty final response"
            )

        return " | ".join(notes)

    def _analyze_tool_result(
        self,
        tool_result: str
    ) -> str:
        """
        Detect obvious execution issues
        """

        lowered = tool_result.lower()

        for keyword in self.failure_keywords:
            if keyword in lowered:
                return (
                    f"Tool review: potential failure detected "
                    f"({keyword})"
                )

        return "Tool review: execution appears successful"

    def _analyze_response(
        self,
        final_response: str
    ) -> str:
        """
        Detect weak response quality
        """

        if len(final_response.strip()) < 10:
            return (
                "Response review: unusually short response"
            )

        if "unknown execution path" in final_response.lower():
            return (
                "Response review: execution routing issue detected"
            )

        return "Response review: acceptable"
