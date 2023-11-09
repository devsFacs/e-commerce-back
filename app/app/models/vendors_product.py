from sqlalchemy import Boolean, Column, Integer, String, DateTime, Text, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

from app.db.base_class import Base
from ..utils import _get_date


class VendorsProduct(Base):
    __tablename__ = "vendors_product"
    id = Column(Integer, primary_key=True, index=True)
    id_vendor = Column(Integer, ForeignKey("vendors.id"))
    id_product = Column(Integer, ForeignKey("product.id"))

    created_at = Column(DateTime, default=_get_date)
    updated_at = Column(DateTime, onupdate=_get_date)

    product = relationship("Product", foreign_keys=[id_product])
    vendor = relationship("Vendors", foreign_keys=[id_vendor])
