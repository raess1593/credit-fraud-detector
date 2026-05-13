.PHONY: lint test

lint:
	black --check src tests
	isort --check-only src tests

lint-fix:
	black src tests
	isort src tests

test:
	python -m pytest tests/ -v --cov=src --cov-fail-under=60