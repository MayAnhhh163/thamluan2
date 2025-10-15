# 📖 Documentation Index

## 🚀 Getting Started

### Quick Start (3 steps)
👉 **[QUICKSTART.md](QUICKSTART.md)** - Chạy ngay trong 3 bước

### Installation Guide
👉 **[INSTALL.md](INSTALL.md)** - Hướng dẫn cài đặt chi tiết (Linux/Mac/Windows)

### Run on Windows
👉 **[RUN_ON_WINDOWS.md](RUN_ON_WINDOWS.md)** - Hướng dẫn đặc biệt cho Windows + PyCharm

### Fix Import Errors
👉 **[FIX_IMPORT_ERRORS.md](FIX_IMPORT_ERRORS.md)** - Fix lỗi import sau khi cleanup

## 📚 Understanding the System

### Main Documentation
👉 **[README.md](README.md)** - Overview, features, và usage

### Architecture
👉 **[LANGGRAPH_STRUCTURE.md](LANGGRAPH_STRUCTURE.md)** - Chi tiết kiến trúc LangGraph

### Project Structure
👉 **[PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)** - Cấu trúc thư mục và files

### Cleanup Report
👉 **[CLEANUP_SUMMARY.md](CLEANUP_SUMMARY.md)** - Báo cáo cleanup (xóa 205KB+ code)

## 🔍 Quick Reference

### File Structure
```
autonomous-ai-agent/
├── agents/          # 4 files - LangGraph Agents
├── core/            # 4 files - Core System
├── tools/           # 6 files - Utilities
├── utils/           # 3 files - Helpers
├── prompts/         # 3 files - LLM Prompts
├── data/            # PDF & CSV storage
├── logs/            # Log files
└── main.py          # Entry point
```

### Workflow (3 Steps)
```
MANAGER → LAW_SEARCH → PDF_ANALYSIS → OPINION_SEARCH → CSV
```

### Quick Commands
```bash
# Install
pip install -r requirements.txt

# Start Ollama
ollama serve
ollama pull llama3.2:3b

# Run
python main.py
```

## 📊 System Metrics

| Metric | Value |
|--------|-------|
| Python files | 21 |
| Total code | ~119KB |
| TaskTypes | 3 |
| Agents | 4 |
| Tools | 6 |
| Dependencies | 14 |
| Docs | 9 markdown files |

## 🎯 Use Cases

### For First Time Users
1. **[QUICKSTART.md](QUICKSTART.md)** - Bắt đầu nhanh
2. **[README.md](README.md)** - Hiểu system
3. Run `python main.py`

### For Windows Users
1. **[RUN_ON_WINDOWS.md](RUN_ON_WINDOWS.md)** - Setup trên Windows
2. **[INSTALL.md](INSTALL.md)** - Chi tiết cài đặt
3. **[FIX_IMPORT_ERRORS.md](FIX_IMPORT_ERRORS.md)** - Fix lỗi nếu có

### For Developers
1. **[LANGGRAPH_STRUCTURE.md](LANGGRAPH_STRUCTURE.md)** - Hiểu architecture
2. **[PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)** - Hiểu code structure
3. **[CLEANUP_SUMMARY.md](CLEANUP_SUMMARY.md)** - Hiểu optimization

## 🎨 Features Overview

### AI-Powered
✅ Intelligent law document search  
✅ Smart PDF analysis & keywords  
✅ Autonomous opinion search  
✅ DuckDuckGo integration  
✅ Sentiment & stance analysis  
✅ CSV export  

### LangGraph Framework
✅ State management  
✅ Agent orchestration  
✅ Error handling  
✅ Async support  
✅ Type safety  

## 🛠️ Troubleshooting Guide

| Problem | Solution |
|---------|----------|
| Import errors | [FIX_IMPORT_ERRORS.md](FIX_IMPORT_ERRORS.md) |
| Windows setup | [RUN_ON_WINDOWS.md](RUN_ON_WINDOWS.md) |
| Installation | [INSTALL.md](INSTALL.md) |
| General help | [README.md](README.md) |

## 📱 Platform-Specific

### Windows
- **[RUN_ON_WINDOWS.md](RUN_ON_WINDOWS.md)** - Complete Windows guide
- PyCharm integration
- PowerShell commands
- Troubleshooting tips

### Linux/Mac
- **[INSTALL.md](INSTALL.md)** - Installation guide
- **[QUICKSTART.md](QUICKSTART.md)** - Quick commands
- Terminal usage

## 🔗 Documentation Links

### Quick Access
- [Quick Start](QUICKSTART.md) - Start in 3 steps
- [Install Guide](INSTALL.md) - Detailed installation
- [Windows Guide](RUN_ON_WINDOWS.md) - For Windows users
- [Fix Errors](FIX_IMPORT_ERRORS.md) - Troubleshooting

### Deep Dive
- [README](README.md) - Main documentation
- [Architecture](LANGGRAPH_STRUCTURE.md) - LangGraph structure
- [Structure](PROJECT_STRUCTURE.md) - Code organization
- [Cleanup](CLEANUP_SUMMARY.md) - Optimization report

## 📈 Workflow Overview

```
1. LAW_SEARCH Agent
   ↓
   Find & download law PDF
   ↓
2. PDF_ANALYSIS Agent
   ↓
   Extract keywords from PDF
   ↓
3. OPINION_SEARCH Agent
   ↓
   Search → Crawl → Analyze → Export CSV
```

## 🎓 Learning Path

1. **Start**: [QUICKSTART.md](QUICKSTART.md)
2. **Understand**: [README.md](README.md)
3. **Architecture**: [LANGGRAPH_STRUCTURE.md](LANGGRAPH_STRUCTURE.md)
4. **Code**: [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)

## 💡 Tips

- Use **QUICKSTART.md** if you want to run immediately
- Use **INSTALL.md** if you encounter installation issues
- Use **RUN_ON_WINDOWS.md** if you're on Windows
- Use **FIX_IMPORT_ERRORS.md** if you get import errors
- Use **README.md** to understand the full system

---

**Status**: ✅ Production Ready  
**Platform**: Windows, Linux, Mac  
**Framework**: LangGraph AI Agent System  
**Total Docs**: 9 markdown files  

🚀 **Choose your starting point and dive in!**
