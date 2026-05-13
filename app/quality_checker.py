from strands.agent.agent_result import AgentResult
from strands.multiagent import MultiAgentBase, MultiAgentResult
from strands.multiagent.base import NodeResult, Status
from strands.types.content import ContentBlock, Message


class QualityChecker(MultiAgentBase):
    """Custom node that evaluates content quality."""

    def __init__(self, approval_after: int = 2):
        super().__init__()
        self.approval_after = approval_after
        self.iteration = 0
        self.name = "checker"

    async def invoke_async(self, task, invocation_state, **kwargs):
        self.iteration += 1
        approved = self.iteration >= self.approval_after

        msg = (
            f"✅ Iteration {self.iteration}: APPROVED"
            if approved
            else f"⚠️ Iteration {self.iteration}: NEEDS REVISION"
        )

        agent_result = AgentResult(
            stop_reason="end_turn",
            message=Message(role="assistant", content=[ContentBlock(text=msg)]),
            metrics=None,
            state={"approved": approved, "iteration": self.iteration},
        )

        return MultiAgentResult(
            status=Status.COMPLETED,
            results={
                self.name: NodeResult(
                    result=agent_result, execution_time=10, status=Status.COMPLETED
                )
            },
            execution_count=1,
            execution_time=10,
        )
