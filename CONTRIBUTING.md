# Contributing to Danny AI OS

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Follow the project rules and precedence model

## Our Philosophy

**Precedence: Safety > Core > Agent > Task > Memory**

- Agents *add* capabilities, they never override the core system
- Runtime data (logs, memory) stays out of version control
- All changes must maintain system stability and safety

## Getting Started

### Development Setup

```bash
# 1. Fork and clone
git clone https://github.com/YOUR_USERNAME/danny-ai-os.git
cd danny-ai-os

# 2. Install with development dependencies
pip install -r requirements.txt -r requirements-dev.txt

# 3. Setup pre-commit hooks
pre-commit install

# 4. Create a feature branch
git checkout -b feature/your-feature-name
```

### Required Tools

- Python 3.11+
- Git (with commit signing enabled)
- Make or equivalent

## Development Workflow

### 1. Making Changes

```bash
# Create feature branch
git checkout -b feature/descriptive-name

# Make your changes
# ... edit files ...

# Run formatting and linting
make format  # Black formatter
make lint    # Flake8 + mypy

# Run tests
make test
```

### 2. Commit Guidelines

We follow [Conventional Commits](https://www.conventionalcommits.org/):

```bash
# Format: type(scope): subject
git commit -S -m "feat(agents): add research agent capabilities"
git commit -S -m "fix(policies): correct memory retention logic"
git commit -S -m "docs: update architecture documentation"
git commit -S -m "test: add unit tests for workflow orchestration"
```

**Commit Types:**
- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation only
- `test` - Test additions/changes
- `refactor` - Code restructuring
- `perf` - Performance improvements
- `chore` - Build, deps, tooling

**Must use `-S` flag for commit signing!**

### 3. Testing

```bash
# Run all tests with coverage
make test

# Run specific test file
pytest tests/test_agents.py -v

# Run with coverage report
pytest --cov --cov-report=html
```

**Guidelines:**
- Write tests for all new features
- Maintain >80% code coverage
- Test edge cases and error paths
- Use descriptive test names

### 4. Code Quality

```bash
# Format code (Black)
make format

# Check formatting
black --check .

# Lint code (Flake8)
make lint

# Type check (mypy)
mypy .

# All-in-one
make quality
```

**Standards:**
- Follow PEP 8
- Use type hints for all functions
- Max line length: 100 characters
- Docstrings required for all modules/classes/functions

## File Structure for New Features

When adding new capabilities, follow this structure:

```
feature_name/
├── __init__.py
├── core.py           # Core logic
├── policies/         # Related policies
│   └── memory.yaml
└── tests/
    └── test_core.py
```

## Pull Request Process

### Before Opening PR

1. ✅ All tests pass: `make test`
2. ✅ Code is formatted: `make format`
3. ✅ Code is linted: `make lint`
4. ✅ Commits are signed: `git commit -S`
5. ✅ Branch is up to date: `git rebase main`

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation

## Related Issues
Closes #(issue number)

## Changes
- Change 1
- Change 2

## Testing
Describe how you tested this

## Checklist
- [ ] Tests pass
- [ ] Code formatted
- [ ] Documentation updated
- [ ] Commits signed
```

### Review Process

- Maintainers will review within 48 hours
- Feedback will be provided as comments
- Make requested changes and push updates
- Once approved, PR will be squash-merged

## Documentation

### When to Update Docs

- ✅ New features
- ✅ Changed behavior
- ✅ New configuration options
- ✅ Architecture changes

### Documentation Files

- **README.md** - Quick start and overview
- **docs/ARCHITECTURE.md** - System design
- **docs/AGENTS.md** - Agent development guide
- **docs/API.md** - API reference
- **docs/DEPLOYMENT.md** - Production setup
- **Docstrings** - Inline code documentation

### Documentation Style

```python
def orchestrate_agents(state: AgentState) -> AgentState:
    """
    Orchestrate multi-agent workflow execution.
    
    This function coordinates agent execution according to the
    state machine defined in workflows/. It respects the
    precedence hierarchy: Safety > Core > Agent > Task > Memory.
    
    Args:
        state: Current agent execution state
        
    Returns:
        Updated agent state after execution
        
    Raises:
        SafetyError: If safety policies are violated
        WorkflowError: If workflow orchestration fails
        
    Example:
        >>> state = {"task": "research", "input": "..."}
        >>> result = orchestrate_agents(state)
    """
```

## Common Issues & Solutions

### Issue: Tests fail locally but pass in CI

```bash
# Clear cache and reinstall
make clean
make install-dev
make test
```

### Issue: Pre-commit hooks failing

```bash
# Run formatters
make format

# Then commit again
git commit -S -m "your message"
```

### Issue: Merge conflicts

```bash
# Rebase on latest main
git fetch origin
git rebase origin/main

# Resolve conflicts in your editor
# Then:
git add .
git rebase --continue
```

## Asking Questions

- **Usage questions**: Open a [Discussion](https://github.com/Dannysoy2800/danny-ai-os/discussions)
- **Bug reports**: Open an [Issue](https://github.com/Dannysoy2800/danny-ai-os/issues)
- **Feature ideas**: Open an [Issue](https://github.com/Dannysoy2800/danny-ai-os/issues)

## Recognition

Contributors will be recognized in:
- Release notes for significant contributions
- CONTRIBUTORS.md file
- GitHub contributors page

## Questions?

- Check existing [Issues](https://github.com/Dannysoy2800/danny-ai-os/issues)
- Read [docs/](docs/) directory
- Ask in [Discussions](https://github.com/Dannysoy2800/danny-ai-os/discussions)

---

Thank you for contributing to Danny AI OS! 🎉
