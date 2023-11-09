from typing import Optional

from app.crud.base import CRUDBase
from app.models.vendors import Vendors
from app.schemas.vendors import VendorsCreate, VendorsUpdate
from sqlalchemy.orm import Session


class CRUDVendors(CRUDBase[Vendors, VendorsCreate, VendorsUpdate]):

    def get_by_name(self, db: Session, *, name: str) -> Optional[Vendors]:
        return db.query(Vendors).filter(Vendors.name == name).first()

    def get_by_user(self, db: Session, *, id_user: str) -> Optional[Vendors]:
        return db.query(Vendors).filter(Vendors.id_user == id_user).first()


vendors = CRUDVendors(Vendors)
