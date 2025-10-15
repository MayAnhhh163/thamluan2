# 🤖 Autonomous AI Agent System - LangGraph

Hệ thống AI Agent tự động thu thập và phân tích ý kiến về dự luật, được xây dựng trên framework LangGraph.

## 📋 Tổng quan

**Autonomous AI Agent** là một workflow hoàn toàn tự động, chỉ cần nhập tên dự luật, AI sẽ tự động:

1. 🔍 **Tìm văn bản luật** - AI tìm và download PDF chính thức
2. 📄 **Phân tích PDF** - AI extract keywords quan trọng
3. 💬 **Thu thập ý kiến** - AI search, crawl và phân tích opinions

## 🏗️ Kiến trúc LangGraph

```
┌────────────────────────────────────┐
│        MANAGER AGENT                │
│     (Orchestrator)                  │
└──────────┬─────────────────────────┘
           │
           ▼
┌────────────────────────────────────┐
│  Phase 1: Law Search Agent          │
│  • Tìm văn bản luật                 │
│  • AI chọn document tốt nhất        │
│  • Download PDF                     │
└──────────┬─────────────────────────┘
           │
           ▼
┌────────────────────────────────────┐
│  Phase 2: PDF Analysis Agent        │
│  • Extract nội dung PDF             │
│  • AI extract keywords              │
└──────────┬─────────────────────────┘
           │
           ▼
┌────────────────────────────────────┐
│  Phase 3: Opinion Search Agent      │
│  • AI sinh search queries           │
│  • Search DuckDuckGo                │
│  • AI đánh giá relevance            │
│  • Crawl nội dung                   │
│  • AI đánh giá chất lượng           │
│  • Phân tích sentiment & stance     │
│  • Export CSV                       │
└────────────────────────────────────┘
```

## 📁 Cấu trúc

```
autonomous-ai-agent/
├── agents/                 # 🤖 LangGraph Agents
│   ├── base.py            # Base Agent class
│   ├── manager.py         # Manager (orchestrator)
│   └── autonomous_agents.py   # 3 autonomous agents
│
├── core/                   # 🏗️ Core System
│   ├── config.py          # Configuration
│   ├── types.py           # State & Task definitions
│   └── workflow.py        # LangGraph workflow
│
├── tools/                  # 🔧 Tools
│   ├── law_list_crawler.py
│   ├── pdf_downloader.py
│   ├── pdf_extractor.py
│   ├── ollama_autonomous_search.py
│   └── nlp_analyzer.py
│
├── utils/                  # 🛠️ Utilities
│   ├── logging.py
│   └── cli.py
│
├── prompts/               # 💬 LLM Prompts
├── data/                  # 📦 Data (PDFs, CSVs)
├── logs/                  # 📝 Logs
└── main.py               # 🚀 Entry point
```

## 🚀 Quick Start

### 1. Cài đặt

```bash
# Clone repository
git clone <repo-url>
cd autonomous-ai-agent

# Tạo virtual environment
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# Cài đặt dependencies
pip install -r requirements.txt
```

### 2. Cấu hình Ollama

```bash
# Start Ollama server
ollama serve

# Pull model (terminal khác)
ollama pull llama3.2:3b
```

### 3. Chạy

```bash
python main.py
```

Nhập:
- **Tên dự luật**: ví dụ "Luật Trí tuệ nhân tạo 2025"
- **Số opinions**: mặc định 20
- **Quality threshold**: mặc định 0.6 (0-1)

## 💻 Sử dụng trong Code

```python
import asyncio
from core.workflow import run_autonomous_workflow

async def main():
    result = await run_autonomous_workflow(
        project_name="Luật Trí tuệ nhân tạo 2025",
        max_opinions=20,
        quality_threshold=0.6
    )
    
    print(f"✅ PDF: {result['pdf_local_path']}")
    print(f"✅ Keywords: {result['search_queries']}")
    print(f"✅ Opinions: {len(result['analyzed_opinions'])}")
    print(f"✅ CSV: {result['csv_output_path']}")

asyncio.run(main())
```

