# Autonomous AI Agent Workflow - LangGraph Integration

## Overview

The autonomous workflow has been fully integrated into the LangGraph AI Agent framework. The AI now automatically handles the entire process from finding law documents to analyzing opinions.

## Workflow Types

### 1. **AUTONOMOUS Workflow** (Recommended - 3 Steps)
Full AI-powered workflow that handles everything automatically:

1. **AUTONOMOUS_LAW_SEARCH**: AI tìm và download PDF văn bản luật
2. **AUTONOMOUS_PDF_ANALYSIS**: AI extract PDF và tạo keywords  
3. **AUTONOMOUS_OPINION_SEARCH**: AI search + crawl + analyze opinions + export

### 2. **HYBRID Workflow** (8 Steps)
More control over each step, suitable for advanced users.

## Quick Start - Autonomous Workflow

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Make sure Ollama is running
ollama serve

# Pull required model (if not already)
ollama pull llama3.2:3b
```

### Basic Usage

```python
import asyncio
from core.auto import run_workflow_async

async def main():
    # Simple autonomous workflow - just provide topic
    result = await run_workflow_async(
        project_name="Luật Trí tuệ nhân tạo 2025",
        workflow_type='autonomous',  # This is default
        max_opinions=20,
        quality_threshold=0.6
    )
    
    print(f"✅ Workflow complete!")
    print(f"CSV exported to: {result.get('csv_output_path')}")

if __name__ == "__main__":
    asyncio.run(main())
```

### Configuration Options

The autonomous workflow accepts these parameters:

- `project_name` (required): Tên dự luật/chủ đề
- `workflow_type` (optional): `'autonomous'` (default) hoặc `'hybrid'`
- `max_opinions` (optional): Số opinions tối đa (default: 20)
- `quality_threshold` (optional): Ngưỡng chất lượng 0-1 (default: 0.6)

### Example: Main Script

Create `main.py`:

```python
import asyncio
import logging
from core.auto import run_workflow_async

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

async def main():
    """
    Run autonomous AI workflow
    """
    print("\n" + "=" * 80)
    print("🤖 AUTONOMOUS AI WORKFLOW")
    print("=" * 80)
    
    # Get topic from user
    topic = input("\n📋 Nhập chủ đề/tên dự luật: ").strip()
    
    if not topic:
        print("❌ Vui lòng nhập topic!")
        return
    
    # Configuration
    max_opinions = int(input("   Số opinions tối đa [20]: ").strip() or "20")
    quality_threshold = float(input("   Quality threshold (0-1) [0.6]: ").strip() or "0.6")
    
    print("\n" + "=" * 80)
    print("🚀 STARTING AUTONOMOUS WORKFLOW...")
    print("=" * 80)
    print(f"\n📊 Config:")
    print(f"   Topic: {topic}")
    print(f"   Max opinions: {max_opinions}")
    print(f"   Quality threshold: {quality_threshold}")
    print(f"\n⏳ This may take 10-15 minutes...")
    
    # Run workflow
    result = await run_workflow_async(
        project_name=topic,
        workflow_type='autonomous',
        max_opinions=max_opinions,
        quality_threshold=quality_threshold
    )
    
    # Display results
    print("\n" + "=" * 80)
    print("📊 WORKFLOW COMPLETE")
    print("=" * 80)
    
    print(f"\n✅ SUCCESS!")
    print(f"\n📋 Law Documents: {len(result.get('law_documents', []))}")
    print(f"📄 PDF Downloaded: {result.get('pdf_local_path') is not None}")
    print(f"🔍 Opinions Collected: {len(result.get('analyzed_opinions', []))}")
    
    csv_path = result.get('csv_output_path')
    if csv_path:
        print(f"\n💾 Results exported to:")
        print(f"   {csv_path}")
        print(f"\n📖 Open this file in Excel to view results!")
    
    print("\n" + "=" * 80)
    print("✅ ALL DONE!")
    print("=" * 80)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Workflow interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
