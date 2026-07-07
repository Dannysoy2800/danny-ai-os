# Danny AI OS

A modular personal AI operating system built with Python + LangGraph.

## Structure
- system/ - master system prompt (single source of truth)
- agents/ - agent definitions (deltas only)
- policies/ - memory and tool policies
- workflows/ - reusable task workflows
- docs/ - documentation and status

## Agents
Manager, Research, Coding, Writing, Review.

## Run
python app.py

## Rules
1. Precedence: Safety > Core > Agent > Task > Memory
2. Agents add capabilities, never override the core
3. Runtime data (logs, memory) stays out of version control
