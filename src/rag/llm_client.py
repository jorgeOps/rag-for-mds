import time
from typing import Optional, List, Dict, Any

from openai import OpenAI, APIConnectionError, APIStatusError, RateLimitError
from rag.config import AppConfig


class ChatLLM:
    """
    Esta clase actúa como un cliente para interactuar con la API de OpenAI.
    Al incializar se necesita el datamodel AppConfig, que tendrá las credenciales
    de Openai.
    """
    def __init__(self, cfg: AppConfig) -> None:
        # Importante para la prueba: inicializar el cliente con base_url del proxy.
        self._client = OpenAI(
            api_key=cfg.openai_api_key,
            base_url=cfg.base_url,
            timeout=cfg.timeout_s,
        )
        self._model = cfg.model
        self._max_retries = cfg.max_retries

    def ask(
        self,
        prompt: str,
        system: Optional[str] = None,
        *,
        temperature: float = 0.0,
        max_tokens: Optional[int] = None,
    ) -> str:
        """
        Lanza una completion de chat y devuelve el texto en limpio.
        Acepta como input el prompt del usuario, y un system prompt opcional.
        Devuelve el texto generado por el modelo.
        """
        messages: List[Dict[str, Any]] = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        # Metemos reintentos por si hay algún error (429 p.ej.)
        delay = 0.8
        for attempt in range(self._max_retries + 1):
            try:
                resp = self._client.chat.completions.create(
                    model=self._model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                )
                return (resp.choices[0].message.content or "").strip()

            except (RateLimitError, APIConnectionError, APIStatusError) as e:
                # Si ya agotamos intentos, lo propagamos.
                if attempt >= self._max_retries:
                    raise
                time.sleep(delay)
                delay *= 1.5

        raise RuntimeError("No se pudo obtener respuesta del LLM tras varios intentos.")
