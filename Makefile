# Usage:
#   make setup     # Create/update .venv and install dependencies
#   make generate  # Regenerate SDK code from proto sources
#   make lint      # Run static checks
#   make test      # Run unit tests

SHELL := /bin/bash

PYTHON ?= python3
VENV_DIR := .venv
VENV_PYTHON := $(VENV_DIR)/bin/python
VENV_PIP := $(VENV_PYTHON) -m pip

PROTO_REPO_URL := https://github.com/scalekit-inc/scalekit.git
PROTO_REF ?= v0.1.103
PROTO_SUBDIR := proto

TEMP_DIR := temp_scalekit
SCALEKIT_DIR := scalekit
BUF_DIR := buf
GOOGLE_DIR := google
PROTO_DIR := proto
PROTOC_DIR := protoc_gen_openapiv2

.PHONY: setup generate lint test tools-check create-venv prepare buf_generate restore generate_init_files cleanup copy_proto_dir

setup: create-venv
	@echo "Installing SDK dependencies in $(VENV_DIR)..."
	$(VENV_PIP) install --upgrade pip
	$(VENV_PIP) install -e .

create-venv:
	@if [ ! -d "$(VENV_DIR)" ]; then \
		echo "Creating virtual environment at $(VENV_DIR)..."; \
		$(PYTHON) -m venv $(VENV_DIR); \
	else \
		echo "Using existing virtual environment at $(VENV_DIR)..."; \
	fi

tools-check:
	@command -v git >/dev/null 2>&1 || (echo "missing git" && exit 1)
	@command -v rsync >/dev/null 2>&1 || (echo "missing rsync" && exit 1)
	@command -v buf >/dev/null 2>&1 || (echo "missing buf. install buf and rerun 'make setup'" && exit 1)

generate: tools-check
	@echo "Step 1: Fetching proto sources from $(PROTO_REPO_URL) at ref $(PROTO_REF)..."
	@set -euo pipefail; \
	tmp_dir="$$(mktemp -d)"; \
	cleanup_tmp() { rm -rf "$$tmp_dir"; rm -f .dirpath; }; \
	trap cleanup_tmp EXIT; \
	git clone --depth=1 --branch "$(PROTO_REF)" "$(PROTO_REPO_URL)" "$$tmp_dir/scalekit"; \
	echo "$$tmp_dir/scalekit/$(PROTO_SUBDIR)" > .dirpath; \
	$(MAKE) copy_proto_dir prepare buf_generate restore generate_init_files cleanup
	@echo "Code generation complete."

copy_proto_dir:
	@proto_dir=$$(cat .dirpath); \
	echo "Step 2: Syncing proto files from $$proto_dir"; \
	rsync -av "$$proto_dir/" proto/

prepare:
	@echo "Step 3: Preparing temp folder and preserving current scalekit package..."
	mkdir -p $(TEMP_DIR)
	rsync -av --exclude 'v1' $(SCALEKIT_DIR)/ $(TEMP_DIR)/
	rm -rf $(BUF_DIR) $(SCALEKIT_DIR)

buf_generate:
	@echo "Step 4: Running 'buf generate --include-imports'..."
	buf generate --include-imports

restore:
	@echo "Step 5: Restoring scalekit package non-generated files..."
	rsync -av $(TEMP_DIR)/ $(SCALEKIT_DIR)/
	rm -rf $(TEMP_DIR)

generate_init_files:
	@echo "Step 6: Ensuring package __init__.py files exist..."
	find $(BUF_DIR) -type d -exec touch {}/__init__.py \;
	find $(SCALEKIT_DIR)/v1 -type d -exec touch {}/__init__.py \;
	touch $(SCALEKIT_DIR)/common/__init__.py
	touch $(SCALEKIT_DIR)/constants/__init__.py
	touch $(SCALEKIT_DIR)/utils/__init__.py

cleanup:
	@echo "Step 7: Cleaning temporary generated source directories..."
	rm -rf $(GOOGLE_DIR) $(PROTO_DIR) $(PROTOC_DIR)
	rm -f .dirpath

lint: create-venv
	@echo "Running static checks..."
	$(VENV_PYTHON) -m compileall -q scalekit tests

test: create-venv
	@echo "Running tests..."
	$(VENV_PYTHON) -m unittest discover -s tests -p "test_*.py" -v
