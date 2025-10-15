# 📖 Documentation Index

## 🎯 Start Here

### For Quick Start
👉 **[QUICKSTART.md](QUICKSTART.md)** - Chạy ngay trong 3 bước

### For Understanding
👉 **[README.md](README.md)** - Overview và hướng dẫn đầy đủ

## 📚 Architecture & Structure

### LangGraph Framework
👉 **[LANGGRAPH_STRUCTURE.md](LANGGRAPH_STRUCTURE.md)** - Chi tiết kiến trúc LangGraph AI Agent

### Project Structure
👉 **[PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)** - Cấu trúc thư mục và files

### Cleanup Report
👉 **[CLEANUP_SUMMARY.md](CLEANUP_SUMMARY.md)** - Báo cáo cleanup và optimization

## 🔍 Quick Reference

### File Structure
```
autonomous-ai-agent/
├── agents/          # 4 files - AI Agents
├── core/            # 4 files - Core System
├── tools/           # 6 files - Utilities
├── utils/           # 3 files - Helpers
├── prompts/         # 3 files - LLM Prompts
├── data/            # PDF & CSV storage
├── logs/            # Log files
└── main.py          # Entry point
```

### Workflow
```
MANAGER → LAW_SEARCH → PDF_ANALYSIS → OPINION_SEARCH → CSV
```

### Usage
```bash
python main.py
```

## 📊 Metrics

| Metric | Value |
|--------|-------|
| Python files | 21 |
| Total code | ~119KB |
| TaskTypes | 3 |
| Agents | 4 |
| Tools | 6 |
| Dependencies | 14 |

## 🎨 Features

✅ AI-powered law document search  
✅ Smart PDF analysis & keyword extraction  
✅ Autonomous opinion search & crawl  
✅ DuckDuckGo integration  
✅ Sentiment & stance analysis  
✅ CSV export  

## 🚀 Quick Commands

```bash
# Install
pip install -r requirements.txt

# Start Ollama
ollama serve
ollama pull llama3.2:3b

# Run
python main.py

# Code usage
from core.workflow import run_autonomous_workflow
result = await run_autonomous_workflow(
    project_name="Luật AI",
    max_opinions=20,
    quality_threshold=0.6
)
```

## 🔗 Links

- [Main README](README.md)
- [Quick Start](QUICKSTART.md)
- [Architecture](LANGGRAPH_STRUCTURE.md)
- [Structure](PROJECT_STRUCTURE.md)
- [Cleanup Report](CLEANUP_SUMMARY.md)

---

**Status**: ✅ Production Ready  
**Total**: 21 Python files, ~119KB clean code  
**Framework**: LangGraph AI Agent System  

🚀 **Ready to use!**
