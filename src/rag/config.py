from datamodel.app_config import AppConfig
import os
from dotenv import load_dotenv


def load() -> AppConfig:

    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY no está definido. "
            "Crea un .env (puedes copiar .env.example) y pon tu clave."
        )

    model = os.getenv("RAG_MODEL", "openai/gpt-4o-mini").strip()
    base_url = os.getenv("LLM_BASE_URL", "https://llmproxy.ai.orange").strip()
    timeout_s = float(os.getenv("OPENAI_TIMEOUT_S", 30))
    max_retries = int(os.getenv("OPENAI_MAX_RETRIES", 2))

    return AppConfig(
        openai_api_key=api_key,
        model=model,
        base_url=base_url,
        timeout_s=timeout_s,
        max_retries=max_retries
    )
