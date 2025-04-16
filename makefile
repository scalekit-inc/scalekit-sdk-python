.PHONY: all prepare buf_generate restore cleanup init

TEMP_DIR := temp_scalekit
SCALEKIT_DIR := scalekit
BUF_DIR := buf

all: prepare buf_generate restore cleanup init

prepare:
	@echo "Step 1: Preparing temp folder and copying contents..."
	rsync -av ~/Documents/scalekit/proto/ proto/
	mkdir -p $(TEMP_DIR)
	rsync -av --exclude 'v1' $(SCALEKIT_DIR)/ $(TEMP_DIR)/
	rm -rf $(BUF_DIR) $(SCALEKIT_DIR)

buf_generate:
	@echo "Step 2: Running 'buf generate --include-imports'..."
	buf generate --include-imports

restore:
	@echo "Step 3: Restoring contents from temp folder..."
	rsync -av $(TEMP_DIR)/ $(SCALEKIT_DIR)/
	rm -rf $(TEMP_DIR)

cleanup:
	@echo "Step 4: Cleaning up generated folders..."
	find . -mindepth 1 -maxdepth 1 -type d ! -name $(BUF_DIR) ! -name $(SCALEKIT_DIR) -exec rm -rf {} +

init:
	@echo "Step 5: Creating blank '__init__.py' files..."
	find $(BUF_DIR) -type d -exec touch {}/__init__.py \;
	find $(SCALEKIT_DIR)/v1 -type d -exec touch {}/__init__.py \;
	touch $(SCALEKIT_DIR)/common/__init__.py
	touch $(SCALEKIT_DIR)/constants/__init__.py
	touch $(SCALEKIT_DIR)/utils/__init__.py
