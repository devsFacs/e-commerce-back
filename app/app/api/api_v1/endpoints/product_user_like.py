from typing import Any, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/get_all/", response_model=schemas.ResponseProductUserLike)
def read_product_user_likes(
    db: Session = Depends(deps.get_db),
    offset: int = Query(0, description="Offset for pagination"),
    limit: int = Query(100, description="Limit for pagination"),
    wheres: List[Any] = Query([], description="Filter conditions"),
    order: str = "ASC",
    order_by: str = "id",
    current_user: models.ProductUserLike = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve product_user_like.
    """
    if crud.user.is_superuser(current_user):
        product_user_like = crud.product_user_like.get_multi(
            db=db,
            limit=limit,
            skip=offset,
            order_by=order_by,
            order=order,
            where=wheres,
        )
        count = crud.product_user_like.get_count(db=db)
    else:
        product_user_like = crud.product_user_like.get_multi(
            db=db,
            limit=limit,
            skip=offset,
            order_by=order_by,
            order=order,
            where=wheres,
            user_id=current_user.id,
            column="id_user",
        )
        count = crud.product_user_like.get_count(
            db=db, user_id=current_user.id, column="id_user"
        )

    response = schemas.ResponseProductUserLike(
        **{"count": count, "data": product_user_like}
    )
    return response


@router.post("/", response_model=schemas.ProductUserLike)
def create_product_user_like(
    *,
    db: Session = Depends(deps.get_db),
    product_user_like_in: schemas.ProductUserLikeCreate,
    current_user: models.ProductUserLike = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new product_user_like.
    """
    product_user_like = crud.product_user_like.create(db, obj_in=product_user_like_in)
    return product_user_like


@router.get("/by_id/", response_model=schemas.ProductUserLike)
def read_product_user_like_by_id(
    product_user_like_id: int,
    current_user: models.ProductUserLike = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific product_user_like by id.
    """
    product_user_like = crud.product_user_like.get(db=db, id=product_user_like_id)
    if not product_user_like:
        raise HTTPException(status_code=400, detail="ProductUserLike not found")
    return product_user_like


@router.put("/", response_model=schemas.ProductUserLike)
def update_product_user_like(
    *,
    db: Session = Depends(deps.get_db),
    product_user_like_id: str,
    product_user_like_in: schemas.ProductUserLikeUpdate,
    current_user: models.ProductUserLike = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a product_user_like.
    """
    product_user_like = crud.product_user_like.get(db, id=product_user_like_id)
    if not product_user_like:
        raise HTTPException(
            status_code=404, detail="product_user_like not found",
        )
    product_user_like = crud.product_user_like.update(
        db, db_obj=product_user_like, obj_in=product_user_like_in
    )
    return product_user_like


@router.delete("/", response_model=Any)
def delete_product_user_like(
    *,
    db: Session = Depends(deps.get_db),
    id_product_user_like: str,
    current_user: models.ProductUserLike = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an product_user_like.
    """
    product_user_like = crud.product_user_like.get(db=db, id=id_product_user_like)

    if not product_user_like:
        raise HTTPException(status_code=404, detail="ProductUserLike not found")
    if not crud.product_user_like.is_superproduct_user_like(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    crud.product_user_like.remove(db=db, id=id_product_user_like)

    return product_user_like
