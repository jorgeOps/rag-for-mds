from rag.config import load
from rag.embeddings import Embedder


def main() -> None:
    cfg = load()
    embedder = Embedder(cfg)

    user_prompt = "You shall not pass!"
    vec = embedder.embed_text(user_prompt)

    print(f"Frase: {user_prompt}")
    print(f"Modelo de embeddings: {cfg.embedding_model} | base_url: {cfg.base_url}")
    print(f"Longitud del embedding: {len(vec)}")
    print("Embedding:")
    print(vec)


if __name__ == "__main__":
    main()
