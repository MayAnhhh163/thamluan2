# LangGraph AI Agent Structure

## 📁 Cấu trúc thư mục chuẩn

```
autonomous-ai-agent/
│
├── agents/                          # 🤖 LangGraph AI Agents
│   ├── __init__.py                 # Export agents
│   ├── base.py                     # BaseAgent class
│   ├── manager.py                  # Manager Agent (orchestrator)
│   └── autonomous_agents.py        # 3 autonomous agents
│       ├── AutonomousLawSearchAgent
│       ├── AutonomousPdfAnalysisAgent
│       └── AutonomousOpinionSearchAgent
│
├── core/                            # 🏗️ Core System
│   ├── __init__.py                 # Core exports
│   ├── config.py                   # Configuration management
│   ├── types.py                    # Type definitions (State, Tasks, etc.)
│   └── workflow.py                 # LangGraph workflow setup
│       ├── create_workflow()
│       └── run_autonomous_workflow()
│
├── tools/                           # 🔧 Tools for Agents
│   ├── __init__.py
│   ├── law_list_crawler.py        # Tìm văn bản luật
│   ├── pdf_downloader.py          # Download PDFs
│   ├── pdf_extractor.py           # Extract PDF content
│   ├── ollama_autonomous_search.py # Autonomous search engine
│   ├── nlp_analyzer.py            # NLP analysis (sentiment/stance)
│   └── [other tools...]
│
├── utils/                           # 🛠️ Utilities
│   ├── __init__.py
│   ├── logging.py                 # Logging setup
│   └── cli.py                     # CLI arguments
│
├── prompts/                         # 💬 LLM Prompts
│   ├── __init__.py
│   └── manager_system.md          # Manager system prompt
│
├── data/                            # 📦 Data Storage
│   ├── pdfs/                      # Downloaded PDFs
│   ├── csv/                       # CSV outputs
│   └── vector_db/                 # ChromaDB (if used)
│
├── logs/                            # 📝 Log Files
│   └── autodata.log
│
├── main.py                          # 🚀 Entry Point
├── requirements.txt                 # 📦 Dependencies
├── README.md                        # 📖 Main Documentation
├── README_AUTONOMOUS.md             # 📖 Autonomous Guide
└── LANGGRAPH_STRUCTURE.md           # 📖 This file
```

## 🎯 LangGraph Components

### 1. Agents (`agents/`)

#### BaseAgent (`agents/base.py`)
```python
class BaseAgent(ABC):
    """Base class for all LangGraph agents"""
    
    def __init__(self, role, name, description)
    
    @abstractmethod
    async def execute(self, state: AgentState) -> AgentState
    
    def create_task(...)
    def complete_task(...)
    def update_state(...)
    def log_error(...)
    async def call_llm(...)
```

#### ManagerAgent (`agents/manager.py`)
```python
class ManagerAgent(BaseAgent):
    """Orchestrates AUTONOMOUS workflow"""
    
    async def execute(self, state: AgentState) -> AgentState
    async def _start_workflow(...)
    async def _monitor_and_decide(...)
    def generate_report(...)
```

#### Autonomous Agents (`agents/autonomous_agents.py`)
```python
class AutonomousLawSearchAgent(BaseAgent):
    """Phase 1: Find and download law PDFs"""
    async def execute(self, state: AgentState) -> AgentState
    async def _ai_select_best_document(...)

class AutonomousPdfAnalysisAgent(BaseAgent):
    """Phase 2: Extract PDF and create keywords"""
    async def execute(self, state: AgentState) -> AgentState
    async def _ai_extract_keywords(...)

class AutonomousOpinionSearchAgent(BaseAgent):
    """Phase 3: Search, crawl, analyze opinions"""
    async def execute(self, state: AgentState) -> AgentState
```

### 2. Core (`core/`)

#### Types (`core/types.py`)
```python
# Enums
class AgentRole(str, Enum)
class TaskStatus(str, Enum)
class TaskType(str, Enum):
    AUTONOMOUS_LAW_SEARCH
    AUTONOMOUS_PDF_ANALYSIS
    AUTONOMOUS_OPINION_SEARCH

# Dataclasses
@dataclass
class Task

@dataclass
class ToolResult

# TypedDict
class AgentState(TypedDict):
    project_name: str
    max_opinions: int
    quality_threshold: float
    current_task: Optional[Task]
    task_history: List[Task]
    law_documents: List[Dict]
    pdf_local_path: Optional[str]
    search_queries: List[str]
    analyzed_opinions: List[Dict]
    csv_output_path: Optional[str]
    errors: List[Dict]
    warnings: List[str]
    started_at: datetime
    last_updated: datetime
    is_complete: bool

# Helpers
def create_initial_state(...)
def update_state_task(...)
```

#### Workflow (`core/workflow.py`)
```python
def create_workflow() -> StateGraph:
    """Create LangGraph workflow"""
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("manager", manager_agent.execute)
    workflow.add_node("autonomous_law_search", ...)
    workflow.add_node("autonomous_pdf_analysis", ...)
    workflow.add_node("autonomous_opinion_search", ...)
    
    # Add routing
    workflow.add_conditional_edges(...)
    
    return workflow

async def run_autonomous_workflow(...) -> Dict[str, Any]:
    """Run AUTONOMOUS workflow"""
    # Create initial state
    # Compile workflow
    # Execute
    # Return final state
```

#### Config (`core/config.py`)
```python
class Config:
    """Configuration management"""
    
    # LLM
    LLM_MODEL: str
    OLLAMA_BASE_URL: str
    
    # Directories
    DATA_DIR: str
    PDF_DIR: str
    CSV_DIR: str
    
    # Logging
    LOG_LEVEL: str
    LOG_FILE: str
```

