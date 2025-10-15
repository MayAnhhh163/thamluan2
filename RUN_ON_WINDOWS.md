# 🪟 Hướng dẫn chạy trên Windows

## Yêu cầu

- Windows 10/11
- Python 3.9+ 
- PyCharm (hoặc VS Code)
- Chrome browser
- 4GB+ RAM

## Bước 1: Cài Python

1. Download Python từ https://www.python.org/downloads/
2. **Quan trọng**: Tick ✅ "Add Python to PATH"
3. Install

Kiểm tra:
```cmd
python --version
```

## Bước 2: Clone Project

```cmd
git clone <repository-url>
cd autonomous-ai-agent
```

## Bước 3: Tạo Virtual Environment

**Option 1: Command Prompt**
```cmd
python -m venv .venv
.venv\Scripts\activate
```

**Option 2: PyCharm**
- File → Settings → Project → Python Interpreter
- Click ⚙️ → Add → Virtualenv Environment
- Chọn `.venv` folder

## Bước 4: Cài Dependencies

```cmd
pip install -r requirements.txt
```

Nếu lỗi, cài từng nhóm:

```cmd
REM Core AI
pip install langgraph langchain langchain-ollama langchain-core

REM Web automation
pip install selenium beautifulsoup4 requests undetected-chromedriver

REM PDF processing
pip install PyPDF2 pdfplumber

REM Data processing
pip install pandas numpy scikit-learn

REM Utilities
pip install python-dotenv tqdm
```

## Bước 5: Cài Ollama

1. Download Ollama for Windows: https://ollama.com/download
2. Install
3. Mở Command Prompt mới:

```cmd
ollama serve
```

4. Mở Command Prompt khác:

```cmd
ollama pull llama3.2:3b
```

## Bước 6: Cài Chrome (nếu chưa có)

Download từ: https://www.google.com/chrome/

## Bước 7: Chạy Project

### Trong PyCharm:

1. Right-click `main.py`
2. Click "Run 'main'"
3. Nhập thông tin khi được hỏi

### Trong Command Prompt:

```cmd
REM Activate venv
.venv\Scripts\activate

REM Run
python main.py
```

## Nhập thông tin

Khi chạy, nhập:

```
Tên dự luật: Luật Trí tuệ nhân tạo 2025
Số opinions: 20
Quality threshold: 0.6
```

Đợi 15-20 phút → Nhận kết quả CSV! 🎉

## Troubleshooting

### Lỗi: `ModuleNotFoundError`

```cmd
pip install -r requirements.txt --force-reinstall
```

### Lỗi: Ollama không connect

```cmd
REM Kiểm tra Ollama đang chạy
tasklist | findstr ollama

REM Nếu không có, chạy
ollama serve

REM Test connection
curl http://localhost:11434/api/tags
```

### Lỗi: Chrome driver

```cmd
pip install undetected-chromedriver --upgrade
```

### Lỗi: Permission denied

- Chạy Command Prompt as Administrator
- Hoặc thay đổi permissions của folder

### Lỗi: `python` không tìm thấy

```cmd
REM Dùng py thay vì python
py --version
py -m venv .venv
py main.py
```

### Virtual environment không activate

```cmd
REM PowerShell
.venv\Scripts\Activate.ps1

REM Nếu lỗi execution policy
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

REM Command Prompt
.venv\Scripts\activate.bat
```

## Tips for Windows

### 1. Sử dụng Windows Terminal

Download: https://aka.ms/terminal

- Đẹp hơn Command Prompt
- Hỗ trợ tabs
- Copy/paste dễ hơn

### 2. Dùng PyCharm

- Auto-detect virtual environment
- Integrated terminal
- Easy debugging
- Code completion

### 3. Check Firewall

Nếu Ollama không connect:
- Windows Security → Firewall & network protection
- Allow an app through firewall
- Thêm Ollama

### 4. Antivirus

Một số antivirus có thể block:
- Chrome driver
- Selenium
- Python scripts

→ Add exception cho project folder

## Paths trên Windows

Project sử dụng `pathlib` nên tự động handle:

```python
# Tự động chuyển thành Windows paths
data/pdfs/file.pdf  → data\pdfs\file.pdf
logs/app.log        → logs\app.log
```

## Output

CSV files sẽ được lưu tại:
```
D:\AutoData2\AutoData2\LawInTech\data\csv\autonomous_<topic>_<timestamp>.csv
```

Mở bằng Excel để xem kết quả!

## Environment Variables (Optional)

Tạo file `.env` trong project root:

```env
LLM_MODEL=llama3.2:3b
OLLAMA_BASE_URL=http://localhost:11434
LOG_LEVEL=INFO
SELENIUM_HEADLESS=false
```

## Next Steps

1. Đọc [QUICKSTART.md](QUICKSTART.md)
2. Đọc [README.md](README.md)
3. Chạy `python main.py`

---

**Cần help?** Check [INSTALL.md](INSTALL.md) hoặc [FIX_IMPORT_ERRORS.md](FIX_IMPORT_ERRORS.md)

🚀 **Happy coding on Windows!**
