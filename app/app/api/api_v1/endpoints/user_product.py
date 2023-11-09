from typing import Any, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/get_all/", response_model=schemas.ResponseUserProduct)
def read_user_products(
        db: Session = Depends(deps.get_db),
        offset: int = Query(0, description="Offset for pagination"),
        limit: int = Query(100, description="Limit for pagination"),
        wheres: List[Any] = Query([], description="Filter conditions"),
        order: str = "ASC",
        order_by: str = "id",
        current_user: models.UserProduct = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve user_product.
    """
    if crud.user.is_superuser(current_user):
        user_product = crud.user_product.get_multi(
            db=db, limit=limit, skip=offset, order_by=order_by, order=order, where=wheres)
        count = crud.user_product.get_count(db=db)
    else:
        user_product = crud.user_product.get_multi(
            db=db, limit=limit, skip=offset, order_by=order_by, order=order, where=wheres,
            user_id=current_user.id, column='id_user'
        )
        count = crud.user_product.get_count(db=db, user_id=current_user.id, column='id_user')

    response = schemas.ResponseUserProduct(**{'count': count, 'data': user_product})
    return response


@router.post("/", response_model=schemas.UserProduct)
def create_user_product(
        *,
        db: Session = Depends(deps.get_db),
        user_product_in: schemas.UserProductCreate,
        current_user: models.UserProduct = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new user_product.
    """
    user_product = crud.user_product.create(db, obj_in=user_product_in)
    return user_product


@router.get("/by_id/", response_model=schemas.UserProduct)
def read_user_product_by_id(
        user_product_id: int,
        current_user: models.UserProduct = Depends(deps.get_current_active_user),
        db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific user_product by id.
    """
    user_product = crud.user_product.get(db=db, id=user_product_id)
    if not user_product:
        raise HTTPException(
            status_code=400, detail="UserProduct not found"
        )
    return user_product


@router.put("/", response_model=schemas.UserProduct)
def update_user_product(
        *,
        db: Session = Depends(deps.get_db),
        user_product_id: str,
        user_product_in: schemas.UserProductUpdate,
        current_user: models.UserProduct = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a user_product.
    """
    user_product = crud.user_product.get(db, id=user_product_id)
    if not user_product:
        raise HTTPException(
            status_code=404,
            detail="user_product not found",
        )
    user_product = crud.user_product.update(db, db_obj=user_product, obj_in=user_product_in)
    return user_product


@router.delete("/", response_model=Any)
def delete_user_product(
        *,
        db: Session = Depends(deps.get_db),
        id_user_product: str,
        current_user: models.UserProduct = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an user_product.
    """
    user_product = crud.user_product.get(db=db, id=id_user_product)

    if not user_product:
        raise HTTPException(status_code=404, detail="UserProduct not found")
    if not crud.user_product.is_superuser_product(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    crud.user_product.remove(db=db, id=id_user_product)

    return user_product
