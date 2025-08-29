from datetime import datetime


def make_base_payload(extra: dict, request_id: str | None = None):
    """

    """
    payload = {"ts": datetime.utcnow().isoformat(), **extra}
    if request_id:
        payload["request_id"] = request_id
    return payload


def key_for_user(user_id: int) -> bytes:
    # Kafka partition key (consistent by user)
    return str(user_id).encode()
