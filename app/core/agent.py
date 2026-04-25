# app/core/agent.py

from app.core.planner import Planner
from app.core.memory import MemoryManager
from app.core.tools import ToolDispatcher
from app.core.policies import PolicyEngine
from app.core.reflection import ReflectionEngine
from app.core.executor import OllamaRuntime


class AgentCore:
    """
    Core autonomous agent loop

    Flow:
    Observe → Plan → Validate → Execute → Reflect → Respond → Store Memory
    """

    def __init__(self):
        self.runtime = OllamaRuntime()
        self.memory = MemoryManager()
        self.planner = Planner(self.runtime)
        self.tools = ToolDispatcher()
        self.policies = PolicyEngine()
        self.reflection = ReflectionEngine()

    def process(self, user_input: str) -> dict:
        """
        Main execution loop
        """

        # Step 1 — Load contextual memory
        memory_context = self.memory.retrieve_context(user_input)

        # Step 2 — Generate execution plan
        plan = self.planner.create_plan(
            user_input=user_input,
            memory_context=memory_context
        )

        # Example plan:
        # {
        #   "action": "tool",
        #   "tool": "shell",
        #   "command": "ls -la",
        #   "reasoning": "Need to inspect directory"
        # }

        # Step 3 — Validate against policy engine
        approved, reason = self.policies.validate(plan)

        if not approved:
            response = {
                "status": "blocked",
                "reason": reason,
                "response": f"Action blocked by policy engine: {reason}"
            }

            self.memory.store_interaction(
                user_input=user_input,
                assistant_response=response["response"]
            )

            return response

        # Step 4 — Execute action
        if plan["action"] == "tool":
            tool_result = self.tools.execute(
                tool_name=plan["tool"],
                payload=plan
            )

            final_response = self.runtime.generate_response(
                user_input=user_input,
                tool_output=tool_result,
                memory_context=memory_context
            )

        elif plan["action"] == "direct_response":
            final_response = self.runtime.generate_direct_response(
                user_input=user_input,
                memory_context=memory_context
            )

            tool_result = None

        else:
            final_response = "Unknown execution path."
            tool_result = None

        # Step 5 — Reflection layer
        reflection_notes = self.reflection.review(
            user_input=user_input,
            plan=plan,
            tool_result=tool_result,
            final_response=final_response
        )

        # Step 6 — Store memory
        self.memory.store_interaction(
            user_input=user_input,
            assistant_response=final_response,
            plan=plan,
            reflection=reflection_notes
        )

        # Step 7 — Return structured output
        return {
            "status": "success",
            "plan": plan,
            "tool_result": tool_result,
            "reflection": reflection_notes,
            "response": final_response
        }


if __name__ == "__main__":
    agent = AgentCore()

    print("\n=== Autonomous Agent Online ===\n")

    while True:
        user = input("You: ")

        if user.lower() in ["exit", "quit"]:
            print("Agent shutting down.")
            break

        result = agent.process(user)

        print("\nAgent:")
        print(result["response"])
        print()
