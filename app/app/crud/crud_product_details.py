from typing import Optional

from app.crud.base import CRUDBase
from app.models.product_details import ProductDetails
from app.schemas.product_details import ProductDetailsCreate, ProductDetailsUpdate
from sqlalchemy.orm import Session


class CRUDProductDetails(CRUDBase[ProductDetails, ProductDetailsCreate, ProductDetailsUpdate]):

    def get_by_id_product(self, db: Session, *, id_product: str) -> Optional[ProductDetails]:
        return db.query(ProductDetails).filter(ProductDetails.id_product == id_product).all()


product_details = CRUDProductDetails(ProductDetails)
