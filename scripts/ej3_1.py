import sys
from rag.vector_db import VectorDDBB


def main() -> None:
    vector_db = VectorDDBB()

    sample_markdown = """
    # Introduction
    This is the introduction section.

    ## First Section
    This is the first section with some content.

    ## Second Section
    This is the second section with different content.

    ## Third Section
    And this is the third section.
    """

    # Ingesta del documento (genera embeddings de cada chunk)
    vector_db.load_document(sample_markdown)

    # Consulta -> He puesto el makefile de manera que la consulta se pueda pasar como variable
    query = sys.argv[1] if len(sys.argv) > 1 else "part number two"
    top = vector_db.nearest_chunks(query)

    print("Query:", query)
    print("Top matches:")
    for i, chunk in enumerate(top, start=1):
        print(f"\n[{i}] ---")
        print(chunk)


if __name__ == "__main__":
    main()
