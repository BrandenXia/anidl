.PHONY: dev

dev:
	uv run textual run --dev src/anidl/__main__.py

check:
	uv run mypy src
