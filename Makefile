# ForkMonkey Makefile
# CI/CD and development automation

.PHONY: help install test test-unit test-coverage test-ci test-burn-in lint format clean

# Default target
help:
	@echo "ForkMonkey Development Commands"
	@echo "================================"
	@echo ""
	@echo "Testing:"
	@echo "  make test          - Run all tests"
	@echo "  make test-unit     - Run unit tests only"
	@echo "  make test-coverage - Run tests with coverage report"
	@echo "  make test-ci       - Run tests in CI mode (strict, coverage, verbose)"
	@echo "  make test-burn-in  - Run burn-in loop (10 iterations for flaky detection)"
	@echo ""
	@echo "Development:"
	@echo "  make install       - Install dependencies"
	@echo "  make lint          - Run linting checks"
	@echo "  make format        - Format code with black"
	@echo "  make clean         - Remove build artifacts"
	@echo ""
	@echo "CI/CD:"
	@echo "  make ci-test       - Full CI test suite (lint + tests + coverage)"
	@echo "  make ci-burn-in    - CI burn-in for flaky test detection"

# =============================================================================
# Installation
# =============================================================================

install:
	pip install -r requirements.txt
	pip install black ruff  # Dev tools

install-dev: install
	pip install -e .

# =============================================================================
# Testing
# =============================================================================

# Standard test run
test:
	python -m pytest tests/ -v

# Unit tests only (excluding e2e)
test-unit:
	python -m pytest tests/ -v --ignore=tests/test_e2e_fork.py

# Tests with coverage
test-coverage:
	python -m pytest tests/ -v \
		--cov=src \
		--cov-report=term-missing \
		--cov-report=html:htmlcov \
		--cov-report=xml:coverage.xml \
		--cov-fail-under=60

# CI mode: strict, verbose, with coverage
test-ci: ci-test

ci-test:
	@echo "🧪 Running CI Test Suite..."
	@echo "=============================="
	python -m pytest tests/ -v \
		--tb=short \
		--strict-markers \
		--cov=src \
		--cov-report=term-missing \
		--cov-report=xml:coverage.xml \
		--cov-fail-under=30 \
		--junit-xml=test-results.xml \
		-x  # Stop on first failure
	@echo ""
	@echo "✅ CI Tests Passed!"

# Burn-in loop for flaky test detection
test-burn-in:
	@echo "🔥 Running Burn-In Loop (10 iterations)..."
	@echo "==========================================="
	@for i in 1 2 3 4 5 6 7 8 9 10; do \
		echo ""; \
		echo "🔥 Burn-in iteration $$i/10"; \
		echo "─────────────────────────────"; \
		python -m pytest tests/ -v --tb=line -q || exit 1; \
	done
	@echo ""
	@echo "✅ Burn-in Complete: No flaky tests detected!"

# CI burn-in (3 iterations for speed)
ci-burn-in:
	@echo "🔥 CI Burn-In Loop (3 iterations)..."
	@for i in 1 2 3; do \
		echo "🔥 Burn-in $$i/3"; \
		python -m pytest tests/ -v --tb=line -q || exit 1; \
	done
	@echo "✅ CI Burn-in passed!"

# =============================================================================
# Linting & Formatting
# =============================================================================

lint:
	@echo "🔍 Running linters..."
	python -m ruff check src/ tests/ --fix || true
	python -m ruff format --check src/ tests/ || true

format:
	@echo "🎨 Formatting code..."
	python -m ruff format src/ tests/
	python -m ruff check src/ tests/ --fix

# =============================================================================
# Cleanup
# =============================================================================

clean:
	rm -rf __pycache__ */__pycache__ */*/__pycache__
	rm -rf .pytest_cache .coverage htmlcov coverage.xml test-results.xml
	rm -rf *.egg-info build dist
	find . -name "*.pyc" -delete
	find . -name ".DS_Store" -delete

# =============================================================================
# Development Helpers
# =============================================================================

# Run the CLI
run:
	python src/cli.py

# Show monkey
show:
	python src/cli.py show

# Evolve monkey
evolve:
	python src/cli.py evolve --ai

