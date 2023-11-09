from typing import Optional

from app.crud.base import CRUDBase
from app.models.product_user_view import ProductUserView
from app.schemas.product_user_view import ProductUserViewCreate, ProductUserViewUpdate
from sqlalchemy.orm import Session


class CRUDProductUserView(CRUDBase[ProductUserView, ProductUserViewCreate, ProductUserViewUpdate]):

    def get_by_user(self, db: Session, *, id_user: str) -> Optional[ProductUserView]:
        return db.query(ProductUserView).filter(ProductUserView.id_user == id_user).all()

    def get_by_product(self, db: Session, *, id_product: str) -> Optional[ProductUserView]:
        return db.query(ProductUserView).filter(ProductUserView.id_product == id_product).all()


product_user_view = CRUDProductUserView(ProductUserView)
