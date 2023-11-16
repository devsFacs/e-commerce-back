from sqlalchemy import Boolean, Column, Integer, String, DateTime, Text, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

from app.db.base_class import Base
from ..utils import _get_date


class Attribute(Base):
    __tablename__ = "attribute"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256), index=True)
    description = Column(Text)

    created_at = Column(DateTime, default=_get_date)
    updated_at = Column(DateTime, onupdate=_get_date)
