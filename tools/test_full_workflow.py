"""
Test Full AI Autonomous Workflow - Từ PDF đến Opinion Analysis
"""

import logging
from tools.ollama_full_autonomous_workflow import ollama_full_autonomous_workflow

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def test_full_workflow():
    """Test full autonomous workflow"""
    
    print("\n" + "=" * 80)
    print("🤖 TESTING FULL AI AUTONOMOUS WORKFLOW")
    print("=" * 80)
    print("\nAI sẽ tự động xử lý TỒN BỘ workflow:")
    print("\n📋 PHASE 1: AI tìm và crawl PDF văn bản luật chính thức")
    print("   - Tìm trên duthaoonline.quochoi.vn")
    print("   - AI đánh giá document nào tốt nhất")
    print("   - Download PDF")
    
    print("\n📄 PHASE 2: AI extract và phân tích PDF")
    print("   - Extract nội dung PDF")
    print("   - AI extract keywords quan trọng")
    
    print("\n🔍 PHASE 3: AI autonomous search opinions")
    print("   - AI sinh search queries từ keywords")
    print("   - Tự động search & crawl opinions")
    print("   - AI phân tích sentiment & stance")
    print("   - Export CSV đầy đủ")
    
    print("\n" + "=" * 80)
    
    # Topic để test
    topic = "Luật Trí tuệ nhân tạo"
    
    print(f"\n📋 Topic: {topic}")
    print("⏳ Starting full workflow... (Có thể mất 5-10 phút)")
    print("💡 Bạn sẽ thấy AI làm việc từng bước\n")
    
    # Run full workflow
    result = ollama_full_autonomous_workflow.run_full_workflow(
        topic=topic,
        max_opinions=10,  # Test với 10 opinions
        quality_threshold=0.6
    )
    
    print("\n" + "=" * 80)
    
    if result.success:
        data = result.data
        
        print("✅ FULL WORKFLOW SUCCESSFUL!")
        
        print(f"\n📊 RESULTS SUMMARY:")
        print("=" * 80)
        
        print(f"\n📋 PHASE 1 - Văn bản luật:")
        print(f"   Documents found: {len(data.get('law_documents', []))}")
        if data.get('law_documents'):
            for i, doc in enumerate(data['law_documents'][:3], 1):
                print(f"   {i}. {doc['title'][:70]}...")
        print(f"   PDF downloaded: {'✅ Yes' if data.get('pdf_downloaded') else '❌ No'}")
        
        print(f"\n📄 PHASE 2 - PDF Analysis:")
        keywords = data.get('keywords', [])
        print(f"   Keywords extracted: {len(keywords)}")
        if keywords:
            print(f"   Top keywords: {', '.join(keywords[:10])}")
        
        print(f"\n🔍 PHASE 3 - Opinion Mining:")
        opinions = data.get('opinions', [])
        print(f"   Opinions collected: {len(opinions)}")
        
        sentiments = data.get('sentiments', {})
        if sentiments:
            print(f"   😊 Sentiments:")
            for sent, count in sentiments.items():
                print(f"      {sent}: {count}")
        
        stances = data.get('stances', {})
        if stances:
            print(f"   📊 Stances:")
            for stance, count in stances.items():
                print(f"      {stance}: {count}")
        
        csv_path = data.get('csv_path')
        if csv_path:
            print(f"\n💾 RESULTS EXPORTED:")
            print(f"   {csv_path}")
        
        print(f"\n📰 SAMPLE OPINIONS:")
        for i, op in enumerate(opinions[:3], 1):
            print(f"\n{i}. {op['title'][:70]}...")
            print(f"   Quality: {op.get('quality_score', 0):.2f}")
            print(f"   Sentiment: {op.get('sentiment', 'N/A')}")
            print(f"   Stance: {op.get('stance', 'N/A')}")
            print(f"   Source: {op.get('source', 'N/A')}")
        
    else:
        print(f"❌ WORKFLOW FAILED: {result.error}")
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    print("\n🚀 Starting Full AI Autonomous Workflow Test...")
    
    print("\n⚠️  Requirements:")
    print("   1. Ollama running (ollama serve)")
    print("   2. Model llama3.1:8b pulled")
    print("   3. Chrome browser installed")
    print("   4. undetected-chromedriver installed (pip install undetected-chromedriver)")
    print("   5. Internet connection")
    print("   6. ~10-15 minutes for full workflow")
    
    print("\n💡 This will run FULL workflow:")
    print("   PDF Law Search → PDF Extract → Opinion Search → Analysis → Export")
    
    input("\n✋ Press Enter to continue...")
    
    test_full_workflow()
    
    print("\n🎉 Test complete!")
    print("\n📖 Next steps:")
    print("   1. Check the CSV file exported")
    print("   2. Review PDF extracted keywords")
    print("   3. Analyze sentiment/stance distributions")
