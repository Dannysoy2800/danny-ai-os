"""Manager Agent implementation

Core agent responsible for managing workflow execution and coordination.
"""

from typing import TypedDict, Any, Dict
from langgraph.graph import StateGraph, END
from src.core.logger import setup_logger
from src.core.exceptions import AgentError

logger = setup_logger(__name__)


class AgentState(TypedDict):
    """State for agent operations"""

    message: str
    status: str
    result: Dict[str, Any]
    error: str | None


class ManagerAgent:
    """Manager Agent for orchestrating AI workflows"""

    def __init__(self):
        """Initialize the Manager Agent"""
        self.graph = self._build_graph()
        logger.info("Manager Agent initialized")

    def _build_graph(self) -> StateGraph:
        """Build the LangGraph state graph

        Returns:
            Compiled LangGraph StateGraph
        """
        builder = StateGraph(AgentState)

        # Add nodes
        builder.add_node("process", self._process_message)
        builder.add_node("validate", self._validate_result)
        builder.add_node("complete", self._complete_task)

        # Add edges
        builder.set_entry_point("process")
        builder.add_edge("process", "validate")
        builder.add_edge("validate", "complete")
        builder.add_edge("complete", END)

        return builder.compile()

    def _process_message(self, state: AgentState) -> AgentState:
        """Process incoming message

        Args:
            state: Current agent state

        Returns:
            Updated agent state
        """
        try:
            logger.info(f"Processing message: {state['message']}")
            state["status"] = "processing"
            state["result"] = {"processed": True, "message": state["message"]}
            state["error"] = None
            return state
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            raise AgentError(f"Failed to process message: {str(e)}")

    def _validate_result(self, state: AgentState) -> AgentState:
        """Validate processing result

        Args:
            state: Current agent state

        Returns:
            Updated agent state
        """
        try:
            logger.info("Validating result")
            if state["result"] and "processed" in state["result"]:
                state["status"] = "validated"
            else:
                state["error"] = "Validation failed: Invalid result format"
            return state
        except Exception as e:
            logger.error(f"Validation error: {str(e)}")
            state["error"] = str(e)
            return state

    def _complete_task(self, state: AgentState) -> AgentState:
        """Complete the task

        Args:
            state: Current agent state

        Returns:
            Updated agent state
        """
        logger.info("Task completed")
        state["status"] = "completed"
        return state

    def execute(self, message: str) -> Dict[str, Any]:
        """Execute agent with given message

        Args:
            message: Input message to process

        Returns:
            Execution result
        """
        initial_state: AgentState = {
            "message": message,
            "status": "initialized",
            "result": {},
            "error": None,
        }

        result = self.graph.invoke(initial_state)
        logger.info(f"Execution result: {result}")
        return result
