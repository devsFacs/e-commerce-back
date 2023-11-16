from typing import Optional

from app.crud.base import CRUDBase
from app.models.attribute import Attribute
from app.schemas.attribute import AttributeCreate, AttributeUpdate
from sqlalchemy.orm import Session


class CRUDAttribute(CRUDBase[Attribute, AttributeCreate, AttributeUpdate]):
    def get_by_name(self, db: Session, *, name: str) -> Optional[Attribute]:
        return db.query(Attribute).filter(Attribute.name == name).first()


attribute = CRUDAttribute(Attribute)
