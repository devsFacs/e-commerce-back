import ast
import json
from datetime import datetime
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union, Tuple

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import text, and_, extract, func

from app.db.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(
            self, db: Session, *, skip: int = 0, limit: int = 100, order_by: str = "id", where: Any = None,
            order: str = 'DESC', user_id: int = 0, column: str = 'id_user'
    ) -> List[Any]:
        query = db.query(self.model)
        if where is not None and where != [] and where != ['']:
            where = list(where[0].replace('},', '};').split(';'))
            if user_id == 0:
                conditions = []
            else:
                conditions = [getattr(self.model, column) == user_id]
            for condition in where:
                condition = json.loads(condition)
                column_name = condition['key']
                operator = condition['operator']
                value = condition['value']
                filter_condition = None
                if operator == "==":
                    filter_condition = getattr(self.model, column_name) == value
                elif operator == ">":
                    filter_condition = getattr(self.model, column_name) > value
                elif operator == "<":
                    filter_condition = getattr(self.model, column_name) < value
                elif operator == "like":
                    filter_condition = getattr(self.model, column_name).like('%' + value + '%')
                if filter_condition is not None:
                    conditions.append(filter_condition)

            query = query.filter(and_(*conditions))
        result = query.order_by(text(f'{order_by} {order}')).offset(skip).limit(limit).all()
        return result

    def get_count(
            self, db: Session, where: List[Any] = None, user_id: int = 0, column: str = 'id_user'
    ) -> int:
        query = db.query(self.model)
        if where is not None and where != [] and where != ['']:
            where = list(where[0].replace('},', '};').split(';'))
            if user_id == 0:
                conditions = []
            else:
                conditions = [getattr(self.model, column) == user_id]
            for condition in where:
                condition = json.loads(condition)
                column_name = condition['key']
                operator = condition['operator']
                value = condition['value']
                filter_condition = None
                if operator == "==":
                    filter_condition = getattr(self.model, column_name) == value
                elif operator == ">":
                    filter_condition = getattr(self.model, column_name) > value
                elif operator == "<":
                    filter_condition = getattr(self.model, column_name) < value
                elif operator == "like":
                    filter_condition = getattr(self.model, column_name).like('%' + value + '%')
                if filter_condition is not None:
                    conditions.append(filter_condition)
            query = query.filter(and_(*conditions))
        result = query.all()
        return len(result)

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
            self,
            db: Session,
            *,
            db_obj: ModelType,
            obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data and field is not None:
                setattr(db_obj, field, update_data[field])

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> ModelType:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj
