# ✅ Windows Setup - Complete Guide

## 🎯 Đã Fix Tất Cả Lỗi

### Lỗi đã fix:

1. ✅ **ModuleNotFoundError: enhanced_opinion_crawler**
   - Fixed: `tools/__init__.py` chỉ import tools cần thiết

2. ✅ **AttributeError: MIN_KEYWORD_LENGTH**
   - Fixed: Thêm config vào `core/config.py`

3. ✅ **dotenv optional**
   - Fixed: `core/config.py` không require dotenv

## 🚀 Chạy trên Windows (PyCharm)

### Step 1: Cài Python Packages

Mở Terminal trong PyCharm (Alt+F12), chạy:

```bash
# Activate virtual environment (nếu chưa active)
.venv\Scripts\activate

# Cài đặt TẤT CẢ packages
pip install -r requirements.txt
```

**Quan trọng**: Đảm bảo TẤT CẢ packages được cài thành công. Nếu lỗi, cài từng nhóm:

```bash
# Group 1: Core AI
pip install langgraph langchain langchain-ollama langchain-core

# Group 2: Web
pip install selenium beautifulsoup4 requests undetected-chromedriver

# Group 3: PDF
pip install PyPDF2 pdfplumber

# Group 4: Data
pip install pandas numpy scikit-learn

# Group 5: Utils
pip install python-dotenv tqdm
```

### Step 2: Start Ollama

Mở Command Prompt **MỚI** (không phải trong PyCharm), chạy:

```cmd
ollama serve
```

Giữ window này mở!

### Step 3: Pull Model

Mở Command Prompt **MỚI** nữa, chạy:

```cmd
ollama pull llama3.2:3b
```

Đợi download xong.

### Step 4: Verify Ollama

```cmd
ollama list
```

Phải thấy `llama3.2:3b` trong list.

### Step 5: Run Main.py

Trong PyCharm:

1. Right-click vào `main.py`
2. Click **"Run 'main'"**
3. Nhập thông tin:
   - Tên dự luật: `Luật Trí tuệ nhân tạo 2025`
   - Số opinions: `20`
   - Quality threshold: `0.6`

**Hoặc** chạy trong Terminal:

```bash
python main.py
```

## ✅ Verify Installation

Chạy lần lượt để verify từng phần:

### Test 1: Python Version
```cmd
python --version
```
Expected: Python 3.9+

### Test 2: Packages Installed
```cmd
pip list | findstr langgraph
pip list | findstr selenium
pip list | findstr PyPDF2
```
Expected: Thấy các packages

### Test 3: Ollama Running
```cmd
curl http://localhost:11434/api/tags
```
Expected: JSON response

### Test 4: Import Test
```python
python -c "from core.config import config; print('OK')"
```
Expected: OK

### Test 5: Full Import Test
```python
python -c "from core.workflow import run_autonomous_workflow; print('✅ Ready!')"
```
Expected: ✅ Ready!

## 🐛 Common Errors & Solutions

### Error 1: `ModuleNotFoundError: langgraph`

**Solution:**
```bash
pip install langgraph langchain langchain-ollama langchain-core
```

### Error 2: `ModuleNotFoundError: selenium`

**Solution:**
```bash
pip install selenium undetected-chromedriver
```

### Error 3: Ollama connection error

**Solution:**
```bash
# Check Ollama running
tasklist | findstr ollama

# If not running
ollama serve

# Test connection
curl http://localhost:11434/api/tags
```

### Error 4: Chrome driver error

**Solution:**
```bash
# Upgrade undetected-chromedriver
pip install undetected-chromedriver --upgrade

# Or install regular chromedriver
pip install webdriver-manager
```

### Error 5: `python-dotenv` not found

**Don't worry!** dotenv is now optional. Just install it:
```bash
pip install python-dotenv
```

## 📋 Checklist Before Running

- [ ] Python 3.9+ installed
- [ ] Virtual environment activated
- [ ] All packages installed (`pip install -r requirements.txt`)
- [ ] Ollama running (`ollama serve`)
- [ ] Model pulled (`ollama pull llama3.2:3b`)
- [ ] Chrome installed
- [ ] Internet connection active

## 🎯 Config đã fix

File `core/config.py` đã có TẤT CẢ config cần thiết:

```python
# PDF Processing
PDF_MAX_SIZE_MB = 50
MIN_KEYWORD_LENGTH = 3
MAX_KEYWORDS = 50
MIN_KEYWORD_FREQUENCY = 2
VIETNAMESE_STOPWORDS = set([...])

# LLM
LLM_MODEL = "llama3.2:3b"
OLLAMA_BASE_URL = "http://localhost:11434"

# Paths
PDF_DIR = data/pdfs
CSV_DIR = data/csv
LOGS_DIR = logs
```

## 🎉 Expected Output

Khi chạy thành công, bạn sẽ thấy:

```
================================================================================
🤖 AUTONOMOUS AI AGENT SYSTEM - LangGraph
================================================================================
Full AI-powered workflow:
  1. AI tìm và download PDF văn bản luật
  2. AI extract PDF và tạo keywords
  3. AI search + crawl + analyze opinions
================================================================================

📋 Nhập tên dự luật/chủ đề: Luật Trí tuệ nhân tạo 2025
   Số opinions tối đa [20]: 20
   Quality threshold (0-1) [0.6]: 0.6

🚀 Starting AUTONOMOUS workflow...

[... AI working ...]

✅ Workflow completed successfully!
💾 CSV Output: data\csv\autonomous_Luật_Trí_tuệ_nhân_tạo_2025_20251015_123045.csv
```

## 📂 Output Location

CSV file sẽ được lưu tại:
```
D:\AutoData2\AutoData2\LawInTech\data\csv\autonomous_<topic>_<timestamp>.csv
```

Mở bằng Excel để xem kết quả!

## 🔧 Environment Variables (Optional)

Tạo file `.env` trong project root:

```env
# LLM
LLM_MODEL=llama3.2:3b
OLLAMA_BASE_URL=http://localhost:11434

# Autonomous workflow
DEFAULT_MAX_OPINIONS=20
DEFAULT_QUALITY_THRESHOLD=0.6

# Logging
LOG_LEVEL=INFO

# Selenium
SELENIUM_HEADLESS=false
```

## 📚 Next Steps

1. Verify installation: Run all tests above
2. Read [QUICKSTART.md](QUICKSTART.md) for quick start
3. Read [README.md](README.md) for full documentation
4. Run `python main.py`

---

**Status**: ✅ All Fixed, Ready to Run on Windows!

**Last Updated**: After fixing config.MIN_KEYWORD_LENGTH error

🚀 **Run now**: `python main.py`
