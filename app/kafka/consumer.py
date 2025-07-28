import json
import logging

from aiokafka import AIOKafkaConsumer
from aiokafka.errors import KafkaError

from app.core.config import settings
from app.schemas.movement import MovementCreate
from app.db.database import get_session_context
from app.services.movement import create_movement

logger = logging.getLogger(__name__)


class KafkaConsumer:
    def __init__(self):
        self._consumer: AIOKafkaConsumer | None = None
        self._running = False

    async def start(self):
        if self._consumer is None:
            self._consumer = AIOKafkaConsumer(
                settings.KAFKA_TOPIC,
                bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
                value_deserializer=lambda m: json.loads(m.decode("utf-8")),
                auto_offset_reset="earliest",
                enable_auto_commit=True,
                group_id="movement-consumer-group"
            )
            await self._consumer.start()
            logger.info("✅ Kafka consumer started")
            self._running = True

    async def stop(self):
        if self._consumer is not None:
            await self._consumer.stop()
            logger.info("⛔ Kafka consumer stopped")
            self._consumer = None
            self._running = False

    async def consume(self):
        if not self._consumer:
            raise RuntimeError("❌ Kafka consumer is not started")

        logger.info("✅ Kafka consumer listening for messages...")
        try:
            async for msg in self._consumer:
                try:
                    raw_data = msg.value
                    logger.info(f"📥 Kafka message with ID {raw_data['id']} was received")
                    data = raw_data.pop("data", {})
                    flat_data = {**raw_data, **data}
                    movement = MovementCreate(**flat_data)

                    async with get_session_context() as session:
                        await create_movement(session, movement)

                except Exception:
                    logger.exception("❌ Error processing Kafka message")

        except KafkaError:
            logger.exception("❌ Kafka error during consumer operation")
        except Exception:
            logger.exception("❌ Unexpected error in Kafka consumer")