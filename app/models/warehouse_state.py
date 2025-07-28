from sqlalchemy import Column, Integer
from sqlalchemy.dialects.postgresql import UUID
from app.models.movement import Base

class WarehouseState(Base):
    __tablename__ = "warehouse_states"

    warehouse_id = Column(UUID(as_uuid=True), primary_key=True)
    product_id = Column(UUID(as_uuid=True), primary_key=True)
    quantity = Column(Integer, nullable=False, default=0)