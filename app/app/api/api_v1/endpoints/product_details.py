from typing import Any, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/get_all/", response_model=schemas.ResponseProductDetails)
def read_product_details(
        db: Session = Depends(deps.get_db),
        offset: int = Query(0, description="Offset for pagination"),
        limit: int = Query(100, description="Limit for pagination"),
        wheres: List[Any] = Query([], description="Filter conditions"),
        order: str = "ASC",
        current_user: models.ProductDetails = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve product_details.
    """
    product_details = crud.product_details.get_multi(db=db, limit=limit, skip=offset, order=order, where=wheres)
    count = crud.product_details.get_count(db=db)
    response = schemas.ResponseProductDetails(**{'count': count, 'data': product_details})
    return response


@router.post("/", response_model=schemas.ProductDetails)
def create_product_details(
        *,
        db: Session = Depends(deps.get_db),
        product_details_in: schemas.ProductDetailsCreate,
        current_user: models.ProductDetails = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new product_details.
    """
    product_details = crud.product_details.create(db, obj_in=product_details_in)
    return product_details


@router.get("/by_id/", response_model=schemas.ProductDetails)
def read_product_details_by_id(
        product_details_id: int,
        current_user: models.ProductDetails = Depends(deps.get_current_active_user),
        db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific product_details by id.
    """
    product_details = crud.product_details.get(db=db, id=product_details_id)
    if not product_details:
        raise HTTPException(
            status_code=400, detail="ProductDetails not found"
        )
    return product_details


@router.put("/", response_model=schemas.ProductDetails)
def update_product_details(
        *,
        db: Session = Depends(deps.get_db),
        product_details_id: str,
        product_details_in: schemas.ProductDetailsUpdate,
        current_user: models.ProductDetails = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a product_details.
    """
    product_details = crud.product_details.get(db, id=product_details_id)
    if not product_details:
        raise HTTPException(
            status_code=404,
            detail="product_details not found",
        )
    product_details = crud.product_details.update(db, db_obj=product_details, obj_in=product_details_in)
    return product_details


@router.delete("/", response_model=Any)
def delete_product_details(
        *,
        db: Session = Depends(deps.get_db),
        id_product_details: str,
        current_user: models.ProductDetails = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an product_details.
    """
    product_details = crud.product_details.get(db=db, id=id_product_details)

    if not product_details:
        raise HTTPException(status_code=404, detail="ProductDetails not found")
    if not crud.product_details.is_superproduct_details(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    crud.product_details.remove(db=db, id=id_product_details)

    return product_details
