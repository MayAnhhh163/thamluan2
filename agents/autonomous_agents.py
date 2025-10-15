"""
Autonomous Agents - LangGraph agents for full AI-powered autonomous workflow
"""

import logging
import time
import json
import re
from typing import Dict, Any, List, Optional
from langchain.schema import HumanMessage

from agents.base import BaseAgent
from core.types import AgentState, AgentRole, TaskType, ToolResult
from core.config import config
from tools.law_list_crawler import law_list_crawler
from tools.pdf_downloader import pdf_downloader
from tools.pdf_extractor import pdf_extractor_tool
from tools.ollama_autonomous_search import ollama_autonomous_search_agent

logger = logging.getLogger(__name__)


class AutonomousLawSearchAgent(BaseAgent):
    """
    Agent tự động tìm và download PDF văn bản luật
    
    Phase 1 của autonomous workflow:
    1. AI tự động tìm PDF văn bản luật chính thức
    2. AI đánh giá và chọn document tốt nhất
    3. Download PDF
    """
    
    def __init__(self):
        super().__init__(
            role=AgentRole.WEB_CRAWLER,
            name="Autonomous Law Search Agent",
            description="AI tự động tìm và download PDF văn bản luật"
        )
    
    async def execute(self, state: AgentState) -> AgentState:
        try:
            logger.info(f"🤖 {self.name} executing...")
            
            current_task = state.get('current_task')
            if not current_task or current_task.task_type != TaskType.AUTONOMOUS_LAW_SEARCH:
                return state
            
            topic = state['project_name']
            
            logger.info("=" * 80)
            logger.info("📋 PHASE 1: AI TÌM VĂN BẢN LUẬT CHÍNH THỨC")
            logger.info("=" * 80)
            logger.info(f"🔍 Searching for law documents: '{topic}'")
            
            # Search with high threshold (0.8) để chỉ lấy relevant
            result = law_list_crawler.crawl_law_list(
                topic=topic,
                source='duthaoonline',
                max_pages=1,
                max_results=10,
                similarity_threshold=0.8  # High threshold
            )
            
            if not result.success:
                error_msg = f"Failed to search law documents: {result.error}"
                logger.error(error_msg)
                task = self.complete_task(current_task, {}, error=error_msg)
                return self.log_error(state, error_msg)
            
            documents = result.data['documents']
            logger.info(f"✅ Found {len(documents)} relevant law documents")
            
            if not documents:
                error_msg = 'No relevant law documents found'
                task = self.complete_task(current_task, {}, error=error_msg)
                return self.log_error(state, error_msg)
            
            # AI đánh giá document nào tốt nhất
            best_doc = await self._ai_select_best_document(documents, topic)
            
            pdf_path = None
            if best_doc and best_doc.pdf_url:
                logger.info(f"📥 Downloading PDF: {best_doc.title}")
                
                # Download PDF
                pdf_result = pdf_downloader.download_pdf(
                    url=best_doc.pdf_url,
                    doc_id=best_doc.doc_id,
                    filename=f"{best_doc.doc_id}.pdf"
                )
                
                if pdf_result.success:
                    pdf_path = pdf_result.data['path']
                    logger.info(f"✅ PDF downloaded: {pdf_path}")
            
            # Complete task
            task = self.complete_task(current_task, {
                'documents_count': len(documents),
                'best_document': best_doc.to_dict() if best_doc else None,
                'pdf_downloaded': pdf_path is not None
            })
            
            state = self.update_state(state, {
                'current_task': task,
                'law_documents': [doc.to_dict() for doc in documents],
                'pdf_local_path': pdf_path
            })
            
            return state
            
        except Exception as e:
            logger.error(f"Autonomous law search error: {str(e)}")
            return self.log_error(state, f"Autonomous law search failed: {str(e)}")
    
    async def _ai_select_best_document(self, documents, topic: str):
        """AI chọn document tốt nhất"""
        try:
            if len(documents) == 1:
                return documents[0]
            
            # Tạo danh sách cho AI
            doc_list = []
            for i, doc in enumerate(documents[:5], 1):  # Top 5
                doc_list.append(f"{i}. {doc.title}")
            
            prompt = f"""Bạn là chuyên gia về luật pháp Việt Nam.

Chủ đề cần tìm: "{topic}"

Danh sách văn bản tìm được:
{chr(10).join(doc_list)}

Nhiệm vụ: Chọn văn bản CHÍNH XÁC NHẤT và LIÊN QUAN NHẤT đến chủ đề.

Chỉ trả về SỐ THỨ TỰ (1, 2, 3, ...), không giải thích."""

            response = await self.llm.ainvoke([HumanMessage(content=prompt)])
            choice_text = response.content.strip()
            
            # Extract number
            match = re.search(r'\d+', choice_text)
            if match:
                choice = int(match.group()) - 1
                if 0 <= choice < len(documents):
                    logger.info(f"✅ AI selected: {documents[choice].title}")
                    return documents[choice]
            
            # Fallback: first document
            return documents[0]
            
        except Exception as e:
            logger.warning(f"AI selection failed: {str(e)}, using first document")
            return documents[0]


