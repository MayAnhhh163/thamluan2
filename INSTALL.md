# 🔧 Installation Guide

## Yêu cầu hệ thống

- Python 3.9+
- Ollama server
- Chrome/Chromium browser
- 4GB+ RAM
- Internet connection

## Cài đặt chi tiết

### 1. Clone Repository

```bash
git clone <repository-url>
cd autonomous-ai-agent
```

### 2. Tạo Virtual Environment

**Linux/Mac:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Cài đặt Dependencies

```bash
pip install -r requirements.txt
```

**Lưu ý**: Nếu gặp lỗi với `undetected-chromedriver`, cài từng package:

```bash
pip install langgraph langchain langchain-ollama langchain-core
pip install selenium beautifulsoup4 requests
pip install PyPDF2 pdfplumber
pip install pandas numpy scikit-learn
pip install python-dotenv tqdm
pip install undetected-chromedriver
```

### 4. Cài đặt Chrome/Chromium

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install chromium-browser chromium-chromedriver
```

**Mac:**
```bash
brew install --cask google-chrome
```

**Windows:**
- Download và cài đặt Chrome từ https://www.google.com/chrome/

### 5. Cài đặt Ollama

**Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Mac:**
```bash
brew install ollama
```

**Windows:**
- Download từ https://ollama.com/download

### 6. Start Ollama và Pull Model

```bash
# Start Ollama server
ollama serve

# Trong terminal khác, pull model
ollama pull llama3.2:3b
```

### 7. Cấu hình (Optional)

Tạo file `.env`:

```env
# LLM Configuration
LLM_MODEL=llama3.2:3b
OLLAMA_BASE_URL=http://localhost:11434
LLM_TEMPERATURE=0.3
LLM_MAX_TOKENS=2048

# Directories
DATA_DIR=data
PDF_DIR=data/pdfs
CSV_DIR=data/csv

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/autodata.log
```

### 8. Test Installation

```bash
python main.py
```

Nếu hiện menu nhập tên dự luật → ✅ Cài đặt thành công!

## Troubleshooting

### Lỗi: `ModuleNotFoundError`

```bash
# Cài lại dependencies
pip install -r requirements.txt
```

### Lỗi: `No module named 'selenium'`

```bash
pip install selenium undetected-chromedriver
```

### Lỗi: Ollama không connect

```bash
# Kiểm tra Ollama
ollama list
ollama serve

# Kiểm tra port
curl http://localhost:11434/api/tags
```

### Lỗi: Chrome driver

```bash
# Linux/Mac
pip install undetected-chromedriver --upgrade

# Hoặc cài chrome driver system-wide
sudo apt-get install chromium-chromedriver  # Ubuntu/Debian
```

### Lỗi: Permission denied (logs/)

```bash
mkdir -p logs data/pdfs data/csv
chmod 755 logs data
```

## Verify Installation

Chạy các lệnh sau để verify:

```bash
# 1. Check Python version
python --version  # Should be 3.9+

# 2. Check packages
pip list | grep langgraph
pip list | grep selenium

# 3. Check Ollama
ollama list

# 4. Check directories
ls -la data/
ls -la logs/

# 5. Test import
python -c "from core.workflow import run_autonomous_workflow; print('✅ Import OK')"
```

## Dependencies chi tiết

| Package | Version | Purpose |
|---------|---------|---------|
| langgraph | >=0.2.0 | AI Agent framework |
| langchain | >=0.3.0 | LLM orchestration |
| langchain-ollama | >=0.1.0 | Ollama integration |
| selenium | >=4.0.0 | Web automation |
| beautifulsoup4 | >=4.9.0 | HTML parsing |
| undetected-chromedriver | >=3.5.0 | Chrome driver |
| PyPDF2 | >=3.0.0 | PDF reading |
| pdfplumber | >=0.10.0 | PDF extraction |
| pandas | >=2.0.0 | Data processing |
| numpy | >=1.24.0 | Numerical computing |
| scikit-learn | >=1.3.0 | NLP/ML |
| requests | >=2.31.0 | HTTP requests |
| python-dotenv | >=1.0.0 | Environment config |
| tqdm | >=4.65.0 | Progress bars |

## Next Steps

Sau khi cài đặt xong:

1. Đọc [QUICKSTART.md](QUICKSTART.md) để chạy ngay
2. Đọc [README.md](README.md) để hiểu workflow
3. Chạy `python main.py` để bắt đầu

---

**Cần help?** Kiểm tra [README.md](README.md) hoặc [INDEX.md](INDEX.md)
