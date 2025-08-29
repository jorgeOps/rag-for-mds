import sys
from pathlib import Path
from rag.vector_db import VectorDDBB


def main() -> None:
    db = VectorDDBB()

    # Ruta al markdown en la raíz del repo
    repo_root = Path(__file__).resolve().parents[1]
    md_path = repo_root / "ai-engineer-evaluation-test.md"

    # El flujo es este
    # 1) Ingesta
    db.load_document_from_path(md_path)

    # 2) Comprobación rápida
    print("Número de chunks y embeddings generados:")
    db.print_number_of_embeddings()

    # 3) Búsqueda:
    # Por defecto se usa la query que viene en el el ejercicio pero tambien puede el user meter una query con el make
    query = sys.argv[1] if len(sys.argv[1]) > 1 else "Darle funcionalidad a la base de datos"
    print("Query del usuario:", query)
    results = db.nearest_chunks(query, top_n=3)

    if not results:
        print("No hay resultados. Comprueba que el documento esté cargado.")
        return

    nearest_chunk = results[0]
    print("\n================== Nearest chunk ==================\n")
    print(nearest_chunk)

if __name__ == "__main__":
    main()
