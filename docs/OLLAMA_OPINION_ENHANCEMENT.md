# Ollama Opinion Enhancement

## Tổng quan

Hệ thống AutoData đã tích hợp **Ollama LLM** để nâng cao chất lượng thu thập và phân tích opinions. Module `OllamaOpinionEnhancer` cung cấp các tính năng AI thông minh để cải thiện workflow.

## Tính năng

### 1. 🔍 Smart Search Query Generation
Sử dụng Ollama để tạo các search queries thông minh hơn từ keywords:

```python
from tools.ollama_opinion_enhancer import ollama_opinion_enhancer

result = ollama_opinion_enhancer.generate_smart_search_queries(
    topic="Luật Trí tuệ nhân tạo",
    keywords=["AI", "công nghệ", "quy định", "bảo mật"],
    num_queries=10
)

queries = result.data['queries']
# ['Luật AI ý kiến chuyên gia', 'trí tuệ nhân tạo phản hồi doanh nghiệp', ...]
```

**Lợi ích:**
- Queries đa dạng hơn (vừa chung, vừa cụ thể)
- Tự nhiên như cách người Việt tìm kiếm
- Tập trung vào opinions chất lượng cao

### 2. ⭐ Opinion Quality Evaluation
Đánh giá chất lượng của từng opinion theo nhiều tiêu chí:

```python
result = ollama_opinion_enhancer.evaluate_opinion_quality(
    opinion={
        'title': 'Chuyên gia nhận định về Luật AI',
        'content': 'Nội dung chi tiết...',
        'url': 'https://...'
    },
    topic="Luật Trí tuệ nhân tạo"
)

quality_data = result.data
# {
#     'quality_score': 0.85,
#     'is_valuable': True,
#     'relevance': 'high',
#     'feedback': 'Phân tích sâu với dẫn chứng cụ thể',
#     'key_points': ['Điểm A', 'Điểm B', ...]
# }
```

**Các tiêu chí đánh giá:**
- **Relevance**: Độ liên quan đến chủ đề (0-10)
- **Depth**: Độ sâu phân tích (0-10)
- **Originality**: Tính độc đáo (0-10)
- **Credibility**: Độ tin cậy (0-10)
- **Value**: Giá trị thông tin (0-10)

### 3. 💡 Insights Extraction
Trích xuất insights tổng hợp từ nhiều opinions:

```python
result = ollama_opinion_enhancer.extract_insights(
    opinions=analyzed_opinions,
    topic="Luật Trí tuệ nhân tạo",
    max_opinions=20
)

insights = result.data
# {
#     'main_themes': ['Bảo mật dữ liệu', 'Quyền sở hữu', ...],
#     'supporting_views': [...],
#     'opposing_views': [...],
#     'concerns': ['Mối quan ngại A', ...],
#     'recommendations': ['Đề xuất X', ...],
#     'sentiment_distribution': {'positive': 45, 'negative': 20, 'neutral': 35},
#     'overall_summary': 'Tóm tắt dư luận...'
# }
```

**Lợi ích:**
- Hiểu tổng quan dư luận
- Phát hiện chủ đề chính
- Nhận diện xu hướng ủng hộ/phản đối

### 4. 🏷️ Opinion Categorization
Tự động phân loại opinions theo nguồn:

```python
result = ollama_opinion_enhancer.categorize_opinions(
    opinions=opinions_list,
    categories=[
        "Chuyên gia pháp lý",
        "Doanh nghiệp/Hiệp hội",
        "Người dân",
        "Cơ quan nhà nước",
        "Học giả/Nghiên cứu"
    ]
)

categorized = result.data['categorized']
summary = result.data['summary']
# {'Chuyên gia pháp lý': 15, 'Doanh nghiệp': 8, ...}
```

### 5. 🔄 Duplicate Detection
Phát hiện opinions trùng lặp hoặc tương tự:

```python
result = ollama_opinion_enhancer.detect_duplicate_opinions(
    opinions=opinions_list,
    similarity_threshold=0.8
)

unique = result.data['unique_opinions']
duplicates = result.data['duplicates']
```

## Cấu hình

### 1. Cài đặt Ollama

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull model
ollama pull llama3.1:8b

# Start Ollama server
ollama serve
```

### 2. Cấu hình môi trường

Tạo file `.env` hoặc export biến môi trường:

```bash
# Ollama settings
OLLAMA_BASE_URL=http://localhost:11434
LLM_MODEL=llama3.1:8b

# Enable/Disable Ollama enhancement
OLLAMA_ENABLE_OPINION_ENHANCEMENT=true
```

### 3. Kiểm tra kết nối

```python
from core.config import config

# Check Ollama connection
issues = config.validate_config()
if issues:
    print("Issues:", issues)
else:
    print("✅ Ollama connected successfully!")
```

## Tích hợp vào Workflow

Module đã được tích hợp tự động vào HYBRID WORKFLOW:

### Trong Opinion Search Phase:
```python
# agents/hybrid_agents.py - EnhancedOpinionSearchAgent
if config.OLLAMA_ENABLE_OPINION_ENHANCEMENT:
    # Sử dụng Ollama để sinh search queries thông minh
    query_result = ollama_opinion_enhancer.generate_smart_search_queries(
        topic=project_name,
        keywords=keywords_list,
        num_queries=10
    )
