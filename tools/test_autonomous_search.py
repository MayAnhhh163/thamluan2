"""
Test script cho Ollama Autonomous Search Agent
"""

import logging
import asyncio
from tools.ollama_autonomous_search import ollama_autonomous_search_agent

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def test_autonomous_search():
    """Test autonomous search với topic cụ thể"""
    
    print("\n" + "=" * 80)
    print("🤖 TESTING OLLAMA AUTONOMOUS SEARCH AGENT")
    print("=" * 80)
    print("\nĐây là demo AI tự động:")
    print("1. Sinh search queries bằng Ollama")
    print("2. Search trên Google Chrome")
    print("3. Đánh giá kết quả bằng Ollama")
    print("4. Crawl các trang relevant")
    print("5. Phân tích chất lượng bằng Ollama")
    print("6. Chỉ lưu opinions chất lượng cao")
    print("\n" + "=" * 80)
    
    # Topic để test
    topic = "Luật Trí tuệ nhân tạo ý kiến chuyên gia"
    
    print(f"\n📋 Topic: {topic}")
    print("⏳ Starting autonomous search... (Có thể mất 3-5 phút)")
    print("💡 Chrome sẽ tự động mở và bạn sẽ thấy AI làm việc\n")
    
    # Run autonomous search
    result = ollama_autonomous_search_agent.autonomous_search_and_crawl(
        topic=topic,
        max_articles=10,  # Chỉ lấy 10 bài để test nhanh
        max_search_pages=2,
        quality_threshold=0.6
    )
    
    print("\n" + "=" * 80)
    
    if result.success:
        opinions = result.data['opinions']
        
        print("✅ TEST SUCCESSFUL!")
        print(f"\n📊 RESULTS:")
        print(f"   Collected: {len(opinions)} high-quality opinions")
        print(f"   Average quality: {result.data['average_quality']:.2f}")
        print(f"   Visited URLs: {result.data['visited_urls']}")
        print(f"   Sources: {result.data['sources']}")
        print(f"   Sentiments: {result.data.get('sentiments', {})}")
        print(f"   Stances: {result.data.get('stances', {})}")
        
        csv_path = result.data.get('csv_path')
        if csv_path:
            print(f"\n💾 EXPORTED TO CSV:")
            print(f"   {csv_path}")
        
        print(f"\n📰 OPINIONS SUMMARY:")
        for i, op in enumerate(opinions, 1):
            print(f"\n{i}. {op['title'][:70]}...")
            print(f"   URL: {op['url']}")
            print(f"   Source: {op['source']}")
            print(f"   Quality: {op['quality_score']:.2f}")
            print(f"   😊 Sentiment: {op.get('sentiment', 'N/A')}")
            print(f"   📊 Stance: {op.get('stance', 'N/A')} (confidence: {op.get('stance_confidence', 0):.2f})")
            print(f"   Feedback: {op['quality_feedback'][:80]}...")
            if op.get('key_points'):
                print(f"   💡 Key points: {', '.join(op['key_points'][:2])}")
    else:
        print(f"❌ TEST FAILED: {result.error}")
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    print("\n🚀 Starting Autonomous Search Test...")
    print("\n⚠️  Requirements:")
    print("   1. Ollama đã cài đặt và running (ollama serve)")
    print("   2. Model llama3.1:8b đã pull (ollama pull llama3.1:8b)")
    print("   3. Chrome browser đã cài đặt")
    print("   4. Internet connection")
    print("   5. ⭐ RECOMMENDED: pip install undetected-chromedriver (bypass Google bot)")
    
    print("\n💡 Tip: Nếu Google chặn bot, hệ thống sẽ tự động dùng DuckDuckGo")
    print("   Nhưng tốt nhất là cài: pip install undetected-chromedriver\n")
    
    input("✋ Press Enter to continue...")
    
    test_autonomous_search()
    
    print("\n🎉 Test complete!")
    print("\n📖 If you got 0 results and saw Google CAPTCHA:")
    print("   → Install: pip install undetected-chromedriver")
    print("   → Read: INSTALL_AUTONOMOUS.md for details")
