# Autonomous AI Agent - LangGraph Framework

## Overview

Hệ thống AI Agent hoàn toàn tự động, sử dụng LangGraph framework để thu thập và phân tích ý kiến về dự luật.

## Workflow (3 Steps)

### Phase 1: Autonomous Law Search Agent
```python
from agents.autonomous_agents import autonomous_law_search_agent
```

**Nhiệm vụ:**
- Tìm văn bản luật trên duthaoonline
- AI đánh giá và chọn document tốt nhất
- Download PDF tự động

**TaskType:** `AUTONOMOUS_LAW_SEARCH`

### Phase 2: Autonomous PDF Analysis Agent
```python
from agents.autonomous_agents import autonomous_pdf_analysis_agent
```

**Nhiệm vụ:**
- Extract nội dung từ PDF
- AI extract keywords quan trọng (10-15 keywords)
- Chuẩn bị keywords cho opinion search

**TaskType:** `AUTONOMOUS_PDF_ANALYSIS`

### Phase 3: Autonomous Opinion Search Agent
```python
from agents.autonomous_agents import autonomous_opinion_search_agent
```

**Nhiệm vụ:**
- AI sinh 5 search queries đa dạng
- Search DuckDuckGo tự động với Selenium
- AI đánh giá từng kết quả (relevant hay không)
- Crawl nội dung từ URLs relevant
- AI đánh giá chất lượng nội dung (0-10)
- Phân tích sentiment và stance tự động
- Export CSV

**TaskType:** `AUTONOMOUS_OPINION_SEARCH`

## Sử dụng

### Basic

```bash
python main.py
```

### Programmatic

```python
import asyncio
from core.workflow import run_autonomous_workflow

async def main():
    result = await run_autonomous_workflow(
        project_name="Luật Trí tuệ nhân tạo 2025",
        max_opinions=20,
        quality_threshold=0.6
    )
    
    print(f"PDF: {result['pdf_local_path']}")
    print(f"Keywords: {result['search_queries']}")
    print(f"Opinions: {len(result['analyzed_opinions'])}")
    print(f"CSV: {result['csv_output_path']}")

asyncio.run(main())
```

## Configuration

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| project_name | str | required | Tên dự luật/chủ đề |
| max_opinions | int | 20 | Số opinions tối đa |
| quality_threshold | float | 0.6 | Ngưỡng chất lượng (0-1) |

### Example

```python
result = await run_autonomous_workflow(
    project_name="Luật Trí tuệ nhân tạo 2025",
    max_opinions=50,  # Thu thập nhiều hơn
    quality_threshold=0.8  # Chất lượng cao hơn
)
```

## State Management

### AgentState

```python
from core.types import AgentState

state = {
    # Input
    'project_name': str,
    'max_opinions': int,
    'quality_threshold': float,
    
    # Tracking
    'current_task': Task,
    'task_history': List[Task],
    
    # Phase 1 results
    'law_documents': List[Dict],
    'pdf_local_path': str,
    
    # Phase 2 results
    'search_queries': List[str],  # Keywords
    
    # Phase 3 results
    'analyzed_opinions': List[Dict],
    
    # Output
    'csv_output_path': str,
    
    # Error handling
    'errors': List[Dict],
    'warnings': List[str],
    
    # Metadata
    'started_at': datetime,
    'last_updated': datetime,
    'is_complete': bool
}
```

## Manager Orchestration

Manager Agent điều phối workflow:

```python
# Step 1
AUTONOMOUS_LAW_SEARCH → AUTONOMOUS_PDF_ANALYSIS

# Step 2
AUTONOMOUS_PDF_ANALYSIS → AUTONOMOUS_OPINION_SEARCH

# Step 3
AUTONOMOUS_OPINION_SEARCH → Complete
```

## Output Format

### CSV Columns

```
title, url, source, quality_score, sentiment, stance, 
stance_confidence, support_score, oppose_score, relevance,
quality_feedback, key_points, search_query, content_preview
```

### Example Row

```csv
"Chuyên gia đánh giá cao Luật AI",
"https://example.com/article",
"example.com",
0.85,
"positive",
"support",
0.92,
8,
2,
"high",
"Bài viết có phân tích chuyên sâu",
"AI sẽ thay đổi tương lai; Quy định rõ ràng",
"Luật Trí tuệ nhân tạo ý kiến chuyên gia",
"Chuyên gia cho rằng dự luật có nhiều điểm tích cực..."
```

