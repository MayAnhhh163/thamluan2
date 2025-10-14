# 🤖 Full AI Autonomous Workflow

## Giới thiệu

**Full Autonomous Workflow** = AI điều khiển **TỒN BỘ** từ đầu đến cuối!

Chỉ cần nhập topic, AI sẽ tự động:

1. 🔍 **Tìm PDF văn bản luật** chính thức
2. 📥 **Download PDF** tốt nhất
3. 📄 **Extract nội dung** PDF
4. 🧠 **Extract keywords** quan trọng
5. 🤖 **Autonomous search** opinions
6. 📊 **Phân tích** sentiment & stance
7. 💾 **Export CSV** đầy đủ

## Sử dụng (Cực kỳ đơn giản!)

### Cách 1: Script đơn giản nhất

```bash
python main_autonomous.py
```

**Nhập topic và Enter:**
```
📋 Nhập chủ đề/tên dự luật:
→ Luật Trí tuệ nhân tạo

⚙️  Configuration:
   Số opinions tối đa [20]: 
   Quality threshold (0-1) [0.6]: 

🚀 STARTING...
```

**Chờ 10-15 phút, AI làm TỒN BỘ!**

### Cách 2: Python Code

```python
from tools.ollama_full_autonomous_workflow import ollama_full_autonomous_workflow

result = ollama_full_autonomous_workflow.run_full_workflow(
    topic="Luật Trí tuệ nhân tạo",
    max_opinions=20,
    quality_threshold=0.6
)

if result.success:
    data = result.data
    
    print(f"Law docs: {len(data['law_documents'])}")
    print(f"PDF: {data['pdf_downloaded']}")
    print(f"Keywords: {data['keywords']}")
    print(f"Opinions: {len(data['opinions'])}")
    print(f"Sentiments: {data['sentiments']}")
    print(f"CSV: {data['csv_path']}")
```

### Cách 3: Test Full Workflow

```bash
python tools/test_full_workflow.py
```

## Workflow Chi tiết

### Phase 1: AI tìm PDF văn bản luật

```
📋 PHASE 1: AI TÌM VĂN BẢN LUẬT
================================

🔍 Searching: 'Luật Trí tuệ nhân tạo'
✅ Found 7 documents

AI đánh giá document nào tốt nhất...
✅ AI selected: Luật Trí tuệ nhân tạo

📥 Downloading PDF...
✅ PDF downloaded: data/pdfs/cfbc89c1df09676e.pdf
```

**AI làm gì?**
- Tìm trên duthaoonline.quochoi.vn
- So sánh nhiều documents
- Chọn document CHÍNH XÁC nhất
- Download PDF

### Phase 2: AI extract & phân tích PDF

```
📄 PHASE 2: AI EXTRACT PDF
===========================

📄 Extracting PDF...
✅ Extracted 45,234 characters

🧠 AI extracting keywords...
✅ AI extracted 12 keywords:
   trí tuệ nhân tạo, AI, công nghệ, dữ liệu, 
   quyền sở hữu, bảo mật, đổi mới, quy định...
```

**AI làm gì?**
- Extract toàn bộ text từ PDF
- Đọc và hiểu nội dung
- Extract keywords QUAN TRỌNG nhất
- Chuẩn bị cho phase 3

### Phase 3: AI autonomous search opinions

```
🔍 PHASE 3: AUTONOMOUS SEARCH
==============================

Using keywords: trí tuệ nhân tạo, AI, công nghệ...

🔍 Query 1/5: 'Luật AI trí tuệ nhân tạo ý kiến chuyên gia'

  [1] Evaluating: Chuyên gia: Luật AI cần rõ...
      ✅ Relevant! Crawling...
      ⭐ Quality: 0.87
      📊 Sentiment: positive
      📊 Stance: support
      💾 Saved! (1/20)

...

✅ Collected: 20 opinions
😊 Sentiments: {positive: 12, neutral: 5, negative: 3}
📊 Stances: {support: 14, neutral: 4, oppose: 2}
💾 Exported: data/csv/autonomous_Luật_AI_20251014_203045.csv
```

**AI làm gì?**
- Sinh search queries từ keywords
- Autonomous search & crawl
- Phân tích sentiment & stance
- Export CSV đầy đủ

## Output

### Console Summary

```
================================================================================
📊 FULL WORKFLOW COMPLETE
================================================================================

📋 PHASE 1 - Văn bản luật:
   Documents found: 7
   PDF downloaded: Yes

📄 PHASE 2 - PDF Analysis:
   Keywords extracted: 12
   Keywords: trí tuệ nhân tạo, AI, công nghệ, dữ liệu, quyền sở hữu...

🔍 PHASE 3 - Opinion Mining:
   Opinions collected: 20
   Sentiments: {positive: 12, neutral: 5, negative: 3}
   Stances: {support: 14, neutral: 4, oppose: 2}

💾 Results exported to:
   data/csv/autonomous_Luật_AI_20251014_203045.csv

✅ FULL AI WORKFLOW COMPLETED SUCCESSFULLY!
```

### CSV File

Chứa TỒN BỘ thông tin:
- PDF analysis results
- Opinion details
- Sentiment & stance
- Quality scores
- Key points
- Full content preview

## Requirements

