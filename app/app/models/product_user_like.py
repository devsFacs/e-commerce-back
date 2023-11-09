from sqlalchemy import Boolean, Column, Integer, String, DateTime, Text, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

from app.db.base_class import Base
from ..utils import _get_date


class ProductUserLike(Base):
    __tablename__ = "product_user_like"
    id = Column(Integer, primary_key=True, index=True)
    id_user = Column(Integer, ForeignKey("user.id"))
    id_product = Column(Integer, ForeignKey("product.id"))
    status = Column(Boolean(), default=True)

    created_at = Column(DateTime, default=_get_date)
    updated_at = Column(DateTime, onupdate=_get_date)

    product = relationship("Product", foreign_keys=[id_product])
    user = relationship("User", foreign_keys=[id_user])
