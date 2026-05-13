import os
from strands import Agent
from strands.models.ollama import OllamaModel
from strands.multiagent import GraphBuilder
from app.quality_checker import QualityChecker
from app.tools import get_all_tools


class ContentLoopWorkflow:
    """Encapsulates the graph with a write-review-improve feedback loop."""

    def __init__(self, model_id: str | None = None, approval_after: int = 2):
        ollama_host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        ollama_model = model_id or os.getenv("OLLAMA_MODEL_ID", "llama3.1:latest")
        self.model = OllamaModel(host=ollama_host, model_id=ollama_model)
        self.approval_after = approval_after
        self.tools = get_all_tools()
        self.graph = self._build_graph()

    def _build_graph(self):
        writer = Agent(
            model=self.model,
            name="writer",
            system_prompt="You are a content writer. Write or improve content based on the task. Use available tools to fetch information if needed. Keep responses concise.",
            tools=self.tools,
        )

        finalizer = Agent(
            model=self.model,
            name="finalizer",
            system_prompt="Polish the approved content into a professional format with a title.",
        )

        checker = QualityChecker(approval_after=self.approval_after)

        builder = GraphBuilder()
        builder.add_node(writer, "writer")
        builder.add_node(checker, "checker")
        builder.add_node(finalizer, "finalizer")

        builder.add_edge("writer", "checker")

        # Define edge conditions
        builder.add_edge("checker", "writer", condition=self._needs_revision)
        builder.add_edge("checker", "finalizer", condition=self._is_approved)

        builder.set_entry_point("writer")
        builder.set_max_node_executions(10)
        builder.set_execution_timeout(60)
        builder.reset_on_revisit(True)

        return builder.build()

    @staticmethod
    def _get_checker_state(state):
        checker_result = state.results.get("checker")
        if not checker_result:
            return None
        multi_result = checker_result.result
        if hasattr(multi_result, "results") and "checker" in multi_result.results:
            agent_result = multi_result.results["checker"].result
            if hasattr(agent_result, "state"):
                return agent_result.state
        return None

    def _needs_revision(self, state):
        checker_state = self._get_checker_state(state)
        if checker_state is not None:
            return not checker_state.get("approved", False)
        return True

    def _is_approved(self, state):
        checker_state = self._get_checker_state(state)
        if checker_state is not None:
            return checker_state.get("approved", False)
        return False

    def execute(self, task: str):
        """Runs the content creation workflow."""
        return self.graph(task)
