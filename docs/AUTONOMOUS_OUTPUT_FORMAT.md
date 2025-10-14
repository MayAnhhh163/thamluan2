# 📊 Autonomous Search - Output Format

## CSV Export Format

Sau khi autonomous search hoàn tất, kết quả sẽ được tự động xuất ra file CSV với format đầy đủ:

### File Location

```
data/csv/autonomous_<topic>_<timestamp>.csv
```

Ví dụ:
```
data/csv/autonomous_Luật_trí_tuệ_nhân_tạo_20251014_203045.csv
```

### CSV Columns

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| **title** | string | Tiêu đề bài viết | "Chuyên gia: Luật AI cần rõ ràng hơn" |
| **url** | string | URL gốc | "https://vnexpress.net/..." |
| **source** | string | Nguồn (domain) | "vnexpress.net" |
| **quality_score** | float | Điểm chất lượng (0-1) | "0.87" |
| **sentiment** | string | Cảm xúc | "positive" / "negative" / "neutral" |
| **stance** | string | Lập trường | "support" / "oppose" / "neutral" |
| **stance_confidence** | float | Độ tin cậy lập trường (0-1) | "0.85" |
| **support_score** | int | Số từ khóa ủng hộ | 8 |
| **oppose_score** | int | Số từ khóa phản đối | 2 |
| **relevance** | string | Độ liên quan | "high" / "medium" / "low" |
| **quality_feedback** | string | Nhận xét chất lượng | "Phân tích sâu, có dẫn chứng" |
| **key_points** | string | Điểm chính (cách nhau bởi ;) | "Điểm A; Điểm B; Điểm C" |
| **search_query** | string | Query đã dùng | "Luật AI ý kiến chuyên gia" |
| **content_preview** | string | Preview nội dung (500 chars) | "Theo chuyên gia..." |

## Console Output

### Real-time Progress

```
🔍 Query 1/5: 'Luật AI ý kiến chuyên gia'
Found 10 search results

  [1] Evaluating: Chuyên gia: Luật AI cần rõ ràng hơn...
      ✅ Ollama says: Relevant! Crawling...
      📄 Crawled 2847 chars
      ⭐ Quality: 0.87 - Phân tích sâu với dẫn chứng cụ thể
      🧠 Analyzing sentiment & stance...
      📊 Sentiment: positive
      📊 Stance: support (confidence: 0.85)
      💾 Saved! Total: 1/20
```

### Final Summary

```
================================================================================
📊 AUTONOMOUS SEARCH COMPLETE
================================================================================
✅ Collected: 20 high-quality opinions
🔍 Visited: 45 URLs
📝 Used: 5 search queries
⭐ Average quality: 0.82

📰 Sources: {'vnexpress.net': 8, 'dantri.com.vn': 5, 'tuoitre.vn': 4, ...}
😊 Sentiments: {'positive': 12, 'neutral': 5, 'negative': 3}
📊 Stances: {'support': 14, 'neutral': 4, 'oppose': 2}

💾 Exported to: data/csv/autonomous_Luật_AI_20251014_203045.csv
```

## Python API Response

```python
result = ollama_autonomous_search_agent.autonomous_search_and_crawl(...)

if result.success:
    data = result.data
    
    # List of opinions with full analysis
    opinions = data['opinions']
    # [
    #   {
    #     'title': '...',
    #     'url': '...',
    #     'content': '...',
    #     'quality_score': 0.87,
    #     'sentiment': 'positive',
    #     'stance': 'support',
    #     'stance_confidence': 0.85,
    #     'support_score': 8,
    #     'oppose_score': 2,
    #     'key_points': [...],
    #     ...
    #   },
    #   ...
    # ]
    
    # Statistics
    count = data['count']                    # 20
    avg_quality = data['average_quality']    # 0.82
    sources = data['sources']                # {'vnexpress.net': 8, ...}
    sentiments = data['sentiments']          # {'positive': 12, ...}
    stances = data['stances']                # {'support': 14, ...}
    csv_path = data['csv_path']              # 'data/csv/...'
```

## Sentiment Values

| Value | Meaning | Vietnamese |
|-------|---------|------------|
| **positive** | Tích cực | Ủng hộ, đánh giá tốt |
| **negative** | Tiêu cực | Phản đối, đánh giá xấu |
| **neutral** | Trung lập | Không thiên về bên nào |
| **mixed** | Lẫn lộn | Vừa tích cực vừa tiêu cực |

## Stance Values

| Value | Meaning | Vietnamese |
|-------|---------|------------|
| **support** | Ủng hộ | Đồng ý, tán thành |
| **oppose** | Phản đối | Không đồng ý, chống lại |
| **neutral** | Trung lập | Không ủng hộ cũng không phản đối |

## Quality Score

- **0.9 - 1.0**: Excellent (Xuất sắc)
  - Phân tích rất sâu
  - Nhiều dẫn chứng cụ thể
  - Từ nguồn uy tín

- **0.7 - 0.89**: Good (Tốt)
  - Phân tích tốt
  - Có dẫn chứng
  - Nguồn đáng tin

- **0.5 - 0.69**: Acceptable (Chấp nhận được)
  - Phân tích cơ bản
  - Ít dẫn chứng
  - Nguồn bình thường

- **< 0.5**: Poor (Kém)
  - Nội dung nông cạn
  - Không có dẫn chứng
  - Nguồn không rõ ràng

