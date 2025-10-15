# 🤖 Autonomous AI Agent System - LangGraph

Hệ thống AI Agent tự động thu thập và phân tích ý kiến về dự luật sử dụng framework LangGraph.

## 🎯 Tổng quan

Autonomous AI Agent System là một workflow hoàn toàn tự động, sử dụng AI để:

1. **Tìm văn bản luật**: AI tự động tìm và download PDF văn bản luật chính thức
2. **Phân tích PDF**: AI extract nội dung và tạo keywords
3. **Thu thập ý kiến**: AI tự động search, crawl và phân tích opinions với sentiment/stance

## 🏗️ Kiến trúc LangGraph

```
┌─────────────────────────────────────────────────────┐
│                   MANAGER AGENT                      │
│            (Điều phối workflow)                      │
└────────────┬────────────────────────────────────────┘
             │
             ▼
┌────────────────────────────────────────────────────┐
│  PHASE 1: Autonomous Law Search Agent              │
│  - AI tìm văn bản luật                             │
│  - AI đánh giá và chọn document tốt nhất           │
│  - Download PDF tự động                            │
└────────────┬───────────────────────────────────────┘
             │
             ▼
┌────────────────────────────────────────────────────┐
│  PHASE 2: Autonomous PDF Analysis Agent            │
│  - Extract nội dung từ PDF                         │
│  - AI extract keywords quan trọng                  │
│  - Chuẩn bị keywords cho search                    │
└────────────┬───────────────────────────────────────┘
             │
             ▼
┌────────────────────────────────────────────────────┐
│  PHASE 3: Autonomous Opinion Search Agent          │
│  - AI sinh search queries                          │
│  - Search DuckDuckGo tự động                       │
│  - AI đánh giá relevance                           │
│  - Crawl nội dung                                  │
│  - AI đánh giá chất lượng                          │
│  - Phân tích sentiment & stance                    │
│  - Export CSV tự động                              │
└────────────────────────────────────────────────────┘
```

## 📁 Cấu trúc thư mục

```
/
├── agents/                      # LangGraph AI Agents
│   ├── __init__.py
│   ├── base.py                 # Base Agent class
│   ├── manager.py              # Manager Agent (orchestrator)
│   └── autonomous_agents.py    # 3 autonomous agents
│
├── core/                       # Core system
│   ├── __init__.py
│   ├── config.py              # Configuration
│   ├── types.py               # Type definitions
│   └── workflow.py            # LangGraph workflow setup
│
├── tools/                      # Tools for agents
│   ├── law_list_crawler.py   # Tìm văn bản luật
│   ├── pdf_downloader.py     # Download PDFs
│   ├── pdf_extractor.py      # Extract PDF content
│   ├── ollama_autonomous_search.py  # Autonomous search
│   └── nlp_analyzer.py       # NLP analysis
│
├── utils/                      # Utilities
│   ├── logging.py            # Logging setup
│   └── cli.py                # CLI argument parsing
│
├── prompts/                    # Prompts for LLM
│   └── manager_system.md
│
├── data/                       # Data storage
│   ├── pdfs/                 # Downloaded PDFs
│   └── csv/                  # CSV outputs
│
├── logs/                       # Log files
│
├── main.py                     # Entry point
├── requirements.txt            # Dependencies
└── README.md                   # This file
```

## 🚀 Quick Start

### 1. Cài đặt

```bash
# Clone repository
git clone <repo-url>
cd <repo-name>

# Tạo virtual environment
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# hoặc
.venv\Scripts\activate  # Windows

# Cài đặt dependencies
pip install -r requirements.txt
```

### 2. Cấu hình Ollama

```bash
# Start Ollama server
ollama serve

# Pull model (trong terminal khác)
ollama pull llama3.2:3b
```

### 3. Chạy workflow

```bash
python main.py
```

Sau đó nhập:
- Tên dự luật/chủ đề
- Số opinions tối đa (mặc định: 20)
- Quality threshold (mặc định: 0.6)

## 💻 Sử dụng trong code

