# SPDX-License-Identifier: MIT
.PHONY: pdf check
pdf:
	mkdir -p build
	latexmk -xelatex -interaction=nonstopmode -halt-on-error -file-line-error -outdir=build china-capital-2026.tex

check:
	python3 research/scripts/verify_expansion.py
	python3 scripts/check_release.py
