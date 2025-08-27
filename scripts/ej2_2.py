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

    # Cargar documento y crear embeddings
    embeddings, chunks, meta = vector_db.load_document(sample_markdown)
    print("Chunks generados a partir del texto:")
    for chunk in chunks:
        print(f" - {chunk}")
    print("\nMetadatos generados:")
    for m in meta:
        print(f" - {m}")

    # Imprimir número de embeddings
    print("\nNúmero de embeddings generados:")
    vector_db.print_number_of_embeddings()


if __name__ == "__main__":
    main()
