from sqlalchemy import Boolean, Column, Integer, String, Date, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

from app.db.base_class import Base
from ..utils import _get_date


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(256), index=True)
    last_name = Column(String(256))
    mobile = Column(String(256))
    address = Column(Text)
    sex = Column(String(30))
    email = Column(String(256), unique=True, index=True, nullable=False)
    hashed_password = Column(String(256), nullable=False)
    id_google = Column(String(256))
    id_facebook = Column(String(256))
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    is_vendors = Column(Boolean(), default=False)

    created_at = Column(Date, default=_get_date)
    updated_at = Column(Date, onupdate=_get_date)
