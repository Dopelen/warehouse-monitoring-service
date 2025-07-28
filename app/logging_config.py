import logging
import sys

def setup_logging():
    """Настройка логгера для всего приложения."""

    logging.basicConfig(
        level=logging.INFO,  # Можно заменить на DEBUG в отладке
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        stream=sys.stdout,
    )

    # Приглушим лишние библиотеки
    logging.getLogger("sqlalchemy").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("aiokafka").setLevel(logging.WARNING)
    logging.getLogger("aiokafka.consumer.group_coordinator").setLevel(logging.ERROR)
    logging.getLogger("uvicorn.error").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)