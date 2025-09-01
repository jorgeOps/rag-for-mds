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

ex3_2:
	PYTHONPATH=src uv run python scripts/ej3_2.py

ex3_3:
	PYTHONPATH=src uv run python scripts/ej3_3.py "$(PROMPT)"

ui:
	PYTHONPATH=src uv run streamlit run main.py --server.port 8501

docker-build:
	docker build -t rag-chatbot .

podman-build:
	podman build -t rag-chatbot .

docker-run:
	podman run --rm -it -p 8501:8501 --env-file .env rag-chatbot

podman-run:
	podman run --rm -it -p 8501:8501 --env-file .env rag-chatbot

docker-run-md:
	docker run --rm -it -p 8501:8501 --env-file .env \
		-v $(PWD)/ai-engineer-evaluation-test.md:/app/ai-engineer-evaluation-test.md:ro \
		rag-chatbot

podman-run-md:
	podman run --rm -it -p 8501:8501 --env-file .env \
		-v $(PWD)/ai-engineer-evaluation-test.md:/app/ai-engineer-evaluation-test.md:ro \
		rag-chatbot
