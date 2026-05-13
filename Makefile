.PHONY: lint

lint:
	black --check src tests
	isort --check-only src tests