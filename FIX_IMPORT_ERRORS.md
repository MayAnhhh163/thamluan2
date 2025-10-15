# ✅ Fixed Import Errors

## Vấn đề

Lỗi import khi chạy trên Windows:
```
ModuleNotFoundError: No module named 'tools.enhanced_opinion_crawler'
```

## Nguyên nhân

Các file `__init__.py` vẫn còn import các module đã bị xóa:
- `tools/__init__.py` - Import các tool đã xóa
- `prompts/__init__.py` - OK
- `utils/__init__.py` - OK  
- `core/config.py` - Còn VECTOR_DB_DIR và embedding settings
- `core/types.py` - Còn AgentRole không dùng

## Đã sửa

### 1. ✅ tools/__init__.py

**Trước:**
```python
from .enhanced_opinion_crawler import enhanced_opinion_crawler
from .csv_exporter import csv_exporter_tool
from .article_scraper import ArticleScraperTool
# ... nhiều imports đã xóa
```

**Sau:**
```python
from .law_list_crawler import law_list_crawler
from .pdf_downloader import pdf_downloader
from .pdf_extractor import pdf_extractor_tool
from .ollama_autonomous_search import ollama_autonomous_search_agent
from .nlp_analyzer import nlp_analyzer
```

### 2. ✅ core/config.py

**Đã xóa:**
- ❌ `VECTOR_DB_DIR`
- ❌ `CHROMA_PERSIST_DIR`
- ❌ `EMBEDDING_MODEL`
- ❌ `EMBEDDING_DIMENSION`
- ❌ `VECTOR_DB_TYPE`
- ❌ Google Search API settings (không dùng)
- ❌ Facebook settings (không dùng)
- ❌ Nhiều settings không liên quan

**Chỉ giữ:**
- ✅ LLM (Ollama) settings
- ✅ Web scraping settings
- ✅ PDF processing settings
- ✅ Logging settings
- ✅ Autonomous workflow settings

### 3. ✅ core/types.py

**Cleaned AgentRole:**
```python
class AgentRole(str, Enum):
    """Agent roles in AUTONOMOUS AI system"""
    MANAGER = "manager"
    WEB_CRAWLER = "web_crawler"  # Used by autonomous agents
    CONTENT_EXTRACTOR = "content_extractor"  # Used by autonomous agents
    SEARCH_AGENT = "search_agent"  # Used by autonomous agents
```

## Cách chạy

### Trên Windows (PyCharm)

```bash
# 1. Activate virtual environment
.venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start Ollama (terminal khác)
ollama serve

# 4. Pull model
ollama pull llama3.2:3b

# 5. Run
python main.py
```

### Trên Linux/Mac

```bash
# 1. Activate virtual environment
source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start Ollama (terminal khác)
ollama serve

# 4. Pull model
ollama pull llama3.2:3b

# 5. Run
python main.py
```

## Test imports

```python
# Test all imports
python -c "from core.config import config; print('✅ Config OK')"
python -c "from core.types import AgentState; print('✅ Types OK')"
python -c "from core.workflow import run_autonomous_workflow; print('✅ Workflow OK')"
python -c "from agents import manager_agent; print('✅ Agents OK')"
python -c "from tools import law_list_crawler; print('✅ Tools OK')"
```

## Verify installation

```bash
# Check Python version
python --version  # >= 3.9

# Check packages installed
pip list | findstr langgraph  # Windows
pip list | grep langgraph     # Linux/Mac

# Check Ollama
ollama list

# Run main
python main.py
```

## Nếu vẫn lỗi

### ModuleNotFoundError

```bash
pip install -r requirements.txt --force-reinstall
```

### Ollama connection error

```bash
# Check Ollama running
ollama serve

# Check model
ollama list
ollama pull llama3.2:3b

# Test connection
curl http://localhost:11434/api/tags
```

### Import errors

```bash
# Reinstall packages one by one
pip install langgraph langchain langchain-ollama
pip install selenium beautifulsoup4
pip install PyPDF2 pdfplumber
pip install pandas numpy scikit-learn
```

## Files đã clean up

| File | Status | Changes |
|------|--------|---------|
| `tools/__init__.py` | ✅ Cleaned | Chỉ 5 imports |
| `core/config.py` | ✅ Cleaned | Xóa vector DB, embedding |
| `core/types.py` | ✅ Cleaned | Clean AgentRole |
| `prompts/__init__.py` | ✅ OK | Minimal |
| `utils/__init__.py` | ✅ OK | Minimal |

## Kết quả

✅ **Tất cả import errors đã được fix**  
✅ **Code clean, chỉ giữ autonomous workflow**  
✅ **Sẵn sàng chạy trên cả Windows và Linux/Mac**  

## Next steps

1. Cài đặt dependencies: `pip install -r requirements.txt`
2. Start Ollama: `ollama serve`
3. Run: `python main.py`

---

**Status**: ✅ Fixed and Ready to Run!