## Example CSV Row

```csv
title,url,source,quality_score,sentiment,stance,stance_confidence,support_score,oppose_score,relevance,quality_feedback,key_points,search_query,content_preview
"Chuyên gia: Luật AI cần rõ ràng hơn","https://vnexpress.net/...","vnexpress.net","0.87","positive","support","0.85","8","2","high","Phân tích sâu với dẫn chứng cụ thể","Cần quy định rõ trách nhiệm AI; Bảo vệ dữ liệu cá nhân; Khuyến khích đổi mới","Luật AI ý kiến chuyên gia","Theo chuyên gia An ninh mạng, Luật AI cần có những quy định rõ ràng về trách nhiệm của nhà phát triển AI..."
```

## Processing Results

### Load CSV in Python

```python
import pandas as pd

df = pd.read_csv('data/csv/autonomous_Luật_AI_20251014_203045.csv')

# Filter by sentiment
positive_opinions = df[df['sentiment'] == 'positive']
negative_opinions = df[df['sentiment'] == 'negative']

# Filter by stance
support_opinions = df[df['stance'] == 'support']
oppose_opinions = df[df['stance'] == 'oppose']

# Filter by quality
high_quality = df[df['quality_score'] >= 0.8]

# Statistics
print(f"Total opinions: {len(df)}")
print(f"Positive: {len(positive_opinions)}")
print(f"Support: {len(support_opinions)}")
print(f"Average quality: {df['quality_score'].mean():.2f}")
```

### Load CSV in Excel

1. Open Excel
2. Data → From Text/CSV
3. Select file: `autonomous_Luật_AI_20251014_203045.csv`
4. Encoding: UTF-8
5. Import

**Pivot Table Example:**
- Rows: sentiment
- Columns: stance
- Values: count

## Integration with Workflow

Khi sử dụng trong main workflow:

```python
from agents.autonomous_opinion_agent import autonomous_opinion_agent

state['current_task'] = Task(
    task_type=TaskType.AUTONOMOUS_OPINION_SEARCH,
    input_data={
        'max_articles': 20,
        'quality_threshold': 0.7
    }
)

state = await autonomous_opinion_agent.execute(state)

# Get results
opinions = state['opinions_raw']
stats = state['autonomous_search_stats']

print(f"Sentiments: {stats.get('sentiments', {})}")
print(f"Stances: {stats.get('stances', {})}")
print(f"CSV: {stats.get('csv_path')}")
```

## Visualization Ideas

### 1. Sentiment Distribution Pie Chart

```python
import matplotlib.pyplot as plt

sentiments = {'positive': 12, 'neutral': 5, 'negative': 3}
plt.pie(sentiments.values(), labels=sentiments.keys(), autopct='%1.1f%%')
plt.title('Sentiment Distribution')
plt.show()
```

### 2. Quality vs Sentiment Scatter

```python
import seaborn as sns

sns.scatterplot(data=df, x='quality_score', y='stance_confidence', 
                hue='sentiment', size='support_score')
plt.title('Quality vs Stance by Sentiment')
plt.show()
```

### 3. Source Distribution Bar Chart

```python
sources = df['source'].value_counts()
sources.plot(kind='bar')
plt.title('Opinions by Source')
plt.xlabel('Source')
plt.ylabel('Count')
plt.show()
```

## Summary Report Template

```
================================================================================
AUTONOMOUS SEARCH REPORT
================================================================================

Topic: Luật Trí tuệ nhân tạo
Date: 2025-10-14 20:30:45
Duration: 8 minutes

COLLECTION STATS
----------------
✅ Opinions collected: 20
🔍 URLs visited: 45
⭐ Average quality: 0.82
📝 Search queries used: 5

SENTIMENT ANALYSIS
------------------
😊 Positive: 12 (60%)
😐 Neutral: 5 (25%)
😞 Negative: 3 (15%)

STANCE ANALYSIS
---------------
✅ Support: 14 (70%)
⚖️ Neutral: 4 (20%)
❌ Oppose: 2 (10%)

TOP SOURCES
-----------
1. vnexpress.net: 8 articles
2. dantri.com.vn: 5 articles
3. tuoitre.vn: 4 articles
4. Others: 3 articles

QUALITY DISTRIBUTION
--------------------
Excellent (0.9-1.0): 5 opinions
Good (0.7-0.89): 12 opinions
Acceptable (0.5-0.69): 3 opinions

KEY FINDINGS
------------
Main themes:
- Cần quy định rõ trách nhiệm AI
- Bảo vệ dữ liệu cá nhân là ưu tiên
- Khuyến khích đổi mới sáng tạo
- Minh bạch trong thuật toán AI
- Giám sát và kiểm soát AI

EXPORT
------
CSV file: data/csv/autonomous_Luật_AI_20251014_203045.csv
Columns: 14
Encoding: UTF-8 with BOM (Excel compatible)

================================================================================
```

## Kết luận

Autonomous search giờ đã xuất ra:
- ✅ File CSV đầy đủ thông tin
- ✅ Sentiment analysis (tích cực/tiêu cực/trung lập)
- ✅ Stance detection (ủng hộ/phản đối/trung lập)
- ✅ Quality scores và feedback
- ✅ Key points từ mỗi opinion
- ✅ Statistics tổng hợp

Mở file CSV trong Excel để xem và phân tích! 📊
