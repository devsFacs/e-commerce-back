from sqlalchemy import Boolean, Column, Integer, String, DateTime, Text, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

from app.db.base_class import Base
from ..utils import _get_date


class ProductDetails(Base):
    __tablename__ = "product_details"
    id = Column(Integer, primary_key=True, index=True)
    color = Column(String(256))
    size = Column(String(256))
    id_product = Column(Integer, ForeignKey("product.id"))
    status_stock = Column(Integer)

    created_at = Column(DateTime, default=_get_date)
    updated_at = Column(DateTime, onupdate=_get_date)

    product = relationship("Product", foreign_keys=[id_product])
