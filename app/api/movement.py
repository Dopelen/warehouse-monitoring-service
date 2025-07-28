import logging
from uuid import UUID
from fastapi import APIRouter, Request, HTTPException, Depends
from app.schemas.movement import KafkaMovementMessage, SendMovementResponse, MovementInfoResponse
from app.db.database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.movement import get_movement_info

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post(
    "/send",
    response_model=SendMovementResponse,
    summary="Отправить событие перемещения в Кафку",
    description=(
            "Тестовый эндпоинт, который отправляет событие перемещения товара между складами в Kafka.\n\n"
            "Эндпоинт принимает сообщение в формате `KafkaMovementMessage` (структура сообщения из описания задания) и отправляет его в Kafka-топик\n"
            "с помощью Kafka producer'а, доступного в приложении."
    ),
    status_code=200
)
async def produce_movement(message: KafkaMovementMessage, request: Request):
    """
    Тестовый эндпоинт, который отправляет событие перемещения товара между складами в Kafka.
    Эндпоинт принимает сообщение в формате KafkaMovementMessage и отправляет его в Kafka-топик
    через Kafka producer, доступный в приложении.

    Исключения:
    - Возвращает 503, если Kafka producer недоступен.
    - Возвращает 500 при общей ошибке отправки сообщения.

    Возвращает статус отправки сообщения.
    """
    producer = request.app.state.kafka_producer
    try:
        await producer.send_movement(message)
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail="Kafka producer is not available")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to send Kafka message")
    return {"status": "message sent"}

@router.get(
    "/{movement_id}",
    response_model=MovementInfoResponse,
    summary="Получить информацию о перемещении",
    description=(
            "Возвращает пару событий перемещения (**отправка** и **получение**) по `movement_id`.\n\n"
            "Подсчитывает:\n"
            "- разницу во времени между событиями,\n"
            "- разницу в количестве товара."
    ))
async def movement_info(
    movement_id: UUID,
    db: AsyncSession = Depends(get_async_session)
):
    """
    Возвращает информацию о паре перемещений (`departure` и `arrival`) по заданному movement_id.

    Параметры:
    - movement_id (UUID): Идентификатор логической пары перемещений (отправка и получение).

    Возвращает:
    - movement_id: ID пары.
    - from_warehouse: UUID склада-отправителя.
    - to_warehouse: UUID склада-получателя.
    - time_diff_seconds: Разница во времени между отправлением и прибытием (в секундах).
    - quantity_difference: Разница в количестве между отправкой и получением.

    Статус коды ответа:
    - 404, если не найдена пара.
    - 400, если пара содержит некорректные события.
    """
    return await get_movement_info(movement_id, db)