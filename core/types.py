"""
Types for the AutoData package.
Định nghĩa các types cho state management và message passing.
"""

from typing import TypedDict, List, Dict, Optional, Annotated, Any
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime


class AgentRole(str, Enum):
    """Agent roles in AUTONOMOUS AI system"""
    MANAGER = "manager"
    WEB_CRAWLER = "web_crawler"  # Used by autonomous agents
    CONTENT_EXTRACTOR = "content_extractor"  # Used by autonomous agents
    SEARCH_AGENT = "search_agent"  # Used by autonomous agents


class TaskStatus(str, Enum):
    """Trạng thái của task"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


class TaskType(str, Enum):
    """Task types for AUTONOMOUS AI-powered workflow"""
    # AUTONOMOUS WORKFLOW (3 steps)
    AUTONOMOUS_LAW_SEARCH = "autonomous_law_search"  # AI tự động tìm và download PDF luật
    AUTONOMOUS_PDF_ANALYSIS = "autonomous_pdf_analysis"  # AI extract PDF và tạo keywords
    AUTONOMOUS_OPINION_SEARCH = "autonomous_opinion_search"  # AI tự động search + crawl + analyze opinions


@dataclass
class Task:
    """Đại diện cho một task cần thực hiện"""
    task_id: str
    task_type: TaskType
    status: TaskStatus = TaskStatus.PENDING
    assigned_to: Optional[AgentRole] = None
    input_data: Dict[str, Any] = field(default_factory=dict)
    output_data: Dict[str, Any] = field(default_factory=dict)
    error_message: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None

    def to_dict(self) -> Dict:
        return {
            "task_id": self.task_id,
            "task_type": self.task_type.value,
            "status": self.status.value,
            "assigned_to": self.assigned_to.value if self.assigned_to else None,
            "input_data": self.input_data,
            "output_data": self.output_data,
            "error_message": self.error_message,
            "created_at": self.created_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None
        }


@dataclass
class PDFDocument:
    """Thông tin về PDF document"""
    url: str
    local_path: Optional[str] = None
    title: Optional[str] = None
    content: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    page_count: int = 0
    file_size: Optional[int] = None


@dataclass
class ExtractedKeywords:
    """Keywords được trích xuất từ PDF"""
    main_keywords: List[str] = field(default_factory=list)
    entities: List[str] = field(default_factory=list)
    key_phrases: List[str] = field(default_factory=list)
    summary: Optional[str] = None


@dataclass
class Comment:
    """Đại diện cho một comment/ý kiến"""
    source: str  # Facebook, forum, news site, etc.
    source_url: str
    author: Optional[str] = None
    content: str = ""
    timestamp: Optional[datetime] = None
    likes: int = 0
    replies: int = 0
    sentiment: Optional[str] = None  # Để mở rộng cho phân tích cảm xúc
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        return {
            "source": self.source,
            "source_url": self.source_url,
            "author": self.author,
            "content": self.content,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "likes": self.likes,
            "replies": self.replies,
            "sentiment": self.sentiment,
            "metadata": self.metadata
        }


class AgentState(TypedDict):
    """
    State for LangGraph AI Agent workflow.
    Optimized for AUTONOMOUS workflow only.
    """
    # Input configuration
    project_name: str  # Tên dự án/chủ đề (BẮT BUỘC)
    max_opinions: int  # Số opinions tối đa
    quality_threshold: float  # Ngưỡng chất lượng (0-1)

    # Workflow tracking
    current_task: Optional[Task]
    task_history: Annotated[List[Task], "History of all tasks"]
    current_agent: Optional[AgentRole]

    # Phase 1: Law document search
    law_documents: Annotated[List[Dict[str, Any]], "Law documents found"]
    pdf_local_path: Optional[str]  # Downloaded PDF path

    # Phase 2: PDF analysis
    search_queries: List[str]  # Keywords extracted from PDF

    # Phase 3: Opinion collection
    analyzed_opinions: Annotated[List[Dict[str, Any]], "Opinions with NLP analysis"]

    # Output
    csv_output_path: Optional[str]

    # Error handling
    errors: Annotated[List[Dict[str, Any]], "Error log"]
    warnings: Annotated[List[str], "Warning messages"]

    # Metadata
    started_at: datetime
    last_updated: datetime
    is_complete: bool


@dataclass
class AgentMessage:
    """Message format để agents communicate"""
    from_agent: AgentRole
    to_agent: Optional[AgentRole]
    message_type: str  # "task_request", "task_complete", "error", "info"
    content: Dict[str, Any]
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class ToolResult:
    """Kết quả trả về từ tool execution"""
    success: bool
    data: Any = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    message: Optional[str] = None  # thêm trường này


    def to_dict(self) -> Dict:
        return {
            "success": self.success,
            "data": self.data,
            "error": self.error,
            "metadata": self.metadata
        }


# Helper functions
def create_initial_state(
    project_name: str,
    max_opinions: int = 20,
    quality_threshold: float = 0.6
) -> AgentState:
    """Create initial state for AUTONOMOUS workflow"""
    now = datetime.now()
    return AgentState(
        project_name=project_name,
        max_opinions=max_opinions,
        quality_threshold=quality_threshold,
        current_task=None,
        task_history=[],
        current_agent=None,
        law_documents=[],
        pdf_local_path=None,
        search_queries=[],
        analyzed_opinions=[],
        csv_output_path=None,
        errors=[],
        warnings=[],
        started_at=now,
        last_updated=now,
        is_complete=False
    )


def update_state_task(state: AgentState, task: Task) -> AgentState:
    """Helper để update task trong state"""
    state["current_task"] = task
    state["task_history"].append(task)
    state["last_updated"] = datetime.now()
    return state