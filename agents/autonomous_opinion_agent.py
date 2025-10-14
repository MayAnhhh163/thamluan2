"""
Autonomous Opinion Agent - Agent tự động dùng Ollama + Chrome để search và crawl
"""

import logging
from typing import Dict, Any

from agents.base import BaseAgent
from core.types import AgentState, AgentRole, TaskType
from tools.ollama_autonomous_search import ollama_autonomous_search_agent

logger = logging.getLogger(__name__)


class AutonomousOpinionAgent(BaseAgent):
    """
    Agent tự động tìm kiếm opinions sử dụng Ollama + Chrome

    Flow:
    1. Nhận topic từ state
    2. Dùng Ollama để sinh search queries
    3. Tự động search trên Google Chrome
    4. Dùng Ollama để đánh giá từng kết quả
    5. Click vào link relevant
    6. Crawl nội dung
    7. Dùng Ollama để đánh giá chất lượng
    8. Lưu opinions chất lượng cao
    """

    def __init__(self):
        super().__init__(
            role=AgentRole.SEARCH_AGENT,
            name="Autonomous Opinion Agent",
            description="AI tự động search Chrome và crawl opinions"
        )

    async def execute(self, state: AgentState) -> AgentState:
        try:
            logger.info(f"🤖 {self.name} executing...")

            current_task = state.get('current_task')
            if not current_task or current_task.task_type != TaskType.AUTONOMOUS_OPINION_SEARCH:
                return state

            project_name = state['project_name']

            # Get search config from task input or use defaults
            max_articles = current_task.input_data.get('max_articles', 20)
            quality_threshold = current_task.input_data.get('quality_threshold', 0.6)

            logger.info(f"🔍 Starting autonomous search for: {project_name}")
            logger.info(f"Target: {max_articles} articles (quality >= {quality_threshold})")

            # Run autonomous search
            result = ollama_autonomous_search_agent.autonomous_search_and_crawl(
                topic=project_name,
                max_articles=max_articles,
                max_search_pages=3,
                quality_threshold=quality_threshold
            )

            if not result.success:
                task = self.complete_task(current_task, {}, error=result.error)
                return self.log_error(state, result.error)

            opinions = result.data['opinions']
            logger.info(f"✅ Autonomous search complete: {len(opinions)} opinions collected")

            # Convert to standard format
            opinions_raw = []
            for op in opinions:
                opinions_raw.append({
                    'url': op['url'],
                    'title': op['title'],
                    'content': op['content'],
                    'source': op['source'],
                    'quality_score': op['quality_score'],
                    'quality_feedback': op['quality_feedback'],
                    'key_points': op.get('key_points', []),
                    'relevance': op.get('relevance', 'medium')
                })

            task = self.complete_task(current_task, {
                'opinions_count': len(opinions),
                'average_quality': result.data['average_quality'],
                'sources': result.data['sources']
            })

            state = self.update_state(state, {
                'current_task': task,
                'opinions_raw': opinions_raw,
                'autonomous_search_stats': {
                    'visited_urls': result.data['visited_urls'],
                    'average_quality': result.data['average_quality'],
                    'sources': result.data['sources']
                }
            })

            return state

        except Exception as e:
            logger.error(f"Autonomous opinion agent error: {str(e)}")
            return self.log_error(state, f"Autonomous search failed: {str(e)}")


# Singleton instance
autonomous_opinion_agent = AutonomousOpinionAgent()
