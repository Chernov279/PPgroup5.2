from datetime import datetime

from src.utils.context_utils import get_user_id, get_request_id


class MessageEnricher:
    """Обогащает любое сообщение системными полями из contextvars."""

    @staticmethod
    def enrich(message: dict) -> dict:
        enriched = {
            **message,
            "request_id": get_request_id(),
            "timestamp": datetime.utcnow().isoformat(),
        }
        return enriched
