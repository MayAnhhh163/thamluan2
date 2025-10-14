"""
Ollama Full Autonomous Workflow - AI điều khiển toàn bộ từ PDF đến Opinion Analysis
"""

import logging
import time
from typing import Dict, Any, Optional
from pathlib import Path

from core.config import config
from core.types import ToolResult
from tools.law_list_crawler import law_list_crawler
from tools.ollama_autonomous_search import ollama_autonomous_search_agent
from langchain_ollama import ChatOllama
from langchain.schema import HumanMessage
import json
import re

logger = logging.getLogger(__name__)


class OllamaFullAutonomousWorkflow:
    """
    Full AI-powered workflow:
    
    1. 🔍 AI tự động tìm PDF văn bản luật
    2. 📥 AI đánh giá và download PDFs relevant
    3. 📄 AI extract nội dung PDF
    4. 🧠 AI extract keywords từ PDF
    5. 🤖 AI autonomous search opinions
    6. 📊 AI phân tích sentiment/stance
    7. 💾 Export kết quả đầy đủ
    """
    
    def __init__(self):
        self.llm = ChatOllama(
            model=config.LLM_MODEL,
            base_url=config.OLLAMA_BASE_URL,
            temperature=0.3,
            num_predict=1024
        )
    
    def run_full_workflow(
        self,
        topic: str,
        max_opinions: int = 20,
        quality_threshold: float = 0.7
    ) -> ToolResult:
        """
        Chạy toàn bộ workflow tự động
        
        Args:
            topic: Chủ đề (ví dụ: "Luật Trí tuệ nhân tạo")
            max_opinions: Số opinions cần thu thập
            quality_threshold: Ngưỡng chất lượng
            
        Returns:
            ToolResult với kết quả đầy đủ
        """
        try:
            logger.info("=" * 80)
            logger.info("🤖 OLLAMA FULL AUTONOMOUS WORKFLOW")
            logger.info("=" * 80)
            logger.info(f"Topic: {topic}")
            logger.info("AI sẽ tự động xử lý TỒN BỘ workflow từ đầu đến cuối...")
            logger.info("=" * 80)
            
            workflow_result = {
                'topic': topic,
                'started_at': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # ====================================================================
            # PHASE 1: AI TÌM VÀ CRAWL PDF VĂN BẢN LUẬT
            # ====================================================================
            logger.info("\n" + "=" * 80)
            logger.info("📋 PHASE 1: AI TÌM VĂN BẢN LUẬT CHÍNH THỨC")
            logger.info("=" * 80)
            
            pdf_result = self._phase1_find_law_pdfs(topic)
            
            if not pdf_result['success']:
                return ToolResult(
                    success=False,
                    error=f"Phase 1 failed: {pdf_result['error']}"
                )
            
            workflow_result['law_documents'] = pdf_result['documents']
            workflow_result['pdf_downloaded'] = pdf_result.get('pdf_path')
            
            # ====================================================================
            # PHASE 2: AI EXTRACT VÀ PHÂN TÍCH PDF
            # ====================================================================
            logger.info("\n" + "=" * 80)
            logger.info("📄 PHASE 2: AI EXTRACT NỘI DUNG PDF")
            logger.info("=" * 80)
            
            if pdf_result.get('pdf_path'):
                extract_result = self._phase2_extract_pdf(pdf_result['pdf_path'])
                
                if extract_result['success']:
                    workflow_result['pdf_content'] = extract_result['content'][:1000]
                    workflow_result['keywords'] = extract_result['keywords']
                    
                    logger.info(f"✅ Extracted {len(extract_result['content'])} chars")
                    logger.info(f"✅ Found {len(extract_result['keywords'])} keywords")
            else:
                logger.warning("⚠️ No PDF downloaded, using topic as keywords")
                extract_result = {
                    'success': True,
                    'keywords': [topic] + topic.split()
                }
                workflow_result['keywords'] = extract_result['keywords']
            
            # ====================================================================
            # PHASE 3: AI AUTONOMOUS SEARCH OPINIONS
            # ====================================================================
            logger.info("\n" + "=" * 80)
            logger.info("🔍 PHASE 3: AI AUTONOMOUS SEARCH OPINIONS")
            logger.info("=" * 80)
            
            search_result = self._phase3_autonomous_search(
                topic=topic,
                keywords=extract_result['keywords'],
                max_opinions=max_opinions,
                quality_threshold=quality_threshold
            )
            
            if not search_result['success']:
                logger.warning(f"⚠️ Phase 3 warning: {search_result.get('error')}")
            
            workflow_result['opinions'] = search_result.get('opinions', [])
            workflow_result['sentiments'] = search_result.get('sentiments', {})
            workflow_result['stances'] = search_result.get('stances', {})
            workflow_result['csv_path'] = search_result.get('csv_path')
            
            # ====================================================================
            # FINAL REPORT
            # ====================================================================
            logger.info("\n" + "=" * 80)
            logger.info("📊 FULL WORKFLOW COMPLETE")
            logger.info("=" * 80)
            
            logger.info(f"\n📋 PHASE 1 - Văn bản luật:")
            logger.info(f"   Documents found: {len(workflow_result.get('law_documents', []))}")
            logger.info(f"   PDF downloaded: {'Yes' if workflow_result.get('pdf_downloaded') else 'No'}")
            
            logger.info(f"\n📄 PHASE 2 - PDF Analysis:")
            logger.info(f"   Keywords extracted: {len(workflow_result.get('keywords', []))}")
            logger.info(f"   Keywords: {', '.join(workflow_result.get('keywords', [])[:5])}")
            
            logger.info(f"\n🔍 PHASE 3 - Opinion Mining:")
            logger.info(f"   Opinions collected: {len(workflow_result.get('opinions', []))}")
            logger.info(f"   Sentiments: {workflow_result.get('sentiments', {})}")
            logger.info(f"   Stances: {workflow_result.get('stances', {})}")
            
            if workflow_result.get('csv_path'):
                logger.info(f"\n💾 Results exported to:")
                logger.info(f"   {workflow_result['csv_path']}")
            
            logger.info("\n" + "=" * 80)
            logger.info("✅ FULL AI WORKFLOW COMPLETED SUCCESSFULLY!")
            logger.info("=" * 80)
            
            return ToolResult(
                success=True,
                data=workflow_result,
                message="Full autonomous workflow completed"
            )
            
        except Exception as e:
            logger.error(f"Full workflow error: {str(e)}")
            return ToolResult(
                success=False,
                error=f"Workflow failed: {str(e)}"
            )
    
    def _phase1_find_law_pdfs(self, topic: str) -> Dict[str, Any]:
        """
        Phase 1: AI tìm và download PDF văn bản luật
        """
        try:
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
                logger.error(f"Failed to search law documents: {result.error}")
                return {
                    'success': False,
                    'error': result.error
                }
            
            documents = result.data['documents']
            logger.info(f"✅ Found {len(documents)} relevant law documents")
            
            if not documents:
                return {
                    'success': False,
                    'error': 'No relevant law documents found'
                }
            
            # AI đánh giá document nào tốt nhất
            best_doc = self._ai_select_best_document(documents, topic)
            
            if best_doc and best_doc.pdf_url:
                logger.info(f"📥 Downloading PDF: {best_doc.title}")
                
                # Download PDF
                from tools.pdf_downloader import pdf_downloader
                pdf_result = pdf_downloader.download_pdf(
                    url=best_doc.pdf_url,
                    doc_id=best_doc.doc_id,
                    filename=f"{best_doc.doc_id}.pdf"
                )
                
                if pdf_result.success:
                    logger.info(f"✅ PDF downloaded: {pdf_result.data['path']}")
                    return {
                        'success': True,
                        'documents': [doc.to_dict() for doc in documents],
                        'best_document': best_doc.to_dict(),
                        'pdf_path': pdf_result.data['path']
                    }
            
            # Fallback: không có PDF
            return {
                'success': True,
                'documents': [doc.to_dict() for doc in documents],
                'best_document': documents[0].to_dict() if documents else None,
                'pdf_path': None
            }
            
        except Exception as e:
            logger.error(f"Phase 1 error: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _ai_select_best_document(self, documents, topic: str):
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

            response = self.llm.invoke([HumanMessage(content=prompt)])
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
    
    def _phase2_extract_pdf(self, pdf_path: str) -> Dict[str, Any]:
        """
        Phase 2: AI extract và phân tích PDF
        """
        try:
            logger.info(f"📄 Extracting PDF: {pdf_path}")
            
            from tools.pdf_extractor import pdf_extractor_tool
            
            # Extract text
            extract_result = pdf_extractor_tool.extract_all(pdf_path)
            
            if not extract_result.success:
                logger.error(f"Failed to extract PDF: {extract_result.error}")
                return {
                    'success': False,
                    'error': extract_result.error
                }
            
            content = extract_result.data.get('text', '')
            logger.info(f"✅ Extracted {len(content)} characters")
            
            # AI extract keywords
            keywords = self._ai_extract_keywords(content)
            
            return {
                'success': True,
                'content': content,
                'keywords': keywords
            }
            
        except Exception as e:
            logger.error(f"Phase 2 error: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _ai_extract_keywords(self, content: str) -> list:
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

            response = self.llm.invoke([HumanMessage(content=prompt)])
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
    
    def _phase3_autonomous_search(
        self,
        topic: str,
        keywords: list,
        max_opinions: int,
        quality_threshold: float
    ) -> Dict[str, Any]:
        """
        Phase 3: AI autonomous search opinions
        """
        try:
            logger.info(f"🔍 Starting autonomous opinion search...")
            logger.info(f"   Using {len(keywords)} keywords from PDF")
            
            # Enhance topic with keywords
            enhanced_topic = f"{topic} {' '.join(keywords[:3])}"
            
            result = ollama_autonomous_search_agent.autonomous_search_and_crawl(
                topic=enhanced_topic,
                max_articles=max_opinions,
                quality_threshold=quality_threshold
            )
            
            if result.success:
                return {
                    'success': True,
                    'opinions': result.data.get('opinions', []),
                    'sentiments': result.data.get('sentiments', {}),
                    'stances': result.data.get('stances', {}),
                    'csv_path': result.data.get('csv_path')
                }
            else:
                return {
                    'success': False,
                    'error': result.error
                }
                
        except Exception as e:
            logger.error(f"Phase 3 error: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }


# Singleton instance
ollama_full_autonomous_workflow = OllamaFullAutonomousWorkflow()