class AutonomousPdfAnalysisAgent(BaseAgent):
    """
    Agent tự động extract và phân tích PDF
    
    Phase 2 của autonomous workflow:
    1. AI extract nội dung PDF
    2. AI extract keywords từ PDF
    """
    
    def __init__(self):
        super().__init__(
            role=AgentRole.CONTENT_EXTRACTOR,
            name="Autonomous PDF Analysis Agent",
            description="AI extract và phân tích PDF để tạo keywords"
        )
    
    async def execute(self, state: AgentState) -> AgentState:
        try:
            logger.info(f"🤖 {self.name} executing...")
            
            current_task = state.get('current_task')
            if not current_task or current_task.task_type != TaskType.AUTONOMOUS_PDF_ANALYSIS:
                return state
            
            logger.info("=" * 80)
            logger.info("📄 PHASE 2: AI EXTRACT NỘI DUNG PDF")
            logger.info("=" * 80)
            
            pdf_path = state.get('pdf_local_path')
            topic = state['project_name']
            
            keywords = []
            pdf_content = ""
            
            if pdf_path:
                logger.info(f"📄 Extracting PDF: {pdf_path}")
                
                # Extract text
                extract_result = pdf_extractor_tool.extract_all(pdf_path)
                
                if not extract_result.success:
                    logger.error(f"Failed to extract PDF: {extract_result.error}")
                    # Fallback to topic-based keywords
                    keywords = [topic] + topic.split()
                else:
                    pdf_content = extract_result.data.get('text', '')
                    logger.info(f"✅ Extracted {len(pdf_content)} characters")
                    
                    # AI extract keywords
                    keywords = await self._ai_extract_keywords(pdf_content)
            else:
                logger.warning("⚠️ No PDF downloaded, using topic as keywords")
                keywords = [topic] + topic.split()
            
            # Complete task
            task = self.complete_task(current_task, {
                'keywords_count': len(keywords),
                'pdf_extracted': bool(pdf_path),
                'content_length': len(pdf_content)
            })
            
            state = self.update_state(state, {
                'current_task': task,
                'search_queries': keywords  # Store keywords as search queries
            })
            
            return state
            
        except Exception as e:
            logger.error(f"Autonomous PDF analysis error: {str(e)}")
            return self.log_error(state, f"Autonomous PDF analysis failed: {str(e)}")
    
    async def _ai_extract_keywords(self, content: str) -> List[str]:
        """AI extract keywords từ PDF content"""
        try:
            logger.info("🧠 AI extracting keywords from PDF content...")
            
            # Truncate content if too long
            content_sample = content[:5000]
            
            prompt = f"""Bạn là chuyên gia phân tích văn bản luật pháp.

Nội dung văn bản (trích):
{content_sample}

Nhiệm vụ: Trích xuất 10-15 từ khóa QUAN TRỌNG NHẤT từ văn bản này.

Yêu cầu:
- Từ khóa liên quan đến chủ đề chính
- Bao gồm: khái niệm chính, quyền lợi, nghĩa vụ, quy định quan trọng
- Không lặp lại
- Ngắn gọn (1-3 từ mỗi keyword)

Trả về JSON array: ["keyword1", "keyword2", ...]
Chỉ JSON, không giải thích."""

            response = await self.llm.ainvoke([HumanMessage(content=prompt)])
            response_text = response.content.strip()
            
            # Parse JSON
            json_match = re.search(r'\[[\s\S]*\]', response_text)
            if json_match:
                keywords = json.loads(json_match.group(0))
                logger.info(f"✅ AI extracted {len(keywords)} keywords")
                logger.info(f"   Keywords: {', '.join(keywords[:5])}...")
                return keywords[:15]
            else:
                raise ValueError("Could not parse keywords")
                
        except Exception as e:
            logger.warning(f"AI keyword extraction failed: {str(e)}")
            # Fallback: simple extraction
            words = content[:2000].split()
            return list(set(words))[:10]