```

Run it:

```bash
python main.py
```

## Architecture

### LangGraph Agents

The autonomous workflow uses 3 specialized agents:

1. **AutonomousLawSearchAgent** (`agents/autonomous_agents.py`)
   - Tìm văn bản luật trên duthaoonline
   - AI đánh giá và chọn document tốt nhất
   - Download PDF tự động

2. **AutonomousPdfAnalysisAgent** (`agents/autonomous_agents.py`)
   - Extract nội dung từ PDF
   - AI extract keywords quan trọng
   - Chuẩn bị keywords cho search opinions

3. **AutonomousOpinionSearchAgent** (`agents/autonomous_agents.py`)
   - AI sinh search queries tự động
   - Search Google/DuckDuckGo với Selenium
   - AI đánh giá relevance của mỗi kết quả
   - Crawl nội dung từ URLs relevant
   - AI đánh giá chất lượng nội dung
   - Phân tích sentiment và stance
   - Export CSV tự động

### Manager Orchestration

The `ManagerAgent` (`agents/manager.py`) automatically:
- Detects workflow type (autonomous vs hybrid)
- Routes tasks to appropriate agents
- Monitors progress
- Handles errors gracefully
- Generates final report

## Features

### AI-Powered Capabilities

✅ **Intelligent Document Search**: AI selects most relevant law documents  
✅ **Smart Keyword Extraction**: AI extracts key concepts from PDFs  
✅ **Autonomous Search**: AI generates diverse search queries  
✅ **DuckDuckGo Search**: Uses DuckDuckGo for reliable, bot-friendly search  
✅ **Quality Assessment**: AI evaluates content quality before saving  
✅ **Sentiment Analysis**: Automatic sentiment detection  
✅ **Stance Detection**: Identifies support/oppose/neutral stances  

### Output

The workflow produces a CSV file with:
- Title, URL, Source
- Quality score (0-1)
- Sentiment (positive/negative/neutral)
- Stance (support/oppose/neutral) + confidence
- Support/oppose scores
- Relevance level
- Quality feedback
- Key points
- Content preview

## Troubleshooting

### Ollama Not Running

```bash
# Start Ollama server
ollama serve

# In another terminal, check models
ollama list

# Pull model if needed
ollama pull llama3.2:3b
```

### Chrome Driver Issues

```bash
# Install undetected-chromedriver
pip install undetected-chromedriver

# If still issues, install regular Chrome
# Ubuntu/Debian:
sudo apt-get install chromium-browser chromium-chromedriver
```

### Search Engine

The workflow uses DuckDuckGo for reliable search without bot detection issues.

## Advanced Usage

### Use Hybrid Workflow

```python
result = await run_workflow_async(
    project_name="Luật Trí tuệ nhân tạo 2025",
    workflow_type='hybrid',  # More control
    target_url="https://example.com/draft-law"  # Optional reference
)
```

### Custom Configuration

```python
from core.types import create_initial_state
from core.auto import create_workflow

# Create custom state
state = create_initial_state(
    project_name="My Topic",
    workflow_type='autonomous',
    max_opinions=50,  # More opinions
    quality_threshold=0.8  # Higher quality threshold
)

# Run workflow
workflow = create_workflow()
app = workflow.compile()
final_state = await app.ainvoke(state)
```

## Migration from Old Autonomous Workflow

If you were using `main_autonomous.py`, the new integrated workflow is simpler:

**Old:**
```python
from tools.ollama_full_autonomous_workflow import ollama_full_autonomous_workflow

result = ollama_full_autonomous_workflow.run_full_workflow(
    topic="Luật AI",
    max_opinions=20,
    quality_threshold=0.6
)
```

**New:**
```python
from core.auto import run_workflow_async

result = await run_workflow_async(
    project_name="Luật AI",
    max_opinions=20,
    quality_threshold=0.6
)
```

Benefits of new approach:
- ✅ Standard LangGraph framework
- ✅ Better error handling
- ✅ State management
- ✅ Async support
- ✅ Easier to extend
- ✅ Better logging and monitoring

## Support

For issues or questions:
1. Check logs in `logs/` directory
2. Enable debug mode: `logging.basicConfig(level=logging.DEBUG)`
3. Review error messages in state: `result.get('errors', [])`
