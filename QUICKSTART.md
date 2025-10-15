# ⚡ Quick Start - Autonomous AI Agent

## 🚀 Chạy ngay trong 3 bước

### Bước 1: Cài đặt

```bash
# Clone repo
git clone <repo-url>
cd autonomous-ai-agent

# Tạo virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Cài packages
pip install -r requirements.txt
```

### Bước 2: Start Ollama

```bash
# Terminal 1: Start Ollama server
ollama serve

# Terminal 2: Pull model
ollama pull llama3.2:3b
```

### Bước 3: Chạy

```bash
python main.py
```

Nhập:
- Tên dự luật: `Luật Trí tuệ nhân tạo 2025`
- Số opinions: `20`
- Quality threshold: `0.6`

**Done!** Đợi 15-20 phút → Nhận CSV kết quả 🎉

## 📊 Output

File CSV được lưu tại `data/csv/autonomous_<topic>_<timestamp>.csv` với các cột:

- **title**: Tiêu đề
- **url**: Nguồn
- **quality_score**: Chất lượng (0-1)
- **sentiment**: Cảm xúc
- **stance**: Quan điểm (ủng hộ/phản đối)
- **key_points**: Điểm chính
- **content_preview**: Preview nội dung

## 💻 Sử dụng trong Code

```python
import asyncio
from core.workflow import run_autonomous_workflow

async def main():
    result = await run_autonomous_workflow(
        project_name="Luật AI 2025",
        max_opinions=20,
        quality_threshold=0.6
    )
    print(f"✅ CSV: {result['csv_output_path']}")

asyncio.run(main())
```

## 🔧 Config (Optional)

Tạo file `.env`:

```env
LLM_MODEL=llama3.2:3b
OLLAMA_BASE_URL=http://localhost:11434
LOG_LEVEL=INFO
```

## ❓ Troubleshooting

### Ollama không chạy
```bash
ollama serve
ollama list
```

### Chrome driver lỗi
```bash
pip install undetected-chromedriver
```

### Import error
```bash
pip install -r requirements.txt
```

## 📚 Docs

- `README.md` - Full documentation
- `LANGGRAPH_STRUCTURE.md` - Architecture
- `PROJECT_STRUCTURE.md` - Code structure

---

**That's it!** Chỉ 3 bước, system chạy ngay! 🚀
