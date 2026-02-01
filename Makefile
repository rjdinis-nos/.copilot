.PHONY: build preview help test review

# Default target
.DEFAULT_GOAL := help

# Build customizations.yml from agent and instruction files
build:
	@echo "Building customizations.yml..."
	@uv run build.py

# Test documentation updates locally
test:
	@echo "Testing documentation updates..."
	@mkdir -p test
	@cp README.md test/README.md.orig
	@cp index.html test/index.html.orig
	@uv run update_docs.py
	@cp README.md test/README.md.new
	@cp index.html test/index.html.new
	@echo "✓ Test files created in test/ folder:"
	@echo "  - test/README.md.orig (before)"
	@echo "  - test/README.md.new (after)"
	@echo "  - test/index.html.orig (before)"
	@echo "  - test/index.html.new (after)"
	@echo ""
	@echo "Review changes with:"
	@echo "  diff test/README.md.orig test/README.md.new"
	@echo "  diff test/index.html.orig test/index.html.new"

# Review changes from test
review:
	@if [ ! -d test ]; then \
		echo "Error: test/ folder not found. Run 'make test' first."; \
		exit 1; \
	fi
	@echo "=== README.md changes ==="
	@diff -u test/README.md.orig test/README.md.new || true
	@echo ""
	@echo "=== index.html changes ==="
	@diff -u test/index.html.orig test/index.html.new || true

# Preview site locally (requires Python)
preview:
	@echo "Starting local server at http://localhost:8000"
	@echo "Press Ctrl+C to stop"
	@python3 -m http.server 8000

# Show help
help:
	@echo "Available commands:"
	@echo "  make build          - Generate customizations.yml from source files"
	@echo "  make test           - Test documentation updates and save to test/ folder"
	@echo "  make review         - Review changes from test (show diffs)"
	@echo "  make preview        - Start local web server to preview site"
	@echo "  make help           - Show this help message"
