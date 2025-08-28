.PHONY: setup ex1 test fmt

setup:
	uv sync

ex1:
	PYTHONPATH=src uv run python scripts/ej1.py

ex2_1:
	PYTHONPATH=src uv run python scripts/ej2_1.py

ex2_2:
	PYTHONPATH=src uv run python scripts/ej2_2.py

ex3_1:
	PYTHONPATH=src uv run python scripts/ej3_1.py "$(PROMPT)"

test:
	uv run pytest -q

fmt:
	uv run ruff check --fix .
