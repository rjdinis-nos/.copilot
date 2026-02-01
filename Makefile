.PHONY: build preview help

# Default target
.DEFAULT_GOAL := help

# Build customizations.yml from agent and instruction files
build:
	@echo "Building customizations.yml..."
	@uv run build.py

# Preview site locally (requires Python)
preview:
	@echo "Starting local server at http://localhost:8000"
	@echo "Press Ctrl+C to stop"
	@python3 -m http.server 8000

# Show help
help:
	@echo "Available commands:"
	@echo "  make build          - Generate customizations.yml from source files"
	@echo "  make preview        - Start local web server to preview site"
	@echo "  make help           - Show this help message"
