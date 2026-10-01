.PHONY: slides check
PYTHON ?= python3

slides:
	cd slides && for source in week_*.tex; do latexmk -pdf -interaction=nonstopmode -halt-on-error "$$source" || exit 1; done

check:
	$(PYTHON) -m unittest discover -s tests -v
	$(PYTHON) scripts/check_notebooks.py
