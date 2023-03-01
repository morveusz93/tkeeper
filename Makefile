.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re
import sys
import textwrap

wrapper = textwrap.TextWrapper(subsequent_indent=(" " * 45), width=79)
for line in sys.stdin:
    if line.startswith("##"):
        print(line.strip())
    match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
    if match:
        target, help = match.groups()
        print("\n".join(wrapper.wrap(f"{target:39}{help}")))
endef

export PRINT_HELP_PYSCRIPT

help:
	cat $(MAKEFILE_LIST) | python -c "$$PRINT_HELP_PYSCRIPT"



test:  ## just tests
	poetry run pytest


test-with-linters:  ## tests with black and isort
	poetry run pytest --black --isort


run-local:  ## run API
	poetry run uvicorn main:app --reload
