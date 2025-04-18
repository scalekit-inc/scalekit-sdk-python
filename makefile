.PHONY: all get_proto_dir prepare buf_generate restore generate_init_files cleanup

TEMP_DIR := temp_scalekit
SCALEKIT_DIR := scalekit
BUF_DIR := buf
GOOGLE_DIR := google
PROTO_DIR := proto
PROTOC_DIR := protoc_gen_openapiv2

all: get_proto_dir copy_proto_dir prepare buf_generate restore generate_init_files cleanup

get_proto_dir:
	@echo "Step 1: Getting proto directory path..."
	@read -p "Enter your proto directory path: " proto_dir; \
	echo $$proto_dir > .dirpath

copy_proto_dir:
	@proto_dir=$$(cat .dirpath); \
	echo "Step 2: Syncing from: $$proto_dir to current directory"; \
	rsync -av "$$proto_dir/" proto/; \
	rm -f .dirpath

prepare:
	@echo "Step 3: Preparing temp folder and copying contents..."
	mkdir -p $(TEMP_DIR)
	rsync -av --exclude 'v1' $(SCALEKIT_DIR)/ $(TEMP_DIR)/
	rm -rf $(BUF_DIR) $(SCALEKIT_DIR)

buf_generate:
	@echo "Step 4: Running 'buf generate --include-imports'..."
	buf generate --include-imports

restore:
	@echo "Step 5: Restoring contents from temp folder..."
	rsync -av $(TEMP_DIR)/ $(SCALEKIT_DIR)/
	rm -rf $(TEMP_DIR)

generate_init_files:
	@echo "Step 6: Creating blank '__init__.py' files..."
	find $(BUF_DIR) -type d -exec touch {}/__init__.py \;
	find $(SCALEKIT_DIR)/v1 -type d -exec touch {}/__init__.py \;
	touch $(SCALEKIT_DIR)/common/__init__.py
	touch $(SCALEKIT_DIR)/constants/__init__.py
	touch $(SCALEKIT_DIR)/utils/__init__.py

cleanup:
	@echo "Step 7: Cleaning up generated folders..."
	rm -rf $(GOOGLE_DIR) $(PROTO_DIR) $(PROTOC_DIR)
