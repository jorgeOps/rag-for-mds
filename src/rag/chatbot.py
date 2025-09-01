from __future__ import annotations

from typing import List
from rag.vector_db import VectorDDBB
from rag.llm_client import ChatLLM


class Chatbot:

    def __init__(
        self,
        vector_db: VectorDDBB,
        llm: ChatLLM,
        *,
        k: int = 3,
        max_context_chars: int = 4000,
    ) -> None:
        self._db = vector_db
        self._llm = llm
        self._k = max(1, k)
        self._max_context_chars = max_context_chars

    def ask_question(self, question: str) -> str:
        if not question or not question.strip():
            return "Por favor, formula una pregunta válida."
        # Usamos el método que creamos de VectorDDBB con el dot product
        chunks = self._db.nearest_chunks(question, top_n=self._k)
        return self.ask_with_chunks(question, chunks)

    def ask_with_chunks(self, question: str, chunks: List[str]) -> str:
        if not chunks:
            return "No tengo contexto cargado todavía. ¿Has ingerido el markdown?"

        context = ("\n\n---\n\n").join(chunks)
        if len(context) > self._max_context_chars:
            context = context[: self._max_context_chars] + "\n\n[...]"

        # Forma de mejorar esto en un futuro -> cambiarlo por yml para que sea más editable
        system = (
            "Eres un asistente que responde exclusivamente con la información del contexto "
            "proporcionado. Si la respuesta a lo que te están preguntando no está en el contexto, di claramente "
            "'No puedo responder a tu pregunta con el contexto proporcionado'. Responde en español y sé conciso."
            " Sí que puedes responder a preguntas de sentido común o generales, "
            "pero siempre avisando de que eso no tiene que ver con el contenido del documento."
        )
        user = (
            "Contexto (extractos de la guía):\n"
            f"{context}\n\n"
            "Pregunta del usuario:\n"
            f"{question}\n\n"
            "Instrucciones:\n"
            "- Responde con una frase o una lista breve.\n"
            "- Si es posible, menciona el título del apartado del que sacas la información.\n"
            "- Si no está en el contexto, responde: 'No puedo responder a tu pregunta con el contexto proporcionado'."
        )
        # Para mandar la pregunta, usamos la función ask del cliente LLM que creamos antes
        return self._llm.ask(user, system=system)
