"""
Ollama Opinion Enhancer - Sử dụng Ollama LLM để nâng cao chất lượng thu thập opinions
"""

import logging
import json
import re
from typing import List, Dict, Any, Optional
from langchain_ollama import ChatOllama
from langchain.schema import HumanMessage, SystemMessage

from core.config import config
from core.types import ToolResult

logger = logging.getLogger(__name__)


class OllamaOpinionEnhancer:
    """
    Sử dụng Ollama LLM để:
    1. Sinh search queries thông minh từ keywords
    2. Đánh giá chất lượng opinions
    3. Trích xuất insights chính từ opinions
    4. Phát hiện duplicate/similar opinions
    5. Tạo summary và categorize opinions
    """
    
    def __init__(self):
        self.llm = ChatOllama(
            model=config.LLM_MODEL,
            base_url=config.OLLAMA_BASE_URL,
            temperature=0.7,  # Higher for creative queries
            num_predict=2048
        )
        
        self.llm_analytical = ChatOllama(
            model=config.LLM_MODEL,
            base_url=config.OLLAMA_BASE_URL,
            temperature=0.2,  # Lower for analytical tasks
            num_predict=1024
        )
    
    def generate_smart_search_queries(
        self, 
        topic: str, 
        keywords: List[str], 
        num_queries: int = 10
    ) -> ToolResult:
        """
        Sinh ra các search queries thông minh để tìm opinions
        
        Args:
            topic: Chủ đề chính (ví dụ: "Luật Trí tuệ nhân tạo")
            keywords: Danh sách keywords từ PDF
            num_queries: Số lượng queries cần sinh
            
        Returns:
            ToolResult với list search queries
        """
        try:
            logger.info(f"🤖 Generating {num_queries} smart search queries using Ollama...")
            
            prompt = f"""Bạn là chuyên gia tìm kiếm thông tin về luật pháp Việt Nam.

Chủ đề: "{topic}"
Keywords liên quan: {', '.join(keywords[:20])}

Nhiệm vụ: Tạo {num_queries} câu tìm kiếm (search queries) để tìm ý kiến, bình luận, phản hồi về chủ đề này trên các trang báo Việt Nam.

Yêu cầu:
1. Mỗi query nên:
   - Kết hợp chủ đề với các từ khóa như: "ý kiến", "phản hồi", "bình luận", "tranh luận", "góp ý"
   - Đa dạng: vừa query chung, vừa query cụ thể về từng khía cạnh
   - Tự nhiên như cách người Việt tìm kiếm
   - Không quá dài (5-10 từ)
   
2. Tập trung vào:
   - Ý kiến chuyên gia
   - Phản hồi của doanh nghiệp, tổ chức
   - Góp ý của người dân
   - Tranh luận, thảo luận
   - Phân tích tác động
   
3. Tránh:
   - Query quá chung chung
   - Lặp lại nội dung
   - Từ ngữ không tự nhiên

Chỉ trả về JSON array các queries, không giải thích:
["query 1", "query 2", ...]"""

            messages = [HumanMessage(content=prompt)]
            response = self.llm.invoke(messages)
            response_text = response.content.strip()
            
            # Parse JSON
            json_match = re.search(r'\[[\s\S]*\]', response_text)
            if json_match:
                queries = json.loads(json_match.group(0))
                logger.info(f"✅ Generated {len(queries)} search queries")
                
                # Log a few examples
                for i, q in enumerate(queries[:3], 1):
                    logger.info(f"   {i}. {q}")
                
                return ToolResult(
                    success=True,
                    data={'queries': queries[:num_queries]}
                )
            else:
                raise ValueError("Could not parse JSON response from LLM")
                
        except Exception as e:
            logger.error(f"Error generating queries: {str(e)}")
            # Fallback to basic queries
            fallback_queries = self._generate_fallback_queries(topic, keywords)
            return ToolResult(
                success=True,
                data={'queries': fallback_queries[:num_queries]},
                metadata={'method': 'fallback', 'error': str(e)}
            )
    
    def _generate_fallback_queries(self, topic: str, keywords: List[str]) -> List[str]:
        """Fallback query generation without LLM"""
        queries = [
            f"{topic} ý kiến chuyên gia",
            f"{topic} phản hồi doanh nghiệp",
            f"{topic} góp ý người dân",
            f"{topic} tranh luận",
            f"{topic} bình luận",
        ]
        
        # Add keyword-based queries
        for kw in keywords[:5]:
            queries.append(f"{topic} {kw} ý kiến")
        
        return queries
    
    def evaluate_opinion_quality(
        self, 
        opinion: Dict[str, Any],
        topic: str
    ) -> ToolResult:
        """
        Đánh giá chất lượng của một opinion
        
        Args:
            opinion: Dict với 'title', 'content', 'url', etc.
            topic: Chủ đề chính để đánh giá relevance
            
        Returns:
            ToolResult với quality score và feedback
        """
        try:
            title = opinion.get('title', '')
            content = opinion.get('content', '')[:2000]  # First 2000 chars
            
            if len(content) < 100:
                return ToolResult(
                    success=True,
                    data={
                        'quality_score': 0.2,
                        'is_valuable': False,
                        'feedback': 'Nội dung quá ngắn',
                        'relevance': 'low'
                    }
                )
            
            prompt = f"""Bạn là chuyên gia đánh giá chất lượng ý kiến về luật pháp.

Chủ đề: "{topic}"

Tiêu đề: {title}
Nội dung: {content}

Đánh giá ý kiến này theo các tiêu chí:
1. Relevance (liên quan đến chủ đề): 0-10
2. Depth (độ sâu phân tích): 0-10  
3. Originality (tính độc đáo, không sao chép): 0-10
4. Credibility (độ tin cậy, có dẫn chứng): 0-10
5. Value (giá trị thông tin): 0-10

Trả về JSON:
{{
    "relevance_score": 0-10,
    "depth_score": 0-10,
    "originality_score": 0-10,
    "credibility_score": 0-10,
    "value_score": 0-10,
    "overall_score": 0-10,
    "is_valuable": true/false,
    "relevance": "high/medium/low",
    "feedback": "Nhận xét ngắn gọn",
    "key_points": ["điểm chính 1", "điểm chính 2", ...]
}}

Chỉ trả về JSON, không giải thích."""

            messages = [HumanMessage(content=prompt)]
            response = self.llm_analytical.invoke(messages)
            response_text = response.content.strip()
            
            # Parse JSON
            json_match = re.search(r'\{[\s\S]*\}', response_text)
            if json_match:
                result = json.loads(json_match.group(0))
                
                # Calculate quality_score (0-1)
                overall = result.get('overall_score', 5)
                result['quality_score'] = overall / 10.0
                
                logger.info(f"Quality: {result['quality_score']:.2f} - {result.get('feedback', '')[:50]}")
                
                return ToolResult(success=True, data=result)
            else:
                raise ValueError("Could not parse JSON response")
                
        except Exception as e:
            logger.error(f"Error evaluating opinion: {str(e)}")
            # Return neutral score
            return ToolResult(
                success=True,
                data={
                    'quality_score': 0.5,
                    'is_valuable': True,
                    'feedback': f'Error: {str(e)}',
                    'relevance': 'medium'
                },
                metadata={'method': 'fallback'}
            )
    
    def extract_insights(
        self, 
        opinions: List[Dict[str, Any]],
        topic: str,
        max_opinions: int = 20
    ) -> ToolResult:
        """
        Trích xuất insights chính từ nhiều opinions
        
        Args:
            opinions: List của opinions
            topic: Chủ đề
            max_opinions: Số lượng opinions tối đa để phân tích
            
        Returns:
            ToolResult với insights summary
        """
        try:
            logger.info(f"🤖 Extracting insights from {len(opinions)} opinions...")
            
            # Combine opinion content
            combined_text = ""
            for i, op in enumerate(opinions[:max_opinions], 1):
                title = op.get('title', '')
                content = op.get('content', '')[:500]  # First 500 chars each
                combined_text += f"\n\n--- Ý kiến {i} ---\nTiêu đề: {title}\nNội dung: {content}"
            
            prompt = f"""Bạn là chuyên gia phân tích dư luận về luật pháp.

Chủ đề: "{topic}"

Dưới đây là {min(len(opinions), max_opinions)} ý kiến từ báo chí và công chúng:
{combined_text[:8000]}

Nhiệm vụ: Tổng hợp và phân tích các ý kiến này.

Trả về JSON:
{{
    "main_themes": ["chủ đề chính 1", "chủ đề chính 2", ...],
    "supporting_views": ["quan điểm ủng hộ 1", "quan điểm ủng hộ 2", ...],
    "opposing_views": ["quan điểm phản đối 1", "quan điểm phản đối 2", ...],
    "concerns": ["mối quan ngại 1", "mối quan ngại 2", ...],
    "recommendations": ["đề xuất 1", "đề xuất 2", ...],
    "sentiment_distribution": {{
        "positive": 0-100,
        "negative": 0-100,
        "neutral": 0-100
    }},
    "overall_summary": "Tóm tắt chung về dư luận"
}}

Chỉ trả về JSON."""

            messages = [HumanMessage(content=prompt)]
            response = self.llm_analytical.invoke(messages)
            response_text = response.content.strip()
            
            # Parse JSON
            json_match = re.search(r'\{[\s\S]*\}', response_text)
            if json_match:
                insights = json.loads(json_match.group(0))
                
                logger.info("✅ Insights extracted:")
                logger.info(f"   Main themes: {len(insights.get('main_themes', []))}")
                logger.info(f"   Supporting views: {len(insights.get('supporting_views', []))}")
                logger.info(f"   Opposing views: {len(insights.get('opposing_views', []))}")
                
                return ToolResult(success=True, data=insights)
            else:
                raise ValueError("Could not parse JSON response")
                
        except Exception as e:
            logger.error(f"Error extracting insights: {str(e)}")
            return ToolResult(
                success=False,
                error=f"Failed to extract insights: {str(e)}"
            )
    
    def categorize_opinions(
        self, 
        opinions: List[Dict[str, Any]],
        categories: Optional[List[str]] = None
    ) -> ToolResult:
        """
        Phân loại opinions vào các categories
        
        Args:
            opinions: List opinions
            categories: Custom categories (optional)
            
        Returns:
            ToolResult với categorized opinions
        """
        try:
            if not categories:
                categories = [
                    "Chuyên gia pháp lý",
                    "Doanh nghiệp/Hiệp hội",
                    "Người dân",
                    "Cơ quan nhà nước",
                    "Học giả/Nghiên cứu",
                    "Báo chí/Phân tích"
                ]
            
            logger.info(f"🤖 Categorizing {len(opinions)} opinions into {len(categories)} categories...")
            
            categorized = {cat: [] for cat in categories}
            categorized['Khác'] = []
            
            for opinion in opinions[:50]:  # Limit to 50 for performance
                title = opinion.get('title', '')
                content = opinion.get('content', '')[:500]
                
                prompt = f"""Phân loại ý kiến sau vào MỘT trong các nhóm:
{json.dumps(categories, ensure_ascii=False)}

Tiêu đề: {title}
Nội dung: {content}

Chỉ trả về tên category (chính xác như trong list), không giải thích."""

                try:
                    messages = [HumanMessage(content=prompt)]
                    response = self.llm_analytical.invoke(messages)
                    category = response.content.strip()
                    
                    # Find matching category
                    matched = False
                    for cat in categories:
                        if cat.lower() in category.lower() or category.lower() in cat.lower():
                            categorized[cat].append(opinion)
                            matched = True
                            break
                    
                    if not matched:
                        categorized['Khác'].append(opinion)
                        
                except Exception as e:
                    logger.warning(f"Error categorizing opinion: {str(e)}")
                    categorized['Khác'].append(opinion)
            
            # Summary
            summary = {cat: len(ops) for cat, ops in categorized.items() if ops}
            logger.info(f"✅ Categorization complete: {summary}")
            
            return ToolResult(
                success=True,
                data={
                    'categorized': categorized,
                    'summary': summary
                }
            )
            
        except Exception as e:
            logger.error(f"Error categorizing opinions: {str(e)}")
            return ToolResult(
                success=False,
                error=f"Failed to categorize: {str(e)}"
            )
    
    def detect_duplicate_opinions(
        self, 
        opinions: List[Dict[str, Any]],
        similarity_threshold: float = 0.8
    ) -> ToolResult:
        """
        Phát hiện các opinions duplicate hoặc tương tự nhau
        
        Returns:
            ToolResult với unique opinions và duplicate groups
        """
        try:
            logger.info(f"🤖 Detecting duplicates in {len(opinions)} opinions...")
            
            # Simple hash-based deduplication first
            seen_hashes = set()
            unique_opinions = []
            duplicates = []
            
            for op in opinions:
                content = op.get('content', '')
                content_hash = hash(content[:500])  # Hash first 500 chars
                
                if content_hash in seen_hashes:
                    duplicates.append(op)
                else:
                    seen_hashes.add(content_hash)
                    unique_opinions.append(op)
            
            logger.info(f"✅ Found {len(unique_opinions)} unique opinions, {len(duplicates)} duplicates")
            
            return ToolResult(
                success=True,
                data={
                    'unique_opinions': unique_opinions,
                    'duplicates': duplicates,
                    'unique_count': len(unique_opinions),
                    'duplicate_count': len(duplicates)
                }
            )
            
        except Exception as e:
            logger.error(f"Error detecting duplicates: {str(e)}")
            return ToolResult(
                success=False,
                error=f"Failed to detect duplicates: {str(e)}"
            )


# Singleton instance
ollama_opinion_enhancer = OllamaOpinionEnhancer()
