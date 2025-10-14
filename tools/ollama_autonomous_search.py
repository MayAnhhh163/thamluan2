"""
Ollama Autonomous Search Agent - AI tự động search Chrome, đánh giá, và crawl opinions
"""

import logging
import time
import json
from typing import List, Dict, Any, Optional
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException
from bs4 import BeautifulSoup
from langchain_ollama import ChatOllama
from langchain.schema import HumanMessage
import re

# Try to use undetected-chromedriver to bypass bot detection
try:
    import undetected_chromedriver as uc
    UNDETECTED_AVAILABLE = True
    logger = logging.getLogger(__name__)
    logger.info("✅ Using undetected-chromedriver for bot bypass")
except ImportError:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    UNDETECTED_AVAILABLE = False
    logger = logging.getLogger(__name__)
    logger.warning("⚠️ undetected-chromedriver not available, using regular Selenium")

from core.config import config
from core.types import ToolResult

logger = logging.getLogger(__name__)


class OllamaAutonomousSearchAgent:
    """
    AI Agent tự động:
    1. Mở Chrome và search Google
    2. Dùng Ollama để đánh giá kết quả search có relevant không
    3. Click vào link relevant
    4. Crawl nội dung
    5. Dùng Ollama để phân tích nội dung
    6. Lặp lại cho đến khi đủ opinions
    """
    
    def __init__(self):
        self.driver = None
        self.llm = ChatOllama(
            model=config.LLM_MODEL,
            base_url=config.OLLAMA_BASE_URL,
            temperature=0.3,  # Lower for decision making
            num_predict=512
        )
        
        self.llm_analyzer = ChatOllama(
            model=config.LLM_MODEL,
            base_url=config.OLLAMA_BASE_URL,
            temperature=0.2,
            num_predict=1024
        )
    
    def _setup_driver(self):
        """Setup Chrome driver with bot detection bypass"""
        try:
            if UNDETECTED_AVAILABLE:
                # Use undetected-chromedriver to bypass bot detection
                options = uc.ChromeOptions()
                options.add_argument("--disable-blink-features=AutomationControlled")
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument("--no-sandbox")
                options.add_argument("--window-size=1920,1080")
                
                self.driver = uc.Chrome(options=options, version_main=None)
                self.driver.set_page_load_timeout(30)
                
                logger.info("✅ Chrome driver initialized (undetected mode)")
            else:
                # Fallback to regular Selenium with stealth settings
                from selenium import webdriver
                from selenium.webdriver.chrome.options import Options
                
                chrome_options = Options()
                # chrome_options.add_argument("--headless")  # Comment for visible
                chrome_options.add_argument("--disable-gpu")
                chrome_options.add_argument("--no-sandbox")
                chrome_options.add_argument("--disable-dev-shm-usage")
                chrome_options.add_argument("--disable-blink-features=AutomationControlled")
                chrome_options.add_argument("--window-size=1920,1080")
                chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
                chrome_options.add_experimental_option('useAutomationExtension', False)
                
                chrome_options.add_argument(
                    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
                )
                
                self.driver = webdriver.Chrome(options=chrome_options)
                self.driver.set_page_load_timeout(30)
                
                # Execute script to hide webdriver property
                self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                
                logger.info("✅ Chrome driver initialized (stealth mode)")
            
        except WebDriverException as e:
            logger.error(f"Failed to initialize Chrome: {str(e)}")
            raise
    
    def _cleanup_driver(self):
        """Đóng driver"""
        if self.driver:
            try:
                self.driver.quit()
                logger.info("✅ Chrome driver closed")
            except Exception as e:
                logger.warning(f"Error closing driver: {str(e)}")
    
    def autonomous_search_and_crawl(
        self,
        topic: str,
        max_articles: int = 20,
        max_search_pages: int = 3,
        quality_threshold: float = 0.6
    ) -> ToolResult:
        """
        AI tự động search và crawl opinions
        
        Args:
            topic: Chủ đề cần tìm (ví dụ: "Luật Trí tuệ nhân tạo ý kiến chuyên gia")
            max_articles: Số lượng bài viết tối đa cần thu thập
            max_search_pages: Số trang search tối đa
            quality_threshold: Ngưỡng chất lượng (0-1)
            
        Returns:
            ToolResult với list opinions
        """
        try:
            logger.info("=" * 80)
            logger.info("🤖 OLLAMA AUTONOMOUS SEARCH AGENT")
            logger.info("=" * 80)
            logger.info(f"Topic: {topic}")
            logger.info(f"Target: {max_articles} high-quality articles")
            logger.info(f"Quality threshold: {quality_threshold}")
            
            # Setup driver
            self._setup_driver()
            
            collected_opinions = []
            visited_urls = set()
            
            # Step 1: Generate search queries using Ollama
            search_queries = self._generate_search_queries(topic)
            logger.info(f"📝 Generated {len(search_queries)} search queries")
            
            # Step 2: For each query, search and collect
            for query_idx, query in enumerate(search_queries, 1):
                if len(collected_opinions) >= max_articles:
                    logger.info(f"✅ Reached target: {max_articles} articles")
                    break
                
                logger.info(f"\n{'='*60}")
                logger.info(f"🔍 Query {query_idx}/{len(search_queries)}: '{query}'")
                logger.info(f"{'='*60}")
                
                # Search Google
                search_results = self._search_google(query)
                logger.info(f"Found {len(search_results)} search results")
                
                # Step 3: Evaluate each result with Ollama
                for result_idx, result in enumerate(search_results, 1):
                    if len(collected_opinions) >= max_articles:
                        break
                    
                    url = result['url']
                    title = result['title']
                    snippet = result.get('snippet', '')
                    
                    # Skip if already visited
                    if url in visited_urls:
                        logger.debug(f"  [{result_idx}] Already visited: {title[:50]}")
                        continue
                    
                    visited_urls.add(url)
                    
                    logger.info(f"\n  [{result_idx}] Evaluating: {title[:60]}...")
                    
                    # Ask Ollama: Should we crawl this?
                    should_crawl = self._should_crawl_url(title, snippet, topic)
                    
                    if not should_crawl:
                        logger.info(f"      ❌ Ollama says: Not relevant, skip")
                        continue
                    
                    logger.info(f"      ✅ Ollama says: Relevant! Crawling...")
                    
                    # Step 4: Crawl the page
                    content_result = self._crawl_page(url, title)
                    
                    if not content_result['success']:
                        logger.warning(f"      ⚠️ Failed to crawl: {content_result.get('error')}")
                        continue
                    
                    content = content_result['content']
                    logger.info(f"      📄 Crawled {len(content)} chars")
                    
                    # Step 5: Analyze quality with Ollama
                    quality_result = self._analyze_content_quality(title, content, topic)
                    
                    quality_score = quality_result['quality_score']
                    is_valuable = quality_result['is_valuable']
                    
                    logger.info(f"      ⭐ Quality: {quality_score:.2f} - {quality_result['feedback'][:50]}")
                    
                    if quality_score >= quality_threshold and is_valuable:
                        opinion = {
                            'url': url,
                            'title': title,
                            'content': content,
                            'snippet': snippet,
                            'quality_score': quality_score,
                            'quality_feedback': quality_result['feedback'],
                            'key_points': quality_result.get('key_points', []),
                            'relevance': quality_result.get('relevance', 'medium'),
                            'source': self._extract_domain(url),
                            'search_query': query
                        }
                        
                        collected_opinions.append(opinion)
                        logger.info(f"      💾 Saved! Total: {len(collected_opinions)}/{max_articles}")
                    else:
                        logger.info(f"      ❌ Quality too low ({quality_score:.2f} < {quality_threshold})")
                    
                    # Sleep to avoid rate limiting
                    time.sleep(2)
            
            # Cleanup
            self._cleanup_driver()
            
            # Final report
            logger.info("\n" + "=" * 80)
            logger.info("📊 AUTONOMOUS SEARCH COMPLETE")
            logger.info("=" * 80)
            logger.info(f"✅ Collected: {len(collected_opinions)} high-quality opinions")
            logger.info(f"🔍 Visited: {len(visited_urls)} URLs")
            logger.info(f"📝 Used: {len(search_queries)} search queries")
            
            # Statistics
            avg_quality = sum(op['quality_score'] for op in collected_opinions) / len(collected_opinions) if collected_opinions else 0
            logger.info(f"⭐ Average quality: {avg_quality:.2f}")
            
            sources = {}
            for op in collected_opinions:
                src = op['source']
                sources[src] = sources.get(src, 0) + 1
            
            logger.info(f"📰 Sources: {sources}")
            
            return ToolResult(
                success=True,
                data={
                    'opinions': collected_opinions,
                    'count': len(collected_opinions),
                    'visited_urls': len(visited_urls),
                    'average_quality': avg_quality,
                    'sources': sources
                },
                message=f"Collected {len(collected_opinions)} high-quality opinions"
            )
            
        except Exception as e:
            logger.error(f"Autonomous search error: {str(e)}")
            self._cleanup_driver()
            return ToolResult(
                success=False,
                error=f"Autonomous search failed: {str(e)}"
            )
    
    def _generate_search_queries(self, topic: str) -> List[str]:
        """Dùng Ollama để sinh search queries"""
        try:
            prompt = f"""Bạn là chuyên gia tìm kiếm thông tin về luật pháp Việt Nam.

Chủ đề: "{topic}"

Tạo 5 câu tìm kiếm (search queries) tiếng Việt để tìm ý kiến, bình luận chất lượng cao về chủ đề này.

Yêu cầu:
1. Mỗi query khác nhau (đa dạng góc nhìn)
2. Tập trung vào: ý kiến chuyên gia, phản hồi, góp ý, tranh luận
3. Tự nhiên như người Việt search Google
4. 5-10 từ mỗi query

Trả về JSON array: ["query 1", "query 2", ...]
Chỉ JSON, không giải thích."""

            response = self.llm.invoke([HumanMessage(content=prompt)])
            response_text = response.content.strip()
            
            # Parse JSON
            json_match = re.search(r'\[[\s\S]*\]', response_text)
            if json_match:
                queries = json.loads(json_match.group(0))
                return queries[:5]
            else:
                # Fallback
                return [
                    f"{topic} ý kiến chuyên gia",
                    f"{topic} phản hồi",
                    f"{topic} tranh luận",
                    f"{topic} góp ý"
                ]
                
        except Exception as e:
            logger.warning(f"Error generating queries: {str(e)}")
            return [f"{topic} ý kiến", f"{topic} phản hồi"]
    
    def _search_google(self, query: str) -> List[Dict[str, str]]:
        """Search Google và lấy kết quả"""
        try:
            # Navigate to Google
            self.driver.get("https://www.google.com")
            time.sleep(3)  # Wait longer for page load
            
            # Check if CAPTCHA or bot detection page
            page_source = self.driver.page_source.lower()
            if 'captcha' in page_source or 'unusual traffic' in page_source:
                logger.warning("⚠️ Google detected bot, trying DuckDuckGo instead...")
                return self._search_duckduckgo(query)
            
            # Find search box
            try:
                search_box = self.driver.find_element(By.NAME, "q")
            except NoSuchElementException:
                # Try alternative selector
                try:
                    search_box = self.driver.find_element(By.CSS_SELECTOR, "textarea[name='q']")
                except NoSuchElementException:
                    logger.error("Cannot find Google search box, using DuckDuckGo")
                    return self._search_duckduckgo(query)
            
            search_box.clear()
            search_box.send_keys(query)
            search_box.send_keys(Keys.RETURN)
            
            # Wait for results
            time.sleep(4)
            
            # Check again for CAPTCHA
            page_source = self.driver.page_source.lower()
            if 'captcha' in page_source or 'unusual traffic' in page_source:
                logger.warning("⚠️ Google CAPTCHA detected, switching to DuckDuckGo...")
                return self._search_duckduckgo(query)
            
            # Parse results
            results = []
            
            # Find all search result divs
            search_results = self.driver.find_elements(By.CSS_SELECTOR, "div.g")
            
            for result in search_results[:10]:  # Top 10 results
                try:
                    # Extract link
                    link_elem = result.find_element(By.CSS_SELECTOR, "a")
                    url = link_elem.get_attribute("href")
                    
                    # Extract title
                    title_elem = result.find_element(By.CSS_SELECTOR, "h3")
                    title = title_elem.text
                    
                    # Extract snippet
                    try:
                        snippet_elem = result.find_element(By.CSS_SELECTOR, "div.VwiC3b")
                        snippet = snippet_elem.text
                    except:
                        snippet = ""
                    
                    if url and title and url.startswith('http'):
                        results.append({
                            'url': url,
                            'title': title,
                            'snippet': snippet
                        })
                        
                except Exception as e:
                    continue
            
            if not results:
                logger.warning("No results from Google, trying DuckDuckGo...")
                return self._search_duckduckgo(query)
            
            return results
            
        except Exception as e:
            logger.error(f"Google search error: {str(e)}, falling back to DuckDuckGo")
            return self._search_duckduckgo(query)
    
    def _search_duckduckgo(self, query: str) -> List[Dict[str, str]]:
        """Search DuckDuckGo (không có bot detection)"""
        try:
            logger.info("🦆 Searching on DuckDuckGo...")
            
            # Navigate to DuckDuckGo
            self.driver.get("https://duckduckgo.com")
            time.sleep(2)
            
            # Find search box
            search_box = self.driver.find_element(By.NAME, "q")
            search_box.clear()
            search_box.send_keys(query)
            search_box.send_keys(Keys.RETURN)
            
            # Wait for results
            time.sleep(3)
            
            # Parse results
            results = []
            
            # DuckDuckGo results selector
            search_results = self.driver.find_elements(By.CSS_SELECTOR, "article[data-testid='result']")
            
            if not search_results:
                # Try alternative selector
                search_results = self.driver.find_elements(By.CSS_SELECTOR, "li[data-layout='organic']")
            
            for result in search_results[:10]:  # Top 10 results
                try:
                    # Extract link
                    link_elem = result.find_element(By.CSS_SELECTOR, "a[href]")
                    url = link_elem.get_attribute("href")
                    
                    # Extract title
                    title_elem = result.find_element(By.CSS_SELECTOR, "h2")
                    title = title_elem.text
                    
                    # Extract snippet
                    try:
                        snippet_elem = result.find_element(By.CSS_SELECTOR, "div[data-result='snippet']")
                        snippet = snippet_elem.text
                    except:
                        snippet = ""
                    
                    if url and title and url.startswith('http'):
                        results.append({
                            'url': url,
                            'title': title,
                            'snippet': snippet
                        })
                        
                except Exception as e:
                    continue
            
            logger.info(f"✅ DuckDuckGo found {len(results)} results")
            return results
            
        except Exception as e:
            logger.error(f"DuckDuckGo search error: {str(e)}")
            return []
    
    def _should_crawl_url(self, title: str, snippet: str, topic: str) -> bool:
        """Dùng Ollama để quyết định có nên crawl URL này không"""
        try:
            prompt = f"""Bạn là AI đánh giá kết quả tìm kiếm.

Chủ đề quan tâm: "{topic}"

Kết quả tìm kiếm:
Tiêu đề: {title}
Mô tả: {snippet}

Câu hỏi: Bài viết này có khả năng chứa ý kiến, phản hồi, hoặc phân tích chất lượng về chủ đề không?

Trả lời CHÍNH XÁC một từ:
- "YES" nếu relevant và có giá trị (ý kiến chuyên gia, phân tích, góp ý)
- "NO" nếu không relevant hoặc là tin tức chung chung

Chỉ trả về YES hoặc NO."""

            response = self.llm.invoke([HumanMessage(content=prompt)])
            decision = response.content.strip().upper()
            
            return "YES" in decision
            
        except Exception as e:
            logger.warning(f"Error in should_crawl: {str(e)}")
            # Default to True (crawl anyway)
            return True
    
    def _crawl_page(self, url: str, title: str) -> Dict[str, Any]:
        """Crawl nội dung từ URL"""
        try:
            self.driver.get(url)
            time.sleep(3)
            
            # Get page source
            page_source = self.driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            
            # Remove script, style tags
            for tag in soup(['script', 'style', 'nav', 'footer', 'header']):
                tag.decompose()
            
            # Extract main content
            # Try common article selectors
            content = ""
            
            article_selectors = [
                'article',
                'div.article-content',
                'div.content',
                'div.post-content',
                'div.entry-content',
                'main',
            ]
            
            for selector in article_selectors:
                article = soup.select_one(selector)
                if article:
                    content = article.get_text(separator='\n', strip=True)
                    break
            
            # Fallback: get body text
            if not content or len(content) < 200:
                body = soup.find('body')
                if body:
                    content = body.get_text(separator='\n', strip=True)
            
            # Clean content
            lines = [line.strip() for line in content.split('\n') if line.strip()]
            content = '\n'.join(lines)
            
            # Limit length
            if len(content) > 10000:
                content = content[:10000]
            
            if len(content) < 100:
                return {
                    'success': False,
                    'error': 'Content too short'
                }
            
            return {
                'success': True,
                'content': content,
                'length': len(content)
            }
            
        except Exception as e:
            logger.error(f"Crawl error: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _analyze_content_quality(
        self, 
        title: str, 
        content: str, 
        topic: str
    ) -> Dict[str, Any]:
        """Dùng Ollama phân tích chất lượng nội dung"""
        try:
            # Truncate content
            content_sample = content[:2000]
            
            prompt = f"""Bạn là chuyên gia đánh giá ý kiến về luật pháp.

Chủ đề: "{topic}"

Tiêu đề: {title}
Nội dung (trích): {content_sample}

Đánh giá:
1. Có liên quan trực tiếp đến chủ đề? (0-10)
2. Có chứa ý kiến, phân tích chuyên sâu? (0-10)
3. Độ tin cậy, có dẫn chứng? (0-10)

Trả về JSON:
{{
    "relevance_score": 0-10,
    "depth_score": 0-10,
    "credibility_score": 0-10,
    "overall_score": 0-10,
    "is_valuable": true/false,
    "feedback": "Nhận xét ngắn (1 câu)",
    "relevance": "high/medium/low",
    "key_points": ["điểm 1", "điểm 2"]
}}

Chỉ JSON, không giải thích."""

            response = self.llm_analyzer.invoke([HumanMessage(content=prompt)])
            response_text = response.content.strip()
            
            # Parse JSON
            json_match = re.search(r'\{[\s\S]*\}', response_text)
            if json_match:
                result = json.loads(json_match.group(0))
                result['quality_score'] = result.get('overall_score', 5) / 10.0
                return result
            else:
                raise ValueError("Could not parse JSON")
                
        except Exception as e:
            logger.warning(f"Error analyzing quality: {str(e)}")
            return {
                'quality_score': 0.5,
                'is_valuable': True,
                'feedback': 'Error in analysis',
                'relevance': 'medium',
                'key_points': []
            }
    
    def _extract_domain(self, url: str) -> str:
        """Extract domain from URL"""
        try:
            from urllib.parse import urlparse
            parsed = urlparse(url)
            domain = parsed.netloc
            # Remove www.
            if domain.startswith('www.'):
                domain = domain[4:]
            return domain
        except:
            return 'unknown'


# Singleton instance
ollama_autonomous_search_agent = OllamaAutonomousSearchAgent()
