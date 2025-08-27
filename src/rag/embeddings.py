import time
from typing import Optional, List

from openai import OpenAI, APIConnectionError, APIStatusError, RateLimitError
from datamodel.app_config import AppConfig


class Embedder:
    """
    Cliente para crear embeddings.
    Necesita como entrada el datamodel de AppConfig.
    Se le puede sobreescribir el modelo.
    """

    def __init__(self, cfg: AppConfig, model: Optional[str] = None, client: Optional[OpenAI] = None) -> None:
        self._client = client or OpenAI(
            api_key=cfg.openai_api_key,
            base_url=cfg.base_url,
            timeout=cfg.timeout_s,
        )
        self._model = model or cfg.embedding_model
        self._max_retries = cfg.max_retries

    def embed_text(self, text: str) -> List[float]:
        """
        Devuelve el embedding como lista de floats.
        Reintenta en errores.
        """
        delay = 0.8
        for attempt in range(self._max_retries + 1):
            try:
                resp = self._client.embeddings.create(
                    model=self._model,
                    input=text,
                )
                vec = resp.data[0].embedding
                return list(vec)
            except (RateLimitError, APIConnectionError, APIStatusError):
                if attempt >= self._max_retries:
                    raise
                time.sleep(delay)
                delay *= 1.5

        raise RuntimeError("No se pudo obtener el embedding tras varios intentos.")
