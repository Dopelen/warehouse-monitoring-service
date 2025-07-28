from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.db.database import get_async_session
from app.schemas.warehouse import WarehouseStockResponse
from app.services.warehouse import get_warehouse_stock

router = APIRouter()

@router.get(
    "/{warehouse_id}/products/{product_id}",
    response_model=WarehouseStockResponse,
    summary="Получить остаток товара на складе",
    description=(
        "Возвращает информацию об остатке определённого товара на заданном складе.\n\n"
        "- `warehouse_id` — UUID склада\n"
        "- `product_id` — UUID товара\n\n"
        "**Ошибки:**\n"
        "- 404 — если товар или склад не найдены"
    ),
    response_description="Информация об остатке товара"
)
async def read_warehouse_stock(
    warehouse_id: UUID,
    product_id: UUID,
    db: AsyncSession = Depends(get_async_session),
):
    """
    Получение текущего количества конкретного товара на складе.

    Параметры:
    - **warehouse_id**: UUID склада.
    - **product_id**: UUID товара.

    Возвращает:
    - Объект `WarehouseStockResponse` с остатком товара.

    Исключения:
    - HTTP 404, если товар или склад не найдены в базе данных.
    """
    return await get_warehouse_stock(db, warehouse_id, product_id)