from typing import Optional

from app.crud.base import CRUDBase
from app.models.vendors_product import VendorsProduct
from app.schemas.vendors_product import VendorsProductCreate, VendorsProductUpdate
from sqlalchemy.orm import Session
from sqlalchemy import and_


class CRUDVendorsProduct(
    CRUDBase[VendorsProduct, VendorsProductCreate, VendorsProductUpdate]
):
    def get_by_id_product(
        self, db: Session, *, id_product: str
    ) -> Optional[VendorsProduct]:
        return (
            db.query(VendorsProduct)
            .filter(VendorsProduct.id_product == id_product)
            .first()
        )

    def get_by_id_product_and_vendors(
        self, db: Session, *, id_product: int, id_vendors: int
    ) -> Optional[VendorsProduct]:
        return (
            db.query(VendorsProduct)
            .filter(
                and_(
                    VendorsProduct.id_product == id_product,
                    VendorsProduct.id_vendor == id_vendors,
                )
            )
            .first()
        )

    def get_by_id_vendors(
        self, db: Session, *, id_vendors: str, limit: int, skip: int
    ) -> Optional[VendorsProduct]:
        return (
            db.query(VendorsProduct)
            .filter(VendorsProduct.id_vendor == id_vendors)
            .offset(skip)
            .limit(limit)
            .all()
        )


vendors_product = CRUDVendorsProduct(VendorsProduct)
