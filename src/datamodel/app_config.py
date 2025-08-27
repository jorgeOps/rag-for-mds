from dataclasses import dataclass


@dataclass(frozen=True)
class AppConfig:
    openai_api_key: str
    model: str
    base_url: str
    timeout_s: float
    max_retries: int