```

### Trong NLP Analysis Phase:
```python
# agents/hybrid_agents.py - NLPAnalysisAgent
if config.OLLAMA_ENABLE_OPINION_ENHANCEMENT and len(analyzed_opinions) >= 5:
    # Extract insights từ tất cả opinions
    insights_result = ollama_opinion_enhancer.extract_insights(
        opinions=analyzed_opinions,
        topic=topic,
        max_opinions=20
    )
```

## So sánh với Phương pháp Truyền thống

| Feature | Traditional | Ollama Enhanced |
|---------|------------|----------------|
| Search Queries | Template-based | AI-generated, context-aware |
| Quality Filter | Keyword matching | Multi-criteria AI evaluation |
| Insights | Statistical summary | Thematic analysis + Summary |
| Categorization | Rule-based | Contextual understanding |
| Language Support | Limited | Natural Vietnamese |

## Performance

### Model đề xuất:

- **llama3.1:8b** (4.7GB): Cân bằng tốt giữa tốc độ và chất lượng
- **llama3.2:3b** (2GB): Nhanh hơn nhưng chất lượng thấp hơn
- **qwen2.5:7b** (4.7GB): Tốt với tiếng Việt

### Thời gian xử lý (ước tính):

- Generate 10 queries: ~5-10 giây
- Evaluate 1 opinion: ~3-5 giây
- Extract insights (20 opinions): ~15-30 giây
- Categorize 50 opinions: ~2-5 phút

## Best Practices

### 1. Khi nào nên dùng Ollama Enhancement?

**✅ Nên dùng:**
- Chủ đề phức tạp cần search queries đa dạng
- Cần lọc opinions chất lượng cao
- Muốn insights tổng hợp từ nhiều nguồn
- Phân tích dư luận toàn diện

**❌ Không cần:**
- Chỉ cần crawl nhanh
- Đã có search queries cụ thể
- Chủ đề đơn giản
- Server không đủ mạnh

### 2. Optimize Performance

```python
# Giới hạn số lượng opinions để phân tích
MAX_OPINIONS_FOR_INSIGHTS = 20

# Sử dụng batching cho large dataset
opinions_batches = [opinions[i:i+20] for i in range(0, len(opinions), 20)]
for batch in opinions_batches:
    result = ollama_opinion_enhancer.extract_insights(batch, topic)
```

### 3. Error Handling

Module có fallback tự động:
- Nếu Ollama không khả dụng → dùng phương pháp truyền thống
- Nếu LLM response không valid → trả về kết quả neutral
- Tất cả errors đều được log nhưng không crash workflow

## Troubleshooting

### Lỗi: "Cannot connect to Ollama"
```bash
# Check Ollama status
systemctl status ollama  # Linux
# hoặc
ollama list  # Check if running

# Restart Ollama
ollama serve
```

### Lỗi: "Model not found"
```bash
# Pull model
ollama pull llama3.1:8b

# List installed models
ollama list
```

### Response quá chậm
```python
# Giảm num_predict trong config
# tools/ollama_opinion_enhancer.py
self.llm = ChatOllama(
    model=config.LLM_MODEL,
    num_predict=512,  # Giảm từ 2048
    temperature=0.7
)
```

## Ví dụ Workflow Hoàn chỉnh

```python
from tools.ollama_opinion_enhancer import ollama_opinion_enhancer

# 1. Generate search queries
queries_result = ollama_opinion_enhancer.generate_smart_search_queries(
    topic="Luật Trí tuệ nhân tạo",
    keywords=["AI", "công nghệ", "dữ liệu"],
    num_queries=10
)

# 2. Crawl opinions (using generated queries)
opinions = crawl_opinions_from_queries(queries_result.data['queries'])

# 3. Evaluate each opinion
valuable_opinions = []
for op in opinions:
    eval_result = ollama_opinion_enhancer.evaluate_opinion_quality(op, topic)
    if eval_result.data['quality_score'] > 0.6:
        valuable_opinions.append(op)

# 4. Detect and remove duplicates
dedup_result = ollama_opinion_enhancer.detect_duplicate_opinions(valuable_opinions)
unique_opinions = dedup_result.data['unique_opinions']

# 5. Extract insights
insights_result = ollama_opinion_enhancer.extract_insights(
    unique_opinions, 
    topic="Luật Trí tuệ nhân tạo"
)

# 6. Categorize opinions
cat_result = ollama_opinion_enhancer.categorize_opinions(unique_opinions)

print(f"✅ Processed {len(opinions)} → {len(unique_opinions)} unique valuable opinions")
print(f"📊 Insights: {insights_result.data['overall_summary']}")
```

## Kết luận

Ollama Opinion Enhancement mang lại giá trị lớn cho việc thu thập và phân tích opinions:

✅ **Search thông minh hơn** - Tìm được opinions chất lượng cao  
✅ **Lọc tự động** - Loại bỏ noise, giữ lại nội dung có giá trị  
✅ **Insights sâu sắc** - Hiểu rõ dư luận và xu hướng  
✅ **Tự động hóa** - Giảm công sức xử lý thủ công  
✅ **Language-aware** - Hiểu tiếng Việt tự nhiên  

Tuy nhiên cần cân nhắc:
- Yêu cầu cài đặt Ollama (4-8GB RAM)
- Thời gian xử lý lâu hơn
- Cần fine-tune cho từng use case
