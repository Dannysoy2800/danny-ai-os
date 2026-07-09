.PHONY: help install install-dev test lint format quality clean run docs

help:
	@echo "Danny AI OS - Development Makefile"
	@echo ""
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  install          Install production dependencies"
	@echo "  install-dev      Install development dependencies"
	@echo "  test             Run tests with coverage"
	@echo "  test-fast        Run tests without coverage"
	@echo "  lint             Run linting checks (flake8 + mypy)"
	@echo "  format           Format code with Black"
	@echo "  check-format     Check formatting without changes"
	@echo "  quality          Run all quality checks (lint + format check)"
	@echo "  clean            Remove cache files and build artifacts"
	@echo "  run              Run the main application"
	@echo "  docs             Build documentation"
	@echo "  help             Show this help message"
	@echo ""

# Installation targets
install:
	pip install -r requirements.txt

install-dev: install
	pip install -r requirements-dev.txt
	pre-commit install

# Testing targets
test:
	pytest -v --cov=. --cov-report=html --cov-report=term-missing

test-fast:
	pytest -v

test-file:
	@read -p "Enter test file path: " file; \
	pytest $$file -v

test-watch:
	ptw -- -v

# Code quality targets
lint:
	@echo "Running Flake8..."
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 . --count --exit-zero --max-complexity=10 --max-line-length=100 --statistics
	@echo "Running mypy..."
	mypy . --ignore-missing-imports

format:
	@echo "Formatting with Black..."
	black . --line-length=100

check-format:
	@echo "Checking formatting with Black..."
	black . --check --line-length=100

quality: lint check-format
	@echo "✅ All quality checks passed!"

# Cleanup targets
clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".coverage" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	@echo "Cleaned up cache files"

# Runtime targets
run:
	python app.py

run-verbose:
	python -u app.py

# Documentation targets
docs:
	@echo "Building documentation..."
	@echo "Documentation files:"
	@ls -la docs/ 2>/dev/null || echo "No docs directory yet"

# Git helpers
sign-config:
	@echo "Setting up GPG commit signing..."
	@echo "Configure your GPG key first: https://docs.github.com/en/authentication/managing-commit-signature-verification/signing-commits"
	git config commit.gpgsign true

commit:
	@read -p "Enter commit message: " msg; \
	git commit -S -m "$$msg"

# Development workflow
dev-setup: install-dev
	@echo "Development environment ready!"
	@echo "Run 'make run' to start the application"
	@echo "Run 'make test' to run tests"
	@echo "Run 'make quality' to check code quality"

prep-commit: format lint test
	@echo "✅ Ready to commit!"

# CI/CD simulation
ci: clean install-dev quality test
	@echo "✅ CI pipeline passed!"
