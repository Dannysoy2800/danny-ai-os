# 🧠 Danny AI OS

> **Modular personal AI operating system** powered by Python + LangGraph

A sophisticated multi-agent AI system with state-based orchestration, safety-first architecture, and pluggable agent/policy systems.

## ✨ Key Features

- **Multi-Agent Architecture**: Manager, Research, Coding, Writing, Review agents
- **State-Based Workflows**: LangGraph powered orchestration
- **Safety-First Design**: Precedence: Safety > Core > Agent > Task > Memory
- **Pluggable System**: Add agents and policies without overriding core
- **Production-Ready**: Async support, comprehensive logging, error handling

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- pip or uv

### Installation

```bash
# Clone the repository
git clone https://github.com/Dannysoy2800/danny-ai-os.git
cd danny-ai-os

# Install dependencies
pip install -r requirements.txt

# (Optional) Setup environment
cp .env.example .env
# Edit .env with your API keys
```

### Run the System

```bash
# Run the basic demo
python app.py

# Or use the Makefile
make run
```

## 📐 Architecture

```
danny-ai-os/
├── system/          Master system prompt (single source of truth)
├── agents/          Agent definitions (delta-based only)
├── policies/        Memory & tool policies
├── workflows/       Reusable task workflows
├── docs/            Documentation & guides
├── app.py           Entry point
├── requirements.txt Dependencies
└── Makefile         Development utilities
```

### How It Works

1. **System Prompt** (`system/`) defines core behavior and constraints
2. **Agents** (`agents/`) add specialized capabilities as deltas
3. **Policies** (`policies/`) manage memory, tools, and rate limits
4. **Workflows** (`workflows/`) orchestrate multi-step tasks
5. **LangGraph** coordinates execution with state management

## 🛠️ Development

### Setup Development Environment

```bash
# Install with development dependencies
make install-dev

# Run tests
make test

# Format code
make format

# Check code quality
make lint
```

### Project Rules

1. **Precedence**: Safety > Core > Agent > Task > Memory
2. **Agents add capabilities**, never override the core system
3. **Runtime data** (logs, memory) stays out of version control
4. Follow [CONTRIBUTING.md](CONTRIBUTING.md) for PRs

## 📚 Documentation

- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Contribution guidelines & standards
- **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)** - Deep dive into system design
- **[docs/AGENTS.md](docs/AGENTS.md)** - Agent development guide
- **[docs/API.md](docs/API.md)** - API reference

## 🔐 Safety & Security

- Commit signing required (`git commit -S`)
- Dependency scanning with Dependabot
- No secrets in version control (use `.env`)
- Regular security audits via CI/CD

## 📦 Dependencies

### Core
- **langgraph** - State graph orchestration
- **langchain** - LLM framework
- **openai** - OpenAI API client
- **pydantic** - Data validation

### Data
- **pandas** - Data manipulation
- **numpy** - Numerical computing

### Utilities
- **python-dotenv** - Environment management
- **pyyaml** - Configuration files
- **colorlog** - Enhanced logging

See [requirements.txt](requirements.txt) for full list.

## 🤝 Contributing

We welcome contributions! Please:

1. Read [CONTRIBUTING.md](CONTRIBUTING.md)
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit with sign-off: `git commit -S -m "feat: description"`
4. Push and open a PR

## 📋 Roadmap

- [ ] Multi-turn conversation memory
- [ ] Tool calling system
- [ ] Persistent knowledge base
- [ ] Production deployment guide
- [ ] Docker support

## 📄 License

MIT License - see [LICENSE.md](LICENSE.md)

## 👤 Author

**Dannysoy2800** - [GitHub](https://github.com/Dannysoy2800)

---

**Questions?** Open an [issue](https://github.com/Dannysoy2800/danny-ai-os/issues) or check the [docs](docs/).
