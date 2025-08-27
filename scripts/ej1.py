from rag.config import load
from rag.llm_client import ChatLLM

def main() -> None:
    cfg = load()
    llm = ChatLLM(cfg)

    pregunta = "¿Cuántas 'a' tiene la palabra MasOrange?"
    system = "Responde solo con el número (un entero), sin explicación."

    print(f"Pregunta: {pregunta}")
    print(f"Usando modelo: {cfg.model} | base_url: {cfg.base_url}")
    respuesta = llm.ask(pregunta, system=system)
    print(f"Respuesta del modelo: {respuesta}")

if __name__ == "__main__":
    main()