class AutonomousOpinionSearchAgent(BaseAgent):
    """
    Agent tự động search opinions sử dụng Ollama + Chrome
    
    Phase 3 của autonomous workflow:
    1. Nhận topic và keywords từ state
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
            name="Autonomous Opinion Search Agent",
            description="AI tự động search Chrome và crawl opinions"
        )
    
    async def execute(self, state: AgentState) -> AgentState:
        try:
            logger.info(f"🤖 {self.name} executing...")
            
            current_task = state.get('current_task')
            if not current_task or current_task.task_type != TaskType.AUTONOMOUS_OPINION_SEARCH:
                return state
            
            topic = state['project_name']
            keywords = state.get('search_queries', [])
            
            # Get search config from task input or use defaults
            max_articles = current_task.input_data.get('max_articles', 20)
            quality_threshold = current_task.input_data.get('quality_threshold', 0.6)
            
            logger.info("=" * 80)
            logger.info("🔍 PHASE 3: AI AUTONOMOUS SEARCH OPINIONS")
            logger.info("=" * 80)
            logger.info(f"Target: {max_articles} articles (quality >= {quality_threshold})")
            logger.info(f"Using {len(keywords)} keywords from PDF")
            
            # Enhance topic with keywords
            enhanced_topic = f"{topic} {' '.join(keywords[:3])}"
            
            # Run autonomous search
            result = ollama_autonomous_search_agent.autonomous_search_and_crawl(
                topic=enhanced_topic,
                max_articles=max_articles,
                max_search_pages=3,
                quality_threshold=quality_threshold
            )
            
            if not result.success:
                error_msg = result.error
                task = self.complete_task(current_task, {}, error=error_msg)
                return self.log_error(state, error_msg)
            
            opinions = result.data['opinions']
            logger.info(f"✅ Autonomous search complete: {len(opinions)} opinions collected")
            
            # Convert to standard format
            opinions_raw = []
            analyzed_opinions = []
            for op in opinions:
                opinion_data = {
                    'url': op['url'],
                    'title': op['title'],
                    'content': op['content'],
                    'source': op['source'],
                    'quality_score': op['quality_score'],
                    'quality_feedback': op['quality_feedback'],
                    'key_points': op.get('key_points', []),
                    'relevance': op.get('relevance', 'medium')
                }
                opinions_raw.append(opinion_data)
                
                # Add NLP analysis
                analyzed_opinions.append({
                    **opinion_data,
                    'sentiment': op.get('sentiment', 'neutral'),
                    'stance': op.get('stance', 'neutral'),
                    'stance_confidence': op.get('stance_confidence', 0),
                    'support_score': op.get('support_score', 0),
                    'oppose_score': op.get('oppose_score', 0)
                })
            
            task = self.complete_task(current_task, {
                'opinions_count': len(opinions),
                'average_quality': result.data['average_quality'],
                'sources': result.data['sources'],
                'sentiments': result.data.get('sentiments', {}),
                'stances': result.data.get('stances', {})
            })
            
            state = self.update_state(state, {
                'current_task': task,
                'opinions_raw': opinions_raw,
                'analyzed_opinions': analyzed_opinions,
                'csv_output_path': result.data.get('csv_path')
            })
            
            return state
            
        except Exception as e:
            logger.error(f"Autonomous opinion search error: {str(e)}")
            return self.log_error(state, f"Autonomous search failed: {str(e)}")


# Singleton instances
autonomous_law_search_agent = AutonomousLawSearchAgent()
autonomous_pdf_analysis_agent = AutonomousPdfAnalysisAgent()
autonomous_opinion_search_agent = AutonomousOpinionSearchAgent()
