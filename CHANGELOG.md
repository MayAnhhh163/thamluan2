# Changelog

## [Latest] - 2025-10-15

### Changed
- **Search Engine**: Switched from Google to DuckDuckGo for all autonomous searches
  - Removed Google search functionality to avoid bot detection issues
  - DuckDuckGo provides more reliable results without CAPTCHA
  - Simplified codebase by removing fallback logic
  - No more bot detection bypass needed

### Benefits
- ✅ More reliable search results
- ✅ No CAPTCHA interruptions
- ✅ Simpler, cleaner code
- ✅ Faster search execution
- ✅ Better privacy

## [2025-10-15] - Autonomous Flow Refactoring

### Added
- Integrated autonomous workflow into LangGraph AI Agent framework
- Created 3 specialized autonomous agents:
  - `AutonomousLawSearchAgent`
  - `AutonomousPdfAnalysisAgent`
  - `AutonomousOpinionSearchAgent`
- Added workflow type selection (autonomous vs hybrid)
- Created `README_AUTONOMOUS.md` documentation
- Created `REFACTORING_SUMMARY.md`

### Changed
- Moved autonomous logic from standalone scripts to LangGraph agents
- Updated `main.py` to support both workflow types
- Merged `requirements_autonomous.txt` into `requirements.txt`
- Updated `core/auto.py` with autonomous workflow support
- Enhanced `agents/manager.py` with autonomous orchestration

### Removed
- Deleted `main_autonomous.py`
- Deleted `tools/ollama_full_autonomous_workflow.py`
- Deleted `agents/autonomous_opinion_agent.py`
- Deleted 6 autonomous documentation files
- Deleted 2 test files
- Removed `requirements_autonomous.txt`

### Fixed
- Improved error handling with LangGraph
- Better state management across agents
- More consistent logging

## Previous Versions

See git history for earlier changes.
