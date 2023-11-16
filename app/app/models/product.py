from sqlalchemy import Boolean, Column, Integer, String, DateTime, Text, Float, ARRAY
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
    id_attribute = Column(Integer, ForeignKey("attribute.id"))
    id_category = Column(Integer, ForeignKey("category.id"))
    colors_disp = Column(String(256))
    size_disp = Column(String(256))

    created_at = Column(DateTime, default=_get_date)
    updated_at = Column(DateTime, onupdate=_get_date)

    category = relationship("Category", foreign_keys=[id_category])
    attribute = relationship("Attribute", foreign_keys=[id_attribute])
