from typing import Any, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/get_all/", response_model=schemas.ResponseProductUserView)
def read_product_user_views(
        db: Session = Depends(deps.get_db),
        offset: int = Query(0, description="Offset for pagination"),
        limit: int = Query(100, description="Limit for pagination"),
        wheres: List[Any] = Query([], description="Filter conditions"),
        order: str = "ASC",
        order_by: str = "id",
        current_user: models.ProductUserView = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve product_user_view.
    """
    if crud.user.is_superuser(current_user):
        product_user_view = crud.product_user_view.get_multi(
            db=db, limit=limit, skip=offset, order_by=order_by, order=order, where=wheres)
        count = crud.product_user_view.get_count(db=db)
    else:
        product_user_view = crud.product_user_view.get_multi(
            db=db, limit=limit, skip=offset, order_by=order_by, order=order, where=wheres,
            user_id=current_user.id, column='id_user'
        )
        count = crud.product_user_view.get_count(db=db, user_id=current_user.id, column='id_user')

    response = schemas.ResponseProductUserView(**{'count': count, 'data': product_user_view})
    return response


@router.post("/", response_model=schemas.ProductUserView)
def create_product_user_view(
        *,
        db: Session = Depends(deps.get_db),
        product_user_view_in: schemas.ProductUserViewCreate,
        current_user: models.ProductUserView = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new product_user_view.
    """
    product_user_view = crud.product_user_view.create(db, obj_in=product_user_view_in)
    return product_user_view


@router.get("/by_id/", response_model=schemas.ProductUserView)
def read_product_user_view_by_id(
        product_user_view_id: int,
        current_user: models.ProductUserView = Depends(deps.get_current_active_user),
        db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific product_user_view by id.
    """
    product_user_view = crud.product_user_view.get(db=db, id=product_user_view_id)
    if not product_user_view:
        raise HTTPException(
            status_code=400, detail="ProductUserView not found"
        )
    return product_user_view


@router.put("/", response_model=schemas.ProductUserView)
def update_product_user_view(
        *,
        db: Session = Depends(deps.get_db),
        product_user_view_id: str,
        product_user_view_in: schemas.ProductUserViewUpdate,
        current_user: models.ProductUserView = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a product_user_view.
    """
    product_user_view = crud.product_user_view.get(db, id=product_user_view_id)
    if not product_user_view:
        raise HTTPException(
            status_code=404,
            detail="product_user_view not found",
        )
    product_user_view = crud.product_user_view.update(db, db_obj=product_user_view, obj_in=product_user_view_in)
    return product_user_view


@router.delete("/", response_model=Any)
def delete_product_user_view(
        *,
        db: Session = Depends(deps.get_db),
        id_product_user_view: str,
        current_user: models.ProductUserView = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an product_user_view.
    """
    product_user_view = crud.product_user_view.get(db=db, id=id_product_user_view)

    if not product_user_view:
        raise HTTPException(status_code=404, detail="ProductUserView not found")
    if not crud.product_user_view.is_superproduct_user_view(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    crud.product_user_view.remove(db=db, id=id_product_user_view)

    return product_user_view