```bash
# 1. Ollama
ollama serve
ollama pull llama3.1:8b

# 2. Python packages
pip install undetected-chromedriver selenium beautifulsoup4 langchain-ollama

# 3. Chrome browser
# Download from google.com/chrome
```

## So sánh với Manual Workflow

| Step | Manual | Full Autonomous |
|------|--------|-----------------|
| **Tìm PDF luật** | Bạn phải search | ✅ AI tự động |
| **Chọn PDF đúng** | Bạn phải đọc | ✅ AI đánh giá |
| **Download PDF** | Manual click | ✅ AI tự động |
| **Extract PDF** | Dùng tool | ✅ AI tự động |
| **Extract keywords** | Manual đọc | ✅ AI tự động |
| **Sinh search queries** | Bạn nghĩ | ✅ AI sinh |
| **Search opinions** | Manual search | ✅ AI autonomous |
| **Crawl content** | Manual copy | ✅ AI tự động |
| **Đánh giá chất lượng** | Manual đọc | ✅ AI đánh giá |
| **Phân tích sentiment** | Manual | ✅ AI phân tích |
| **Export results** | Manual format | ✅ AI export |
| **Time** | 2-3 giờ | 10-15 phút |

## Advanced Usage

### Custom Configuration

```python
result = ollama_full_autonomous_workflow.run_full_workflow(
    topic="Luật Trí tuệ nhân tạo",
    
    # Số opinions muốn thu thập
    max_opinions=30,
    
    # Ngưỡng chất lượng (càng cao càng khó)
    quality_threshold=0.8  # Very high quality only
)
```

### Access All Data

```python
data = result.data

# Phase 1 results
law_docs = data['law_documents']
pdf_path = data['pdf_downloaded']

# Phase 2 results
keywords = data['keywords']
pdf_content = data.get('pdf_content', '')

# Phase 3 results
opinions = data['opinions']
sentiments = data['sentiments']
stances = data['stances']
csv_path = data['csv_path']
```

### Process Results

```python
import pandas as pd

# Load CSV
df = pd.read_csv(data['csv_path'])

# Analyze by sentiment
positive = df[df['sentiment'] == 'positive']
negative = df[df['sentiment'] == 'negative']

# Analyze by stance
support = df[df['stance'] == 'support']
oppose = df[df['stance'] == 'oppose']

# High quality support opinions
high_support = df[(df['stance'] == 'support') & 
                  (df['quality_score'] >= 0.8)]
```

## Troubleshooting

### Lỗi: "No law documents found"

```
Có thể do:
1. Tên dự luật không chính xác
2. Chưa có trên duthaoonline.quochoi.vn
3. Similarity threshold quá cao

Giải pháp:
- Thử tên khác: "Luật AI" thay vì "Luật Trí tuệ nhân tạo"
- Workflow vẫn chạy tiếp (dùng topic làm keywords)
```

### Lỗi: "PDF download failed"

```
Có thể do:
1. PDF link hỏng
2. SSL certificate error
3. Network issue

Giải pháp:
- Đã có fix SSL (verify=False)
- Workflow vẫn chạy tiếp với keywords từ topic
```

### Lỗi: "Google bot detection"

```
Giải pháp:
- Install: pip install undetected-chromedriver
- System tự động fallback sang DuckDuckGo
```

## Performance

| Phase | Time | Notes |
|-------|------|-------|
| Phase 1: PDF Search | 30-60s | Tìm + download PDF |
| Phase 2: PDF Extract | 10-30s | Extract + AI keywords |
| Phase 3: Opinion Search | 8-12 min | Autonomous search + analysis |
| **Total** | **10-15 min** | Full workflow |

## Examples

### Example 1: Luật Trí tuệ nhân tạo

```bash
python main_autonomous.py
→ Luật Trí tuệ nhân tạo

Results:
- 1 PDF downloaded
- 12 keywords extracted
- 20 opinions collected
- 12 positive, 3 negative
- 14 support, 2 oppose
```

### Example 2: Luật Đất đai

```bash
python main_autonomous.py
→ Luật Đất đai

Results:
- 3 PDFs found (AI chọn tốt nhất)
- 15 keywords extracted
- 25 opinions collected
- CSV exported
```

## Best Practices

### 1. Topic Naming

```python
✅ Good:
- "Luật Trí tuệ nhân tạo"
- "Luật Đất đai"
- "Luật Giao thông đường bộ"

⚠️ OK but less accurate:
- "Luật AI"
- "Đất đai"
- "Giao thông"
```

### 2. Quality Threshold

```python
# For broad coverage
quality_threshold=0.5

# Balanced (recommended)
quality_threshold=0.6

# High quality only
quality_threshold=0.8
```

### 3. Max Opinions

```python
# Quick test
max_opinions=10  # ~5 minutes

# Standard
max_opinions=20  # ~10 minutes

# Comprehensive
max_opinions=50  # ~25 minutes
```

## Summary

**Full AI Autonomous Workflow** = Tự động TỒN BỘ từ A đến Z!

```
Input:  "Luật Trí tuệ nhân tạo"
          ↓
AI tìm PDF → AI extract → AI search → AI analyze → CSV
          ↓
Output: Full analysis report + CSV
```

**1 lệnh, 10 phút, TỒN BỘ xong!**

```bash
python main_autonomous.py
```

Enjoy! 🎉
