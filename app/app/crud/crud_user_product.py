from typing import Optional

from app.crud.base import CRUDBase
from app.models.user_product import UserProduct
from app.schemas.user_product import UserProductCreate, UserProductUpdate
from sqlalchemy.orm import Session


class CRUDUserProduct(CRUDBase[UserProduct, UserProductCreate, UserProductUpdate]):

    def get_by_user(self, db: Session, *, id_user: str) -> Optional[UserProduct]:
        return db.query(UserProduct).filter(UserProduct.id_user == id_user).all()


user_product = CRUDUserProduct(UserProduct)
