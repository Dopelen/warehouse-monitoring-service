from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from app.models.enums import MovementEvent


class KafkaMovementData(BaseModel):
    movement_id: UUID = Field(..., description="ID перемещения")
    warehouse_id: UUID = Field(..., description="ID склада")
    product_id: UUID = Field(..., description="ID товара")
    quantity: int = Field(..., description="Количество товара")
    event: MovementEvent = Field(..., description="Событие: arrival или departure")
    timestamp: datetime = Field(..., description="Временная метка события")


class KafkaMovementMessage(BaseModel):
    id: UUID = Field(..., description="ID сообщения")
    source: str = Field(..., description="Источник сообщения")
    specversion: str = Field(..., description="Версия спецификации")
    type: str = Field(..., description="Тип события")
    datacontenttype: str = Field(..., description="Тип содержимого")
    dataschema: str = Field(..., description="Ссылка на схему данных")
    time: int = Field(..., description="Время события в миллисекундах UNIX")
    subject: str = Field(..., description="Тема события")
    destination: str = Field(..., description="Получатель события")
    data: KafkaMovementData = Field(..., description="Данные перемещения")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "39df66b2-a5ac-43d9-995e-d4a05142d6d9",
                "source": "inventory-service",
                "specversion": "1.0",
                "type": "inventory.movement",
                "datacontenttype": "application/json",
                "dataschema": "/schemas/movement",
                "time": 1721906400000,
                "subject": "warehouse.sync",
                "destination": "movement-processor",
                "data": {
                    "movement_id": "77900d3c-8d3a-4421-97d7-297e995b516d",
                    "warehouse_id": "7689ba85-8a97-46dd-a7bf-b5e47b3f0acf",
                    "product_id": "2b898dd7-525e-4548-9a5c-41cfcda38a30",
                    "quantity": 100,
                    "event": "arrival",
                    "timestamp": "2025-07-25T10:00:00Z"
                }
            }
        }


class FlatMovementMessage(BaseModel):
    id: UUID = Field(..., description="ID сообщения")
    source: str = Field(..., description="Источник сообщения")
    specversion: str = Field(..., description="Версия спецификации")
    type: str = Field(..., description="Тип события")
    datacontenttype: str = Field(..., description="Тип содержимого")
    dataschema: str = Field(..., description="Ссылка на схему данных")
    time: int = Field(..., description="Время события в миллисекундах UNIX")
    subject: str = Field(..., description="Тема события")
    destination: str = Field(..., description="Получатель события")

    movement_id: UUID = Field(..., description="ID перемещения")
    warehouse_id: UUID = Field(..., description="ID склада")
    product_id: UUID = Field(..., description="ID товара")
    quantity: int = Field(..., description="Количество")
    event: MovementEvent = Field(..., description="Тип события")
    timestamp: datetime = Field(..., description="Время события")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "39df66b2-a5ac-43d9-995e-d4a05142d6d9",
                "source": "inventory-service",
                "specversion": "1.0",
                "type": "inventory.movement",
                "datacontenttype": "application/json",
                "dataschema": "/schemas/movement",
                "time": 1721906400000,
                "subject": "warehouse.sync",
                "destination": "movement-processor",

                "movement_id": "77900d3c-8d3a-4421-97d7-297e995b516d",
                "warehouse_id": "7689ba85-8a97-46dd-a7bf-b5e47b3f0acf",
                "product_id": "2b898dd7-525e-4548-9a5c-41cfcda38a30",
                "quantity": 100,
                "event": "arrival",
                "timestamp": "2025-07-25T10:00:00Z"
            }
        }


class MovementCreate(FlatMovementMessage):
    """Пока просто наследуется от FlatMovementMessage"""
    pass


class SendMovementResponse(BaseModel):
    status: str = Field(..., example="message sent", description="Статус отправки сообщения в Kafka")


class MovementInfoResponse(BaseModel):
    movement_id: UUID = Field(..., description="ID перемещения")
    from_warehouse: UUID = Field(..., description="ID отправителя")
    to_warehouse: UUID = Field(..., description="ID получателя")
    time_diff_seconds: float = Field(..., description="Разница во времени между отправкой и приемкой (в секундах)")
    quantity_difference: int = Field(..., description="Разница в количестве между отправкой и приемкой")

    class Config:
        json_schema_extra = {
            "example": {
                "movement_id": "29a1adda-8c55-46f2-a2a5-644bd03d6db9",
                "from_warehouse": "ce6e83c5-f734-4981-bfe5-d3c1dc45350d",
                "to_warehouse": "b77151af-7b0c-42da-858a-ba758c9ada0e",
                "time_diff_seconds": 6.5,
                "quantity_difference": 0
            }
        }