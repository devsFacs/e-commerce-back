from typing import Any, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/get_all/", response_model=schemas.ResponseAttribute)
def read_attributes(
    db: Session = Depends(deps.get_db),
    offset: int = Query(0, description="Offset for pagination"),
    limit: int = Query(100, description="Limit for pagination"),
    wheres: List[Any] = Query([], description="Filter conditions"),
    order: str = "ASC",
    order_by: str = "name",
    current_user: models.Attribute = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve attribute.
    """
    attribute = crud.attribute.get_multi(
        db=db, limit=limit, skip=offset, order_by=order_by, order=order, where=wheres
    )
    count = crud.attribute.get_count(db=db)
    response = schemas.ResponseAttribute(**{"count": count, "data": attribute})
    return response


@router.post("/", response_model=schemas.Attribute)
def create_attribute(
    *,
    db: Session = Depends(deps.get_db),
    attribute_in: schemas.AttributeCreate,
    current_user: models.Attribute = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new attribute.
    """
    attribute = crud.attribute.create(db, obj_in=attribute_in)
    return attribute


@router.get("/by_id/", response_model=schemas.Attribute)
def read_attribute_by_id(
    attribute_id: int,
    current_user: models.Attribute = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific attribute by id.
    """
    attribute = crud.attribute.get(db=db, id=attribute_id)
    if not attribute:
        raise HTTPException(status_code=400, detail="Attribute not found")
    return attribute


@router.put("/", response_model=schemas.Attribute)
def update_attribute(
    *,
    db: Session = Depends(deps.get_db),
    attribute_id: str,
    attribute_in: schemas.AttributeUpdate,
    current_user: models.Attribute = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a attribute.
    """
    attribute = crud.attribute.get(db, id=attribute_id)
    if not attribute:
        raise HTTPException(
            status_code=404, detail="attribute not found",
        )
    attribute = crud.attribute.update(db, db_obj=attribute, obj_in=attribute_in)
    return attribute


@router.delete("/", response_model=Any)
def delete_attribute(
    *,
    db: Session = Depends(deps.get_db),
    id_attribute: str,
    current_user: models.Attribute = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an attribute.
    """
    attribute = crud.attribute.get(db=db, id=id_attribute)

    if not attribute:
        raise HTTPException(status_code=404, detail="Attribute not found")
    if not crud.attribute.is_superattribute(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    crud.attribute.remove(db=db, id=id_attribute)

    return attribute
