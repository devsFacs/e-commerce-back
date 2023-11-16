import ast
import json
from datetime import datetime
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union, Tuple

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import text, and_, extract, func, asc, desc

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

    def get_condition_deep(self, condition):
        column_name = condition["key"]
        operator = condition["operator"]
        value = condition.get("value", None)
        parts = column_name.split(".")
        attrs = []
        filter_condition = None
        previous_model = self.model
        for i in range(0, len(parts)):

            if i < len(parts) - 1:
                attr = getattr(previous_model, parts[i])
                attrs.append(attr)
                previous_model = attr.property.mapper.class_
            else:
                if operator == "==":
                    filter_condition = getattr(previous_model, parts[i]) == value
                elif operator == "!=":
                    filter_condition = getattr(previous_model, parts[i]) != value
                elif operator == ">":
                    filter_condition = getattr(previous_model, parts[i]) > value
                elif operator == "<":
                    filter_condition = getattr(previous_model, parts[i]) < value
                elif operator == "like":
                    filter_condition = getattr(previous_model, parts[i]).like(
                        "%" + value + "%"
                    )
                elif operator == "month":
                    if value is None:
                        filter_condition = extract(
                            "month", getattr(previous_model, parts[i])
                        ).is_(None)
                    else:
                        filter_condition = (
                            extract("month", getattr(previous_model, parts[i])) == value
                        )
                elif operator == "date":
                    date_value = datetime.strptime(value, "%Y-%m-%d").date()
                    filter_condition = (
                        func.date(getattr(previous_model, parts[i])) == date_value
                    )
                elif operator == "between_date":
                    date_split = value.split(",")
                    date_1 = datetime.strptime(date_split[0], "%Y-%m-%d").date()
                    date_2 = datetime.strptime(date_split[1], "%Y-%m-%d").date()
                    filter_condition = func.date(
                        getattr(previous_model, parts[i])
                    ).between(date_1, date_2)
                elif operator == "year":
                    if value is None:
                        filter_condition = extract(
                            "year", getattr(previous_model, parts[i])
                        ).is_(None)
                    else:
                        filter_condition = (
                            extract("year", getattr(previous_model, parts[i])) == value
                        )
                elif operator == "week":
                    if value is None:
                        filter_condition = extract(
                            "week", getattr(previous_model, parts[i])
                        ).is_(None)
                    else:
                        filter_condition = (
                            extract("week", getattr(previous_model, parts[i])) == value
                        )
                elif operator == "isNull":
                    filter_condition = getattr(previous_model, parts[i]).is_(None)
                elif operator == "isNotNull":
                    filter_condition = getattr(previous_model, parts[i]).isnot(None)
                elif operator == "notIn":
                    filter_condition = getattr(previous_model, parts[i]).notin_(value)
                elif operator == "in":
                    filter_condition = getattr(previous_model, parts[i]).in_(value)

        attrs.reverse()
        if filter_condition is not None:
            for attr in attrs:
                try:
                    filter_condition = attr.has(filter_condition)
                except:
                    filter_condition = attr.any(filter_condition)
        return filter_condition

    def get_joined_load(self, column_name):
        parts = column_name.split(".")
        previous_model = self.model
        result = None
        for i in range(0, len(parts)):
            attr = getattr(previous_model, parts[i])
            if result:
                result = result.joinedload(attr)
            else:
                result = joinedload(attr)
            if i < len(parts) - 1:
                previous_model = attr.property.mapper.class_
        return result

    def get_all_relations(self, relations: List):
        return [self.get_joined_load(x) for x in relations]

    def get_multi_where_array(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        order_by: str = "id",
        where: Any = None,
        order: str = "DESC",
        resource: str = "",
        relations=None,
    ) -> List[ModelType]:
        query = db.query(self.model)
        if where is not None:
            conditions = []
            for condition in where:
                filter_condition = self.get_condition_deep(condition)
                if filter_condition is not None:
                    conditions.append(filter_condition)
            query = query.filter(and_(*conditions))
            if relations is not None and len(relations) > 0:
                query = query.options(*(self.get_all_relations(relations)))

        order_function = asc
        if order == "DESC":
            order_function = desc
        result = (
            query.order_by(
                order_function(getattr(self.model, order_by)),
                desc(getattr(self.model, "id")),
            )
            .offset(skip)
            .limit(limit)
            .all()
        )

        return result

    def get_multi(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        order_by: str = "id",
        where: Any = None,
        order: str = "DESC",
        user_id: int = 0,
        column: str = "id_user",
    ) -> List[Any]:
        query = db.query(self.model)
        if where is not None and where != [] and where != [""]:
            where = list(where[0].replace("},", "};").split(";"))
            if user_id == 0:
                conditions = []
            else:
                conditions = [getattr(self.model, column) == user_id]
            for condition in where:
                condition = json.loads(condition)
                column_name = condition["key"]
                operator = condition["operator"]
                value = condition["value"]
                filter_condition = None
                if operator == "==":
                    filter_condition = getattr(self.model, column_name) == value
                elif operator == ">":
                    filter_condition = getattr(self.model, column_name) > value
                elif operator == "<":
                    filter_condition = getattr(self.model, column_name) < value
                elif operator == "like":
                    filter_condition = getattr(self.model, column_name).like(
                        "%" + value + "%"
                    )
                if filter_condition is not None:
                    conditions.append(filter_condition)

            query = query.filter(and_(*conditions))
        result = (
            query.order_by(text(f"{order_by} {order}")).offset(skip).limit(limit).all()
        )
        return result

    def get_count_where_array(self, db: Session, where: Any = None) -> int:
        query = db.query(self.model)
        if where is not None:
            conditions = []
            for condition in where:
                filter_condition = self.get_condition_deep(condition)
                if filter_condition is not None:
                    conditions.append(filter_condition)

            query = query.filter(and_(*conditions))
        result = query.all()
        return len(result)

    def get_count(
        self,
        db: Session,
        where: List[Any] = None,
        user_id: int = 0,
        column: str = "id_user",
    ) -> int:
        query = db.query(self.model)
        if where is not None and where != [] and where != [""]:
            where = list(where[0].replace("},", "};").split(";"))
            if user_id == 0:
                conditions = []
            else:
                conditions = [getattr(self.model, column) == user_id]
            for condition in where:
                condition = json.loads(condition)
                column_name = condition["key"]
                operator = condition["operator"]
                value = condition["value"]
                filter_condition = None
                if operator == "==":
                    filter_condition = getattr(self.model, column_name) == value
                elif operator == ">":
                    filter_condition = getattr(self.model, column_name) > value
                elif operator == "<":
                    filter_condition = getattr(self.model, column_name) < value
                elif operator == "like":
                    filter_condition = getattr(self.model, column_name).like(
                        "%" + value + "%"
                    )
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
        obj_in: Union[UpdateSchemaType, Dict[str, Any]],
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
