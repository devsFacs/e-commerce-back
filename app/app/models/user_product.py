from sqlalchemy import Boolean, Column, Integer, String, DateTime, Text, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

from app.db.base_class import Base
from ..utils import _get_date


class UserProduct(Base):
    __tablename__ = "user_product"
    id = Column(Integer, primary_key=True, index=True)
    id_user = Column(Integer, ForeignKey("user.id"))
    id_product_details = Column(Integer, ForeignKey("product_details.id"))
    quantity = Column(Integer)

    created_at = Column(DateTime, default=_get_date)
    updated_at = Column(DateTime, onupdate=_get_date)

    product_details = relationship("ProductDetails", foreign_keys=[id_product_details])
    user = relationship("User", foreign_keys=[id_user])