### 3. Entry Point (`main.py`)

```python
def main():
    """Main entry point"""
    
    # Setup logging
    logger = setup_logging()
    
    # Parse arguments
    args = parse_arguments()
    
    # Get user input
    project_name = input(...)
    max_opinions = int(input(...))
    quality_threshold = float(input(...))
    
    # Run workflow
    final_state = asyncio.run(run_autonomous_workflow(
        project_name=project_name,
        max_opinions=max_opinions,
        quality_threshold=quality_threshold
    ))
    
    # Display results
    logger.info(f"Opinions: {len(final_state['analyzed_opinions'])}")
    logger.info(f"CSV: {final_state['csv_output_path']}")
```

## 🔄 LangGraph Workflow Flow

```
┌─────────────┐
│   START     │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────┐
│  MANAGER                             │
│  - Check if first task               │
│  - Create AUTONOMOUS_LAW_SEARCH task │
└──────┬──────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────┐
│  AUTONOMOUS_LAW_SEARCH               │
│  - Find law documents                │
│  - AI select best document           │
│  - Download PDF                      │
│  - Complete task                     │
└──────┬──────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────┐
│  MANAGER                             │
│  - Check completed tasks             │
│  - Create AUTONOMOUS_PDF_ANALYSIS    │
└──────┬──────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────┐
│  AUTONOMOUS_PDF_ANALYSIS             │
│  - Extract PDF content               │
│  - AI extract keywords               │
│  - Complete task                     │
└──────┬──────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────┐
│  MANAGER                             │
│  - Check completed tasks             │
│  - Create AUTONOMOUS_OPINION_SEARCH  │
└──────┬──────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────┐
│  AUTONOMOUS_OPINION_SEARCH           │
│  - AI generate search queries        │
│  - Search DuckDuckGo                 │
│  - AI evaluate each result           │
│  - Crawl relevant URLs               │
│  - AI assess quality                 │
│  - Analyze sentiment/stance          │
│  - Export CSV                        │
│  - Complete task                     │
└──────┬──────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────┐
│  MANAGER                             │
│  - Check all tasks completed         │
│  - Mark is_complete = True           │
└──────┬──────────────────────────────┘
       │
       ▼
┌─────────────┐
│     END     │
│  (Complete) │
└─────────────┘
```

## 📊 State Flow

```python
# Initial State
{
    'project_name': "Luật AI 2025",
    'max_opinions': 20,
    'quality_threshold': 0.6,
    'current_task': None,
    'task_history': [],
    'is_complete': False,
    ...
}

# After Phase 1
{
    'law_documents': [{'title': '...', 'url': '...'}],
    'pdf_local_path': 'data/pdfs/abc123.pdf',
    'current_task': Task(AUTONOMOUS_PDF_ANALYSIS),
    'task_history': [Task(AUTONOMOUS_LAW_SEARCH, COMPLETED)],
    ...
}

# After Phase 2
{
    'search_queries': ['keyword1', 'keyword2', ...],
    'current_task': Task(AUTONOMOUS_OPINION_SEARCH),
    'task_history': [
        Task(AUTONOMOUS_LAW_SEARCH, COMPLETED),
        Task(AUTONOMOUS_PDF_ANALYSIS, COMPLETED)
    ],
    ...
}

# Final State
{
    'analyzed_opinions': [
        {'title': '...', 'sentiment': 'positive', 'stance': 'support', ...},
        ...
    ],
    'csv_output_path': 'data/csv/autonomous_Luật_AI_2025.csv',
    'current_task': Task(AUTONOMOUS_OPINION_SEARCH, COMPLETED),
    'task_history': [all 3 tasks COMPLETED],
    'is_complete': True,
    ...
}
```

## ✅ LangGraph Best Practices

### 1. State Management
- ✅ Use TypedDict for AgentState
- ✅ Immutable updates (return new state)
- ✅ Clear state schema
- ✅ Document all fields

### 2. Agent Design
- ✅ Single responsibility per agent
- ✅ Inherit from BaseAgent
- ✅ Async execute method
- ✅ Clear error handling

### 3. Workflow Design
- ✅ Clear entry/exit points
- ✅ Conditional routing
- ✅ Loop prevention (recursion limit)
- ✅ Manager orchestration pattern

### 4. Error Handling
- ✅ Graceful degradation
- ✅ Error logging in state
- ✅ Continue on non-critical errors
- ✅ Clear error messages

### 5. Testing
- ✅ Unit tests for agents
- ✅ Integration tests for workflow
- ✅ Mock LLM calls for speed
- ✅ Test error scenarios

## 🚀 Usage Examples

### Basic Usage
```python
import asyncio
from core.workflow import run_autonomous_workflow

result = asyncio.run(run_autonomous_workflow(
    project_name="Luật AI",
    max_opinions=20,
    quality_threshold=0.6
))
```

### Advanced Usage
```python
from core.workflow import create_workflow
from core.types import create_initial_state

# Custom state
state = create_initial_state(
    project_name="Custom Topic",
    max_opinions=50,
    quality_threshold=0.8
)

# Custom workflow
workflow = create_workflow()
app = workflow.compile()

# Run with custom config
config = {"recursion_limit": 100}
final_state = await app.ainvoke(state, config=config)
```

## 📚 Additional Resources

- **LangGraph Docs**: https://python.langchain.com/docs/langgraph
- **Main README**: `README.md`
- **Autonomous Guide**: `README_AUTONOMOUS.md`
- **Changelog**: `CHANGELOG.md`

---

This structure follows LangGraph best practices for AI Agent systems.
