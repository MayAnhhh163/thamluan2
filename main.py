"""
Main.py - Entry point for AUTONOMOUS AI Agent System
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from core.config import config
from core.workflow import run_autonomous_workflow
from utils.logging import setup_logging
from utils.cli import parse_arguments


def main():
    """Main function"""

    # Setup logging
    logger = setup_logging()

    logger.info("=" * 80)
    logger.info("🤖 AUTONOMOUS AI AGENT SYSTEM - LangGraph")
    logger.info("=" * 80)
    logger.info("Full AI-powered workflow:")
    logger.info("  1. AI tìm và download PDF văn bản luật")
    logger.info("  2. AI extract PDF và tạo keywords")
    logger.info("  3. AI search + crawl + analyze opinions")
    logger.info("=" * 80)

    # Parse arguments
    args = parse_arguments()

    # Display configuration if requested
    if args.show_config:
        config.display_config()
        return

    # Validate configuration
    if not config.validate_config():
        logger.error("Configuration validation failed. Please check your setup.")
        return

    # Get project name
    project_name = args.project or input("\n📋 Nhập tên dự luật/chủ đề: ").strip()
    
    if not project_name:
        logger.error("❌ Project name is required!")
        return

    logger.info(f"Topic/Project: {project_name}")
    
    # Get configuration
    max_opinions_input = input("   Số opinions tối đa [20]: ").strip()
    max_opinions = int(max_opinions_input) if max_opinions_input else 20
    
    threshold_input = input("   Quality threshold (0-1) [0.6]: ").strip()
    quality_threshold = float(threshold_input) if threshold_input else 0.6
    
    logger.info(f"Max Opinions: {max_opinions}")
    logger.info(f"Quality Threshold: {quality_threshold}")

    try:
        # Run autonomous workflow
        logger.info("\n🚀 Starting AUTONOMOUS workflow...")
        final_state = asyncio.run(run_autonomous_workflow(
            project_name=project_name,
            max_opinions=max_opinions,
            quality_threshold=quality_threshold
        ))

        # Display results
        logger.info("\n" + "=" * 80)
        logger.info("✅ Workflow completed successfully!")
        logger.info("=" * 80)

        # Show results
        law_docs_count = len(final_state.get('law_documents', []))
        logger.info(f"\n📋 Law Documents Found: {law_docs_count}")
        logger.info(f"📄 PDF Downloaded: {'Yes' if final_state.get('pdf_local_path') else 'No'}")
        
        keywords_count = len(final_state.get('search_queries', []))
        logger.info(f"🔑 Keywords Extracted: {keywords_count}")
        
        analyzed_count = len(final_state.get('analyzed_opinions', []))
        logger.info(f"💬 Opinions Analyzed: {analyzed_count}")
        
        if final_state.get('csv_output_path'):
            logger.info(f"\n💾 CSV Output: {final_state['csv_output_path']}")
            logger.info("📖 Open this file in Excel to view results!")

        # Show errors if any
        errors = final_state.get('errors', [])
        if errors:
            logger.warning(f"\n⚠️  Errors encountered: {len(errors)}")
            for error in errors[:5]:  # Show first 5 errors
                logger.warning(f"  - {error.get('message')}")

        logger.info("\n" + "=" * 80)

    except KeyboardInterrupt:
        logger.info("\n⚠️  Workflow interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"\n❌ Workflow failed: {str(e)}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
