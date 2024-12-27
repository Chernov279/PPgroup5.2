import logging
from functools import wraps


def log_errors(log_file="errors.log"):
    """
    Декоратор для логирования ошибок.

    Args:
        log_file (str): Путь к файлу для записи логов.

    Returns:
        function: Декорированная функция.
    """
    # Настройка логгера
    logging.basicConfig(
        filename=log_file,
        level=logging.ERROR,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logging.error("Exception in %s: %s", func.__name__, str(e), exc_info=True)
                raise

        return wrapper

    return decorator
