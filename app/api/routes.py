from fastapi import APIRouter
from app.api import movement, warehouse

api_router = APIRouter()
api_router.include_router(movement.router, prefix="/movements", tags=["movements"])
api_router.include_router(warehouse.router, prefix="/warehouses", tags=["warehouses"])