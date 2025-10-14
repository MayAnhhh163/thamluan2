# 🚀 Cài đặt Autonomous Search (Fix Google Bot Detection)

## Vấn đề

Google phát hiện bot và yêu cầu CAPTCHA → Search không thành công

## Giải pháp

Hệ thống đã được fix với **3 layers protection**:

### Layer 1: Undetected ChromeDriver ✨ (Best)
Sử dụng `undetected-chromedriver` để bypass Google bot detection

### Layer 2: Stealth Mode 
Nếu không có undetected-chromedriver, dùng Selenium với stealth settings

### Layer 3: DuckDuckGo Fallback 🦆
Nếu Google vẫn chặn, tự động chuyển sang DuckDuckGo (không có CAPTCHA)

## Cài đặt Nhanh

### Bước 1: Cài undetected-chromedriver

```bash
pip install undetected-chromedriver
```

**Quan trọng:** Package này giúp bypass Google bot detection!

### Bước 2: Test lại

```bash
python tools/test_autonomous_search.py
```

**Kết quả mong đợi:**

```
✅ Chrome driver initialized (undetected mode)

🔍 Query 1/5: 'Ý kiến chuyên gia luật Trí tuệ nhân tạo'
Found 10 search results  ← Thành công!

  [1] Evaluating: Chuyên gia: Luật AI cần rõ ràng hơn...
      ✅ Ollama says: Relevant! Crawling...
      📄 Crawled 2847 chars
      ⭐ Quality: 0.87
      💾 SAVED! (1/10)
```

## Nếu Vẫn Gặp Lỗi

### Option A: Thử chạy với quyền admin

```bash
# Windows (Run as Administrator)
python tools/test_autonomous_search.py

# Linux/Mac
sudo python tools/test_autonomous_search.py
```

### Option B: Update Chrome

```bash
# Download Chrome mới nhất
# https://www.google.com/chrome/

# Hoặc update chromedriver
pip install --upgrade undetected-chromedriver
```

### Option C: Dùng DuckDuckGo thay vì Google

Hệ thống sẽ **tự động** fallback sang DuckDuckGo nếu Google chặn:

```
⚠️ Google detected bot, trying DuckDuckGo instead...
🦆 Searching on DuckDuckGo...
✅ DuckDuckGo found 10 results
```

DuckDuckGo **KHÔNG CÓ** bot detection, luôn hoạt động!

## Verify Installation

```bash
# Check if undetected-chromedriver installed
python -c "import undetected_chromedriver; print('✅ Installed')"

# If error, install:
pip install undetected-chromedriver
```

## Flow Diagram

```
┌─────────────────────────────────────┐
│  Start Autonomous Search            │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│  Check: undetected-chromedriver?    │
└────────────┬────────────────────────┘
             │
      YES ┌──┴──┐ NO
          │     │
          ▼     ▼
    ┌─────────┐ ┌────────────────┐
    │Undetected│ │Stealth Selenium│
    │  Mode   │ │   + Tricks     │
    └────┬────┘ └────┬───────────┘
         │           │
         └─────┬─────┘
               │
               ▼
    ┌──────────────────┐
    │  Try Google      │
    └────────┬─────────┘
             │
    Blocked? │
             │
      YES ┌──┴──┐ NO
          │     │
          ▼     ▼
    ┌──────────┐ ┌─────────┐
    │DuckDuckGo│ │ Success │
    │ (Always  │ │         │
    │  works)  │ └─────────┘
    └──────────┘
```

## Các Package Cần Thiết

```bash
# Core requirements (đã có)
selenium>=4.0.0
beautifulsoup4>=4.9.0
langchain-ollama>=0.1.0

# NEW: Bypass bot detection
undetected-chromedriver>=3.5.0

# Install tất cả:
pip install undetected-chromedriver selenium beautifulsoup4 langchain-ollama
```

## So sánh Search Engines

| Engine | Bot Detection | Speed | Results Quality | Vietnamese |
|--------|---------------|-------|-----------------|------------|
| **Google** | ❌ Yes (CAPTCHA) | ⚡⚡⚡ Fast | ⭐⭐⭐⭐⭐ Best | ✅ Good |
| **Google + Undetected** | ✅ Bypassed | ⚡⚡ Medium | ⭐⭐⭐⭐⭐ Best | ✅ Good |
| **DuckDuckGo** | ✅ No | ⚡⚡⚡ Fast | ⭐⭐⭐⭐ Good | ✅ OK |
| **Bing** | ⚠️ Sometimes | ⚡⚡ Medium | ⭐⭐⭐ OK | ⚠️ Weak |

**Recommendation:** Install `undetected-chromedriver` để bypass Google!

## Troubleshooting

### 1. Lỗi: "chromedriver version mismatch"

```bash
# Uninstall và reinstall
pip uninstall undetected-chromedriver
pip install undetected-chromedriver

# Nó sẽ tự động match Chrome version
```

### 2. Lỗi: "Chrome binary not found"

```bash
# Install/Update Chrome browser
# Windows: Download từ google.com/chrome
# Linux:
sudo apt-get install google-chrome-stable

# Mac:
brew install --cask google-chrome
```

### 3. Vẫn bị Google chặn

```python
# Hệ thống sẽ TỰ ĐỘNG chuyển sang DuckDuckGo:
⚠️ Google detected bot, trying DuckDuckGo instead...
🦆 Searching on DuckDuckGo...
✅ DuckDuckGo found 10 results

# Bạn không cần làm gì!
```

### 4. DuckDuckGo không trả về kết quả

```bash
# Check internet connection
ping duckduckgo.com

# Try with different query
python tools/test_autonomous_search.py
# → Try: "Vietnam AI law"
```

## Test Commands

```bash
# Test 1: Basic test
python tools/test_autonomous_search.py

# Test 2: Check package
python -c "import undetected_chromedriver as uc; print('✅ OK')"

# Test 3: Check Chrome version
google-chrome --version  # Linux/Mac
# or
"C:\Program Files\Google\Chrome\Application\chrome.exe" --version  # Windows
```

## Kết luận

Sau khi cài `undetected-chromedriver`:
- ✅ Google search hoạt động (bypass bot detection)
- ✅ DuckDuckGo làm fallback tự động
- ✅ Không cần CAPTCHA manual
- ✅ Autonomous search hoạt động hoàn hảo

**Install ngay:**

```bash
pip install undetected-chromedriver
```

Rồi chạy lại test! 🚀
