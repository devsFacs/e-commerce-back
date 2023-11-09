from sqlalchemy import Boolean, Column, Integer, String, DateTime, Text, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

from app.db.base_class import Base
from ..utils import _get_date


class Vendors(Base):
    __tablename__ = "vendors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256))
    address = Column(Text)
    id_user = Column(Integer, ForeignKey("user.id"))
    logo_url = Column(String(256))
    latitude = Column(Float)
    longitude = Column(Float)

    created_at = Column(DateTime, default=_get_date)
    updated_at = Column(DateTime, onupdate=_get_date)

    user = relationship("User", foreign_keys=[id_user])