```python
import asyncio
from core.workflow import run_autonomous_workflow

async def main():
    result = await run_autonomous_workflow(
        project_name="Luật Trí tuệ nhân tạo 2025",
        max_opinions=20,
        quality_threshold=0.6
    )
    
    print(f"✅ CSV: {result['csv_output_path']}")
    print(f"📊 Opinions: {len(result['analyzed_opinions'])}")

asyncio.run(main())
```

## 🎨 Tính năng

### AI-Powered
✅ **Intelligent Document Search**: AI chọn văn bản luật chính xác nhất  
✅ **Smart Keyword Extraction**: AI extract keywords từ PDF  
✅ **Autonomous Search**: AI sinh search queries đa dạng  
✅ **DuckDuckGo Search**: Search đáng tin cậy, không bot detection  
✅ **Quality Assessment**: AI đánh giá chất lượng trước khi lưu  
✅ **Sentiment Analysis**: Phân tích cảm xúc tự động  
✅ **Stance Detection**: Phát hiện quan điểm (ủng hộ/phản đối/trung lập)

### LangGraph Framework
✅ **State Management**: Quản lý state chuẩn LangGraph  
✅ **Agent Orchestration**: Manager điều phối các agents  
✅ **Error Handling**: Xử lý lỗi tích hợp  
✅ **Async Support**: Hỗ trợ async/await đầy đủ  
✅ **Logging**: Centralized logging  
✅ **Type Safety**: TypedDict và dataclass

## 📊 Output

Workflow tạo file CSV với các cột:

| Cột | Mô tả |
|-----|-------|
| title | Tiêu đề bài viết |
| url | URL nguồn |
| source | Domain |
| quality_score | Điểm chất lượng (0-1) |
| sentiment | positive/negative/neutral |
| stance | support/oppose/neutral |
| stance_confidence | Độ tin cậy stance (0-1) |
| support_score | Điểm ủng hộ |
| oppose_score | Điểm phản đối |
| relevance | high/medium/low |
| quality_feedback | Nhận xét AI |
| key_points | Các điểm chính |
| search_query | Query đã dùng |
| content_preview | Preview nội dung |

## 🔧 Configuration

File `.env` (tùy chọn):

```env
# LLM Model
LLM_MODEL=llama3.2:3b
OLLAMA_BASE_URL=http://localhost:11434

# Directories
DATA_DIR=data
PDF_DIR=data/pdfs
CSV_DIR=data/csv
VECTOR_DB_DIR=data/vector_db

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/autodata.log
```

## 🐛 Troubleshooting

### Ollama không chạy
```bash
# Start Ollama
ollama serve

# Kiểm tra models
ollama list

# Pull model nếu cần
ollama pull llama3.2:3b
```

### Chrome Driver lỗi
```bash
# Cài đặt undetected-chromedriver
pip install undetected-chromedriver

# Ubuntu/Debian - cài Chrome
sudo apt-get install chromium-browser chromium-chromedriver
```

### DuckDuckGo không trả kết quả
- Kiểm tra kết nối internet
- Thử lại sau vài phút
- DuckDuckGo có thể giới hạn requests

## 📖 Documentation

- **README_AUTONOMOUS.md**: Hướng dẫn chi tiết autonomous workflow
- **CHANGELOG.md**: Lịch sử thay đổi
- **REFACTORING_SUMMARY.md**: Tổng kết refactoring

## 🤝 Contributing

Workflow này được xây dựng theo chuẩn LangGraph AI Agent framework. Để mở rộng:

1. Tạo agent mới trong `agents/`
2. Thêm TaskType mới vào `core/types.py`
3. Cập nhật routing trong `core/workflow.py`
4. Update Manager orchestration trong `agents/manager.py`

## 📝 License

MIT License

## 👥 Support

Nếu gặp vấn đề:
1. Kiểm tra logs trong `logs/`
2. Enable debug: `logging.basicConfig(level=logging.DEBUG)`
3. Xem errors trong state: `result.get('errors', [])`

---

Made with ❤️ using LangGraph AI Agent Framework
