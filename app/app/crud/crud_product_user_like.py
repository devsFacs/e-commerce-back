from typing import Optional

from app.crud.base import CRUDBase
from app.models.product_user_like import ProductUserLike
from app.schemas.product_user_like import ProductUserLikeCreate, ProductUserLikeUpdate
from sqlalchemy.orm import Session
from sqlalchemy import and_


class CRUDProductUserLike(
    CRUDBase[ProductUserLike, ProductUserLikeCreate, ProductUserLikeUpdate]
):
    def get_by_user(self, db: Session, *, id_user: str) -> Optional[ProductUserLike]:
        return (
            db.query(ProductUserLike).filter(ProductUserLike.id_user == id_user).all()
        )

    def get_by_user_and_product(
        self, db: Session, *, id_user: str, id_product
    ) -> Optional[ProductUserLike]:
        return (
            db.query(ProductUserLike)
            .filter(
                and_(
                    ProductUserLike.id_user == id_user,
                    ProductUserLike.id_product == id_product,
                )
            )
            .first()
        )

    def get_by_product(
        self, db: Session, *, id_product: str
    ) -> Optional[ProductUserLike]:
        return (
            db.query(ProductUserLike)
            .filter(ProductUserLike.id_product == id_product)
            .all()
        )


product_user_like = CRUDProductUserLike(ProductUserLike)
