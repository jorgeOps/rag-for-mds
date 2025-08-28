from __future__ import annotations

from pathlib import Path
from rag.vector_db import VectorDDBB


def main() -> None:
    vector_db = VectorDDBB()

    # Ruta al markdown: <repo_root>/ai-engineer-evaluation-test.md
    repo_root = Path(__file__).resolve().parents[1]
    md_path = repo_root / "ai-engineer-evaluation-test.md"

    # Cargar documento y crear embeddings
    vector_db.load_document_from_path(md_path)

    # Imprimir número de embeddings
    print("Número de chunks y embeddings generados:")
    vector_db.print_number_of_embeddings()


if __name__ == "__main__":
    main()
