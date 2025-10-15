"""
Manager Agent - Orchestrates AUTONOMOUS AI workflow.
"""

import logging
from typing import Dict, Any
from datetime import datetime

from agents.base import BaseAgent
from core.types import AgentState, AgentRole, TaskType
from prompts import load_prompt

logger = logging.getLogger(__name__)


class ManagerAgent(BaseAgent):
    """
    Manager Agent - Orchestrator for AUTONOMOUS AI workflow.

    AUTONOMOUS WORKFLOW (3 steps):
    1. AUTONOMOUS_LAW_SEARCH → AI tìm và download PDF luật
    2. AUTONOMOUS_PDF_ANALYSIS → AI extract PDF + tạo keywords
    3. AUTONOMOUS_OPINION_SEARCH → AI search + crawl + analyze opinions
    """

    def __init__(self):
        super().__init__(
            role=AgentRole.MANAGER,
            name="Manager Agent",
            description="Orchestrates AUTONOMOUS AI workflow"
        )
        self.system_prompt = load_prompt("manager_system.md")

    async def execute(self, state: AgentState) -> AgentState:
        """Execute manager logic."""
        try:
            logger.info("=" * 60)
            logger.info("Manager Agent executing...")
            logger.info("=" * 60)

            if not state.get('current_task'):
                return await self._start_workflow(state)
            else:
                return await self._monitor_and_decide(state)

        except Exception as e:
            logger.error(f"Manager execution error: {str(e)}")
            return self.log_error(state, f"Manager execution failed: {str(e)}")

    async def _start_workflow(self, state: AgentState) -> AgentState:
        """Start AUTONOMOUS workflow."""
        project_name = state['project_name']
        
        logger.info("Starting AUTONOMOUS AI workflow...")
        logger.info(f"Project/Topic: {project_name}")
        logger.info(f"Max Opinions: {state['max_opinions']}")
        logger.info(f"Quality Threshold: {state['quality_threshold']}")
        
        # Start with AUTONOMOUS_LAW_SEARCH
        task = self.create_task(
            task_type=TaskType.AUTONOMOUS_LAW_SEARCH.value,
            input_data={'topic': project_name}
        )

        state = self.update_state(state, {'current_task': task})
        from core.types import update_state_task
        state = update_state_task(state, task)

        logger.info(f"✅ Created first task: {task.task_type.value}")
        return state

    async def _monitor_and_decide(self, state: AgentState) -> AgentState:
        """Monitor progress and decide next step."""
        current_task = state.get('current_task')
        task_history = state.get('task_history', [])

        if not current_task:
            logger.info("No current task, workflow may be complete")
            return state

        logger.info(f"Current task: {current_task.task_type.value} - {current_task.status.value}")

        # Get completed task types
        completed_types = [
            task.task_type
            for task in task_history
            if task.status.value == 'completed'
        ]

        def task_already_created(task_type):
            """Check if a task type already exists in history."""
            return any(t.task_type == task_type for t in task_history) or \
                   (current_task and current_task.task_type == task_type)

        next_task = None

        # ========================================================================
        # AUTONOMOUS WORKFLOW LOGIC (3 Steps)
        # ========================================================================
        
        # Step 1: AUTONOMOUS_LAW_SEARCH → AUTONOMOUS_PDF_ANALYSIS
        if TaskType.AUTONOMOUS_LAW_SEARCH in completed_types and \
           TaskType.AUTONOMOUS_PDF_ANALYSIS not in completed_types:
            if not task_already_created(TaskType.AUTONOMOUS_PDF_ANALYSIS):
                next_task = self.create_task(
                    task_type=TaskType.AUTONOMOUS_PDF_ANALYSIS.value,
                    input_data={}
                )
                logger.info("📄 Next: AI extract PDF and create keywords")
        
        # Step 2: AUTONOMOUS_PDF_ANALYSIS → AUTONOMOUS_OPINION_SEARCH
        elif TaskType.AUTONOMOUS_PDF_ANALYSIS in completed_types and \
             TaskType.AUTONOMOUS_OPINION_SEARCH not in completed_types:
            if not task_already_created(TaskType.AUTONOMOUS_OPINION_SEARCH):
                max_articles = state.get('max_opinions', 20)
                quality_threshold = state.get('quality_threshold', 0.6)
                
                next_task = self.create_task(
                    task_type=TaskType.AUTONOMOUS_OPINION_SEARCH.value,
                    input_data={
                        'max_articles': max_articles,
                        'quality_threshold': quality_threshold
                    }
                )
                logger.info(f"🔍 Next: AI autonomous search (max={max_articles}, threshold={quality_threshold})")
        
        # Step 3: AUTONOMOUS_OPINION_SEARCH → Complete
        elif TaskType.AUTONOMOUS_OPINION_SEARCH in completed_types:
            logger.info("✅ AUTONOMOUS Workflow completed successfully!")
            state['is_complete'] = True
            return state

        # ========================================================================
        # Update state with next task or complete
        # ========================================================================

        logger.info(
            f"🔍 End of Manager logic: next_task={next_task is not None}, "
            f"is_complete={state.get('is_complete', False)}"
        )

        if next_task:
            logger.info(f"✅ Setting next task: {next_task.task_type.value} (status: {next_task.status.value})")
            state = self.update_state(state, {'current_task': next_task})
            from core.types import update_state_task
            state = update_state_task(state, next_task)
        else:
            # Safety check: if task is completed but no next task created
            if current_task and current_task.status.value == 'completed':
                logger.warning("⚠️ Current task completed but no next task created")
                logger.warning(f"⚠️ Task: {current_task.task_type.value}")
                logger.warning("⚠️ Marking workflow as complete to avoid infinite loop")
                state['is_complete'] = True
            else:
                logger.info("ℹ️ No new task to create, workflow continues with current task")

        logger.info(
            f"🔄 Manager returning state with current_task="
            f"{state.get('current_task').task_type.value if state.get('current_task') else 'None'}"
        )
        return state

    def generate_report(self, state: AgentState) -> Dict[str, Any]:
        """Generate workflow summary report."""
        task_history = state.get('task_history', [])
        completed_tasks = [t for t in task_history if t.status.value == 'completed']
        failed_tasks = [t for t in task_history if t.status.value == 'failed']

        report = {
            'project_name': state.get('project_name'),
            'started_at': state.get('started_at'),
            'completed_at': datetime.now() if state.get('is_complete') else None,
            'total_tasks': len(task_history),
            'completed_tasks': len(completed_tasks),
            'failed_tasks': len(failed_tasks),
            'errors_count': len(state.get('errors', [])),
            'warnings_count': len(state.get('warnings', [])),
            # Autonomous workflow metrics
            'law_documents_found': len(state.get('law_documents', [])),
            'pdf_downloaded': state.get('pdf_local_path') is not None,
            'keywords_extracted': len(state.get('search_queries', [])),
            'opinions_analyzed': len(state.get('analyzed_opinions', [])),
            'csv_exported': state.get('csv_output_path') is not None
        }
        return report


# Singleton instance
manager_agent = ManagerAgent()