## 🎯 Workflow (3 Steps)

### Step 1: Autonomous Law Search
**Agent**: `AutonomousLawSearchAgent`  
**Task**: `AUTONOMOUS_LAW_SEARCH`

- Tìm văn bản luật trên duthaoonline
- AI đánh giá và chọn document relevant nhất
- Download PDF tự động

### Step 2: Autonomous PDF Analysis
**Agent**: `AutonomousPdfAnalysisAgent`  
**Task**: `AUTONOMOUS_PDF_ANALYSIS`

- Extract nội dung từ PDF
- AI extract 10-15 keywords quan trọng
- Chuẩn bị keywords cho opinion search

### Step 3: Autonomous Opinion Search
**Agent**: `AutonomousOpinionSearchAgent`  
**Task**: `AUTONOMOUS_OPINION_SEARCH`

- AI sinh 5 search queries đa dạng
- Search DuckDuckGo tự động
- AI đánh giá từng kết quả (relevant?)
- Crawl nội dung từ URLs relevant
- AI đánh giá chất lượng (0-10)
- Phân tích sentiment và stance
- Export CSV

## 📊 Output CSV

| Column | Description |
|--------|-------------|
| title | Tiêu đề bài viết |
| url | URL nguồn |
| source | Domain |
| quality_score | Điểm chất lượng (0-1) |
| sentiment | positive/negative/neutral |
| stance | support/oppose/neutral |
| stance_confidence | Độ tin cậy (0-1) |
| support_score | Điểm ủng hộ |
| oppose_score | Điểm phản đối |
| relevance | high/medium/low |
| quality_feedback | Nhận xét AI |
| key_points | Điểm chính |
| search_query | Query đã dùng |
| content_preview | Preview nội dung |

## 🎨 Tính năng

### AI-Powered
✅ Intelligent Document Search  
✅ Smart Keyword Extraction  
✅ Autonomous Search Query Generation  
✅ DuckDuckGo Search (no bot detection)  
✅ Quality Assessment  
✅ Sentiment Analysis  
✅ Stance Detection  

### LangGraph Framework
✅ State Management  
✅ Agent Orchestration  
✅ Error Handling  
✅ Async Support  
✅ Type Safety  

## ⚙️ Configuration

Create `.env` file (optional):

```env
# LLM
LLM_MODEL=llama3.2:3b
OLLAMA_BASE_URL=http://localhost:11434

# Directories
DATA_DIR=data
PDF_DIR=data/pdfs
CSV_DIR=data/csv

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/autodata.log
```

## 🔧 Troubleshooting

### Ollama không chạy
```bash
ollama serve
ollama list
ollama pull llama3.2:3b
```

### Chrome Driver lỗi
```bash
pip install undetected-chromedriver
# Ubuntu: sudo apt-get install chromium-browser chromium-chromedriver
```

### DuckDuckGo không có kết quả
- Kiểm tra internet
- Đợi vài phút và thử lại

## 📈 Performance

**Typical Runtime** (20 opinions):
- Phase 1: 30-60 giây
- Phase 2: 10-20 giây
- Phase 3: 10-15 phút

**Total**: ~15-20 phút

## 🛠️ Extend

Để thêm agent mới:

1. Tạo agent trong `agents/autonomous_agents.py`
2. Thêm TaskType trong `core/types.py`
3. Update routing trong `core/workflow.py`
4. Update Manager trong `agents/manager.py`

## 📚 Documentation

- **README.md** - This file
- **LANGGRAPH_STRUCTURE.md** - Chi tiết kiến trúc LangGraph

## 🤝 Contributing

Follow LangGraph best practices:
- Single responsibility per agent
- Clear state management
- Proper error handling
- Type safety

## 📝 License

MIT License

---

**Made with ❤️ using LangGraph AI Agent Framework**

🚀 **Ready to use!** Run `python main.py`
