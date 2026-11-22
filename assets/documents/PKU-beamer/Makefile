# PKU-beamer
ifeq ($(OS),Windows_NT)
    BUILD_SCRIPT := powershell -NoProfile -ExecutionPolicy Bypass -File scripts/build.ps1
else
    BUILD_SCRIPT := bash scripts/build.sh
endif

.PHONY: all beamer clean help
all: beamer
beamer:
	@$(BUILD_SCRIPT) beamer
clean:
	@$(BUILD_SCRIPT) clean
help:
	@echo "make [beamer | clean] - build the presentation or remove build artifacts"
