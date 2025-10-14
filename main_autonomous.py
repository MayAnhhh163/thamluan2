"""
Main Autonomous - Full AI Workflow chỉ cần nhập topic
"""

import logging
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from tools.ollama_full_autonomous_workflow import ollama_full_autonomous_workflow

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/autonomous_workflow.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def main():
    """
    Main function - Chạy full AI autonomous workflow
    """
    print("\n" + "=" * 80)
    print("🤖 FULL AI AUTONOMOUS WORKFLOW")
    print("=" * 80)
    print("\nAI sẽ tự động xử lý TỒN BỘ từ đầu đến cuối:")
    print("\n1️⃣  AI tìm PDF văn bản luật chính thức")
    print("2️⃣  AI extract và phân tích PDF")
    print("3️⃣  AI autonomous search opinions")
    print("4️⃣  AI phân tích sentiment & stance")
    print("5️⃣  Export CSV đầy đủ")
    print("\n" + "=" * 80)

    # Input topic
    print("\n📋 Nhập chủ đề/tên dự luật:")
    topic = input("→ ").strip()

    if not topic:
        print("❌ Vui lòng nhập topic!")
        return

    print(f"\n✅ Topic: {topic}")

    # Configuration
    print("\n⚙️  Configuration (Enter để dùng mặc định):")

    max_opinions_input = input("   Số opinions tối đa [20]: ").strip()
    max_opinions = int(max_opinions_input) if max_opinions_input else 20

    threshold_input = input("   Quality threshold (0-1) [0.6]: ").strip()
    quality_threshold = float(threshold_input) if threshold_input else 0.6

    print("\n" + "=" * 80)
    print("🚀 STARTING FULL AI WORKFLOW...")
    print("=" * 80)
    print(f"\n📊 Config:")
    print(f"   Topic: {topic}")
    print(f"   Max opinions: {max_opinions}")
    print(f"   Quality threshold: {quality_threshold}")
    print(f"\n⏳ This may take 10-15 minutes...")
    print("💡 AI is working, please wait...\n")

    # Run workflow
    result = ollama_full_autonomous_workflow.run_full_workflow(
        topic=topic,
        max_opinions=max_opinions,
        quality_threshold=quality_threshold
    )

    print("\n" + "=" * 80)
    print("📊 WORKFLOW COMPLETE")
    print("=" * 80)

    if result.success:
        data = result.data

        print("\n✅ SUCCESS!")

        # Summary
        print(f"\n📋 Law Documents:")
        print(f"   Found: {len(data.get('law_documents', []))}")
        print(f"   PDF downloaded: {'Yes' if data.get('pdf_downloaded') else 'No'}")

        print(f"\n📄 PDF Analysis:")
        keywords = data.get('keywords', [])
        print(f"   Keywords: {len(keywords)}")
        if keywords:
            print(f"   → {', '.join(keywords[:8])}")

        print(f"\n🔍 Opinions:")
        opinions = data.get('opinions', [])
        print(f"   Collected: {len(opinions)}")

        sentiments = data.get('sentiments', {})
        if sentiments:
            print(f"   Sentiments: {sentiments}")

        stances = data.get('stances', {})
        if stances:
            print(f"   Stances: {stances}")

        csv_path = data.get('csv_path')
        if csv_path:
            print(f"\n💾 Results exported to:")
            print(f"   {csv_path}")
            print(f"\n📖 Open this file in Excel to view results!")

        print("\n" + "=" * 80)
        print("✅ ALL DONE!")
        print("=" * 80)

    else:
        print(f"\n❌ WORKFLOW FAILED:")
        print(f"   {result.error}")
        print("\n💡 Tips:")
        print("   1. Check if Ollama is running (ollama serve)")
        print("   2. Check internet connection")
        print("   3. Install undetected-chromedriver: pip install undetected-chromedriver")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Workflow interrupted by user")
    except Exception as e:
        logger.error(f"Main error: {str(e)}")
        print(f"\n❌ Error: {str(e)}")
