from sqlalchemy import Boolean, Column, Integer, String, DateTime, Text, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

from app.db.base_class import Base
from ..utils import _get_date


class Product(Base):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256), index=True)
    description = Column(Text)
    image_thumbnail = Column(String(256))
    image_url = Column(String(256))
    price = Column(Float)
    discount = Column(Float)
    attribute = Column(String(256))
    code_promo = Column(String(256))
    id_category = Column(Integer, ForeignKey("category.id"))
    valid_code_start = Column(DateTime, default=_get_date())
    valid_code_end = Column(DateTime)

    created_at = Column(DateTime, default=_get_date)
    updated_at = Column(DateTime, onupdate=_get_date)

    category = relationship("Category", foreign_keys=[id_category])
