"""
LangGraph Workflow - AUTONOMOUS AI Agent System
"""

import logging
from typing import Dict, Any
from langgraph.graph import StateGraph, END

from core.types import AgentState, TaskType, create_initial_state
from agents import (
    manager_agent,
    autonomous_law_search_agent,
    autonomous_pdf_analysis_agent,
    autonomous_opinion_search_agent
)

logger = logging.getLogger(__name__)


def create_workflow() -> StateGraph:
    """Create LangGraph workflow for AUTONOMOUS AI system."""
    workflow = StateGraph(AgentState)

    # Add nodes
    workflow.add_node("manager", manager_agent.execute)
    workflow.add_node("autonomous_law_search", autonomous_law_search_agent.execute)
    workflow.add_node("autonomous_pdf_analysis", autonomous_pdf_analysis_agent.execute)
    workflow.add_node("autonomous_opinion_search", autonomous_opinion_search_agent.execute)

    # Routing from manager based on current task
    def route_from_manager(state: AgentState) -> str:
        current_task = state.get('current_task')
        is_complete = state.get('is_complete', False)

        logger.info(
            f"→ Routing: current_task={current_task.task_type.value if current_task else 'None'}, "
            f"is_complete={is_complete}"
        )

        if not current_task:
            logger.info("→ No current task, ending workflow")
            return END

        if is_complete:
            logger.info("→ Workflow marked as complete, ending")
            return END

        task_type = current_task.task_type
        next_agent = {
            TaskType.AUTONOMOUS_LAW_SEARCH: "autonomous_law_search",
            TaskType.AUTONOMOUS_PDF_ANALYSIS: "autonomous_pdf_analysis",
            TaskType.AUTONOMOUS_OPINION_SEARCH: "autonomous_opinion_search",
        }.get(task_type, END)

        logger.info(f"→ Routing to: {next_agent}")
        return next_agent

    # Check if workflow should continue
    def should_continue(state: AgentState) -> str:
        if state.get('is_complete') or len(state.get('errors', [])) > 5:
            return END
        return "manager"

    # Set entry point
    workflow.set_entry_point("manager")

    # Add conditional edges from manager
    workflow.add_conditional_edges(
        "manager",
        route_from_manager,
        {
            "autonomous_law_search": "autonomous_law_search",
            "autonomous_pdf_analysis": "autonomous_pdf_analysis",
            "autonomous_opinion_search": "autonomous_opinion_search",
            END: END
        }
    )

    # All agents return to manager after completion
    all_agents = [
        "autonomous_law_search",
        "autonomous_pdf_analysis",
        "autonomous_opinion_search"
    ]

    for agent in all_agents:
        workflow.add_conditional_edges(agent, should_continue)

    return workflow


async def run_autonomous_workflow(
    project_name: str,
    max_opinions: int = 20,
    quality_threshold: float = 0.6
) -> Dict[str, Any]:
    """
    Run AUTONOMOUS AI workflow.
    
    Args:
        project_name: Tên dự luật/chủ đề (BẮT BUỘC)
        max_opinions: Số opinions tối đa (mặc định: 20)
        quality_threshold: Ngưỡng chất lượng (mặc định: 0.6)
        
    Returns:
        Final state with results
    """
    try:
        logger.info("=" * 80)
        logger.info("🤖 AUTONOMOUS AI WORKFLOW - LangGraph")
        logger.info("=" * 80)
        logger.info(f"Topic/Project: {project_name}")
        logger.info(f"Max Opinions: {max_opinions}")
        logger.info(f"Quality Threshold: {quality_threshold}")
        logger.info("=" * 80)

        # Create initial state
        initial_state = create_initial_state(
            project_name=project_name,
            max_opinions=max_opinions,
            quality_threshold=quality_threshold
        )
        
        # Compile workflow
        workflow = create_workflow()
        app = workflow.compile(
            checkpointer=None,
            interrupt_before=None,
            interrupt_after=None,
            debug=False
        )
        
        # Configure with higher recursion limit
        config = {"recursion_limit": 50}

        logger.info("→ Executing workflow...")
        final_state = await app.ainvoke(initial_state, config=config)

        # Generate report
        report = manager_agent.generate_report(final_state)
        logger.info("=" * 80)
        logger.info("📊 Workflow Report")
        logger.info("=" * 80)
        for key, value in report.items():
            logger.info(f"{key}: {value}")
        logger.info("=" * 80)

        return final_state

    except Exception as e:
        logger.error(f"Workflow execution failed: {str(e)}", exc_info=True)
        raise


# Export
__all__ = ["create_workflow", "run_autonomous_workflow"]
