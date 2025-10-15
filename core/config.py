"""
Configuration for Autonomous AI Agent System.
Clean, minimal configuration for autonomous workflow only.
"""

import os
from pathlib import Path
from typing import Optional

# Load environment variables (optional)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv is optional


class Config:
    """Configuration class for AUTONOMOUS AI workflow"""

    # ========== Paths ==========
    BASE_DIR = Path(__file__).parent.parent
    DATA_DIR = BASE_DIR / "data"
    PDF_DIR = DATA_DIR / "pdfs"
    CSV_DIR = DATA_DIR / "csv"
    LOGS_DIR = BASE_DIR / "logs"

    # Create directories if not exist
    for dir_path in [DATA_DIR, PDF_DIR, CSV_DIR, LOGS_DIR]:
        dir_path.mkdir(parents=True, exist_ok=True)

    # ========== LLM Settings (Ollama) ==========
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    LLM_MODEL = os.getenv("LLM_MODEL", "llama3.2:3b")
    LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.3"))
    LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", "2048"))

    # ========== Web Scraping Settings ==========
    USER_AGENT = os.getenv(
        "USER_AGENT",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
    REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "30"))
    MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
    RETRY_DELAY = int(os.getenv("RETRY_DELAY", "2"))

    # Selenium settings
    SELENIUM_HEADLESS = os.getenv("SELENIUM_HEADLESS", "false").lower() == "true"
    SELENIUM_WAIT_TIME = int(os.getenv("SELENIUM_WAIT_TIME", "10"))

    # ========== PDF Processing Settings ==========
    PDF_MAX_SIZE_MB = int(os.getenv("PDF_MAX_SIZE_MB", "50"))
    
    # Keyword extraction settings
    MIN_KEYWORD_LENGTH = int(os.getenv("MIN_KEYWORD_LENGTH", "3"))
    MAX_KEYWORDS = int(os.getenv("MAX_KEYWORDS", "50"))
    MIN_KEYWORD_FREQUENCY = int(os.getenv("MIN_KEYWORD_FREQUENCY", "2"))
    
    # Vietnamese stopwords (common words to ignore)
    VIETNAMESE_STOPWORDS = set([
        "và", "của", "có", "các", "được", "là", "cho", "với", "để", "từ",
        "trong", "này", "đó", "hay", "hoặc", "nhưng", "vì", "nên", "thì",
        "đã", "sẽ", "bị", "bởi", "theo", "như", "về", "tại", "trên", "dưới",
        "một", "hai", "ba", "khi", "nếu", "mà", "cũng", "đều", "không", "chỉ"
    ])

    # ========== Logging Settings ==========
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = LOGS_DIR / "autodata.log"
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # ========== Autonomous Workflow Settings ==========
    DEFAULT_MAX_OPINIONS = int(os.getenv("DEFAULT_MAX_OPINIONS", "20"))
    DEFAULT_QUALITY_THRESHOLD = float(os.getenv("DEFAULT_QUALITY_THRESHOLD", "0.6"))
    
    # Law crawler settings
    LAW_CRAWLER_SOURCE = os.getenv("LAW_CRAWLER_SOURCE", "duthaoonline")
    LAW_SIMILARITY_THRESHOLD = float(os.getenv("LAW_SIMILARITY_THRESHOLD", "0.8"))

    @classmethod
    def validate_config(cls) -> bool:
        """Validate configuration settings"""
        try:
            # Check Ollama connection
            import requests
            response = requests.get(f"{cls.OLLAMA_BASE_URL}/api/tags", timeout=5)
            if response.status_code != 200:
                print(f"⚠️  Warning: Cannot connect to Ollama at {cls.OLLAMA_BASE_URL}")
                print("   Make sure Ollama is running: ollama serve")
                return False
            
            # Check required directories
            for dir_path in [cls.DATA_DIR, cls.PDF_DIR, cls.CSV_DIR, cls.LOGS_DIR]:
                if not dir_path.exists():
                    print(f"❌ Directory not found: {dir_path}")
                    return False
            
            return True
            
        except Exception as e:
            print(f"❌ Config validation error: {str(e)}")
            return False

    @classmethod
    def display_config(cls):
        """Display current configuration"""
        print("\n" + "=" * 60)
        print("⚙️  AUTONOMOUS AI AGENT - Configuration")
        print("=" * 60)
        
        print("\n📁 Paths:")
        print(f"  Base Dir: {cls.BASE_DIR}")
        print(f"  Data Dir: {cls.DATA_DIR}")
        print(f"  PDF Dir: {cls.PDF_DIR}")
        print(f"  CSV Dir: {cls.CSV_DIR}")
        print(f"  Logs Dir: {cls.LOGS_DIR}")
        
        print("\n🤖 LLM (Ollama):")
        print(f"  Base URL: {cls.OLLAMA_BASE_URL}")
        print(f"  Model: {cls.LLM_MODEL}")
        print(f"  Temperature: {cls.LLM_TEMPERATURE}")
        print(f"  Max Tokens: {cls.LLM_MAX_TOKENS}")
        
        print("\n🌐 Web Scraping:")
        print(f"  Timeout: {cls.REQUEST_TIMEOUT}s")
        print(f"  Max Retries: {cls.MAX_RETRIES}")
        print(f"  Selenium Headless: {cls.SELENIUM_HEADLESS}")
        
        print("\n📄 PDF Processing:")
        print(f"  Max Size: {cls.PDF_MAX_SIZE_MB}MB")
        
        print("\n🔍 Autonomous Workflow:")
        print(f"  Default Max Opinions: {cls.DEFAULT_MAX_OPINIONS}")
        print(f"  Default Quality Threshold: {cls.DEFAULT_QUALITY_THRESHOLD}")
        print(f"  Law Crawler Source: {cls.LAW_CRAWLER_SOURCE}")
        
        print("\n" + "=" * 60)


# Create singleton instance
config = Config()


# Export
__all__ = ['config', 'Config']
