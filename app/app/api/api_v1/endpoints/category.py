from typing import Any, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/get_all/", response_model=schemas.ResponseCategory)
def read_categorys(
        db: Session = Depends(deps.get_db),
        offset: int = Query(0, description="Offset for pagination"),
        limit: int = Query(100, description="Limit for pagination"),
        wheres: List[Any] = Query([], description="Filter conditions"),
        order: str = "ASC",
        order_by: str = "name",
        current_user: models.Category = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve category.
    """
    category = crud.category.get_multi(db=db, limit=limit, skip=offset, order_by=order_by, order=order, where=wheres)
    count = crud.category.get_count(db=db)
    response = schemas.ResponseCategory(**{'count': count, 'data': category})
    return response


@router.post("/", response_model=schemas.Category)
def create_category(
        *,
        db: Session = Depends(deps.get_db),
        category_in: schemas.CategoryCreate,
        current_user: models.Category = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new category.
    """
    category = crud.category.create(db, obj_in=category_in)
    return category


@router.get("/by_id/", response_model=schemas.Category)
def read_category_by_id(
        category_id: int,
        current_user: models.Category = Depends(deps.get_current_active_user),
        db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific category by id.
    """
    category = crud.category.get(db=db, id=category_id)
    if not category:
        raise HTTPException(
            status_code=400, detail="Category not found"
        )
    return category


@router.put("/", response_model=schemas.Category)
def update_category(
        *,
        db: Session = Depends(deps.get_db),
        category_id: str,
        category_in: schemas.CategoryUpdate,
        current_user: models.Category = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a category.
    """
    category = crud.category.get(db, id=category_id)
    if not category:
        raise HTTPException(
            status_code=404,
            detail="category not found",
        )
    category = crud.category.update(db, db_obj=category, obj_in=category_in)
    return category


@router.delete("/", response_model=Any)
def delete_category(
        *,
        db: Session = Depends(deps.get_db),
        id_category: str,
        current_user: models.Category = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an category.
    """
    category = crud.category.get(db=db, id=id_category)

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    if not crud.category.is_supercategory(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    crud.category.remove(db=db, id=id_category)

    return category
