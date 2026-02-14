from datetime import datetime, timezone


def format_user_activity(last_active_time: datetime) -> str:
    """Форматирует время последней активности"""

    now = datetime.now(timezone.utc)
    diff = now - last_active_time
    total_seconds = int(diff.total_seconds())

    if total_seconds < 60:
        return "Только что"
    elif total_seconds < 3600:
        minutes = total_seconds // 60
        return f"{minutes} минут назад"
    elif total_seconds < 86400:
        hours = total_seconds // 3600
        return f"{hours} часов назад"
    elif diff.days == 1:
        return "Вчера"
    elif diff.days < 7:
        return f"{diff.days} дней назад"
    elif diff.days < 30:
        weeks = diff.days // 7
        return f"{weeks} недель назад"
    elif diff.days < 365:
        months = diff.days // 30
        return f"{months} месяцев назад"
    else:
        years = diff.days // 365
        return f"{years} лет назад"