## AI Capabilities

### 1. Document Selection
AI đánh giá documents dựa trên:
- Độ chính xác với topic
- Tính chính thức của văn bản
- Mức độ liên quan

### 2. Keyword Extraction
AI extract keywords dựa trên:
- Khái niệm chính trong văn bản
- Quyền lợi và nghĩa vụ
- Quy định quan trọng

### 3. Search Query Generation
AI tạo queries đa dạng:
- Góc nhìn khác nhau
- Tập trung vào ý kiến chuyên gia
- Tự nhiên như người Việt search

### 4. Relevance Assessment
AI đánh giá mỗi kết quả search:
- Có chứa ý kiến không?
- Có phân tích chuyên sâu không?
- Có liên quan trực tiếp không?

### 5. Quality Evaluation
AI đánh giá chất lượng content:
- Relevance score (0-10)
- Depth score (0-10)
- Credibility score (0-10)
- Overall score (0-10)

## Search Engine

Sử dụng **DuckDuckGo** để tránh bot detection:
- Không cần CAPTCHA
- Kết quả ổn định
- Bảo mật và riêng tư

## Error Handling

### Graceful Degradation

- Nếu không tìm thấy PDF: Dùng topic làm keywords
- Nếu không extract được PDF: Dùng topic split
- Nếu search thất bại: Retry với query khác
- Nếu crawl thất bại: Skip URL đó

### Error Tracking

```python
errors = final_state.get('errors', [])
for error in errors:
    print(f"{error['agent']}: {error['message']}")
```

## Performance

### Typical Runtime

- **Phase 1**: 30-60 giây (tìm và download PDF)
- **Phase 2**: 10-20 giây (extract và keywords)
- **Phase 3**: 10-15 phút (search và crawl 20 opinions)

**Total**: ~15-20 phút cho 20 opinions

### Optimization Tips

1. **Giảm max_opinions**: Thu thập ít hơn = nhanh hơn
2. **Tăng quality_threshold**: Chọn lọc kỹ hơn = ít crawl hơn
3. **Parallel processing**: Sẽ được implement trong tương lai

## Troubleshooting

### PDF không download được
- Kiểm tra kết nối internet
- Thử lại với topic khác
- Workflow vẫn chạy với keywords từ topic

### DuckDuckGo không có kết quả
- Đợi vài phút và thử lại
- Kiểm tra kết nối internet
- Thử với search query đơn giản hơn

### Opinions chất lượng thấp
- Tăng `quality_threshold` lên 0.7-0.8
- Tăng `max_opinions` để có nhiều lựa chọn hơn
- Refine topic để specific hơn

### Ollama chậm
- Sử dụng model nhỏ hơn (llama3.2:1b)
- Tăng RAM cho Ollama
- Chạy trên máy có GPU

## Advanced Usage

### Custom Agent Behavior

Modify agents trong `agents/autonomous_agents.py`:

```python
class AutonomousLawSearchAgent(BaseAgent):
    async def execute(self, state: AgentState) -> AgentState:
        # Your custom logic here
        pass
```

### Custom Workflow

Modify workflow trong `core/workflow.py`:

```python
def create_workflow() -> StateGraph:
    workflow = StateGraph(AgentState)
    # Add your custom nodes/edges
    return workflow
```

### Custom Manager Logic

Modify orchestration trong `agents/manager.py`:

```python
async def _monitor_and_decide(self, state: AgentState) -> AgentState:
    # Your custom routing logic
    pass
```

## Best Practices

1. **Topic Selection**: Chọn topic cụ thể và rõ ràng
2. **Quality First**: Ưu tiên chất lượng hơn số lượng
3. **Monitor Logs**: Theo dõi logs để debug
4. **Validate Output**: Kiểm tra CSV output
5. **Iterative Refinement**: Chạy nhiều lần với configs khác nhau

## Future Enhancements

- [ ] Parallel opinion crawling
- [ ] Caching for repeated searches
- [ ] Multi-LLM support
- [ ] Web UI for monitoring
- [ ] Checkpoint/resume functionality
- [ ] Advanced NLP analysis
- [ ] Multi-language support

---

For more information, see main `README.md`
