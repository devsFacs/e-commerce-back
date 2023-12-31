from typing import Any, Dict, Optional, Union, List

from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def get_by_email_and_id_google(
        self, db: Session, *, email: str, id_google: str
    ) -> Optional[User]:
        return (
            db.query(User)
            .filter(and_(User.email == email, User.id_google == id_google))
            .first()
        )

    def get_by_email_and_id_facebook(
        self, db: Session, *, email: str, id_facebook: str
    ) -> Optional[User]:
        return (
            db.query(User)
            .filter(and_(User.email == email, User.id_facebook == id_facebook))
            .first()
        )

    def get_by_name(self, db: Session, *, name: str) -> Optional[User]:
        return db.query(User).filter(User.name == name).first()

    def get_supperadmin(self, db: Session) -> Optional[User]:
        return db.query(User).filter(User.is_superuser == True).first()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        db_obj = User(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            first_name=obj_in.first_name,
            last_name=obj_in.last_name,
            mobile=obj_in.mobile,
            is_vendors=obj_in.is_vendors,
            is_active=obj_in.is_active,
            address=obj_in.address,
            id_google=obj_in.id_google,
            sex=obj_in.sex,
            id_facebook=obj_in.id_facebook,
            is_superuser=obj_in.is_superuser,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if "password" in update_data:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[User]:
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def authenticate_google(
        self, db: Session, *, email: str, id_google: str
    ) -> Optional[User]:
        user = self.get_by_email_and_id_google(db, email=email, id_google=id_google)
        if not user:
            return None
        return user

    def authenticate_facebook(
        self, db: Session, *, email: str, id_facebook: str
    ) -> Optional[User]:
        user = self.get_by_email_and_id_facebook(
            db, email=email, id_facebook=id_facebook
        )
        if not user:
            return None
        return user

    def is_active(self, user: User) -> bool:
        return user.is_active

    def is_superuser(self, user: User) -> bool:
        return user.is_superuser

    def is_vendor(self, user: User) -> bool:
        return user.is_vendors


user = CRUDUser(User)
