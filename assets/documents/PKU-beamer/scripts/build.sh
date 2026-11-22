#!/usr/bin/env bash
set -euo pipefail
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BUILD_DIR="${PROJECT_DIR}/scripts/.build/beamer"
case "${1:-beamer}" in
    clean)
        [[ "$BUILD_DIR" == "$PROJECT_DIR"/scripts/.build/beamer ]] || exit 1
        rm -rf -- "$BUILD_DIR"
        rm -f -- "$PROJECT_DIR/output/beamer.pdf"
        exit 0
        ;;
    all|beamer) ;;
    *) echo "Usage: $0 [beamer | clean]" >&2; exit 1 ;;
esac
command -v latexmk >/dev/null || { echo "Install latexmk and XeLaTeX." >&2; exit 1; }
mkdir -p "$BUILD_DIR"
STYLE_PATH="$PROJECT_DIR/style"
SEPARATOR=":"
case "$(uname -s)" in
    CYGWIN*|MINGW*|MSYS*)
        STYLE_PATH="$(cygpath -m "$STYLE_PATH")"
        SEPARATOR=";"
        ;;
esac
export TEXINPUTS="${STYLE_PATH}//${SEPARATOR}${TEXINPUTS:-}"
cd "$PROJECT_DIR/src/beamer"
latexmk -xelatex -silent -interaction=nonstopmode -halt-on-error -synctex=1 \
    "-outdir=$BUILD_DIR" main.tex
mkdir -p "$PROJECT_DIR/output"
cp "$BUILD_DIR/main.pdf" "$PROJECT_DIR/output/beamer.pdf"
echo "Created: $PROJECT_DIR/output/beamer.pdf"
