#!/usr/bin/env bash
# Compile every .tex document in the repo to PDF using the shared template.
# Usage: ./scripts/build-pdf.sh            # all documents
#        ./scripts/build-pdf.sh path/a.tex # selected documents
# Output: pdf/<folder>/<name>.pdf
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
export TEXINPUTS="$ROOT/latex//:"

if [ "$#" -gt 0 ]; then
  files=("$@")
else
  # Every .tex except the shared template folder and the build folder.
  mapfile -t files < <(find . -name '*.tex' -not -path './latex/*' -not -path './pdf/*' -not -path './.git/*' | sort)
fi

status=0
for tex in "${files[@]}"; do
  tex="${tex#./}"
  outdir="pdf/$(dirname "$tex")"
  mkdir -p "$outdir" build
  echo "==> $tex"
  if latexmk -pdf -interaction=nonstopmode -halt-on-error -quiet \
       -outdir="build/$(dirname "$tex")" "$tex"; then
    cp "build/$(dirname "$tex")/$(basename "${tex%.tex}").pdf" "$outdir/"
  else
    echo "!! failed: $tex"; status=1
  fi
done
exit $status
