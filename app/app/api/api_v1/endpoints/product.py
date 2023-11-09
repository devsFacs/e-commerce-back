from typing import Any, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/get_all/", response_model=schemas.ResponseProduct)
def read_products(
        db: Session = Depends(deps.get_db),
        offset: int = Query(0, description="Offset for pagination"),
        limit: int = Query(100, description="Limit for pagination"),
        wheres: List[Any] = Query([], description="Filter conditions"),
        order: str = "ASC",
        order_by: str = "name",
        current_user: models.Product = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve products.
    """
    products = crud.product.get_multi(db=db, limit=limit, skip=offset, order_by=order_by, order=order, where=wheres)
    count = crud.product.get_count(db=db)
    response = schemas.ResponseProduct(**{'count': count, 'data': products})
    return response


@router.post("/", response_model=schemas.Product)
def create_product(
        *,
        db: Session = Depends(deps.get_db),
        product_in: schemas.ProductCreate,
        current_user: models.Product = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new product.
    """
    product = crud.product.create(db, obj_in=product_in)
    return product


@router.get("/by_id/", response_model=schemas.Product)
def read_product_by_id(
        product_id: int,
        current_user: models.Product = Depends(deps.get_current_active_user),
        db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific product by id.
    """
    product = crud.product.get(db=db, id=product_id)
    if not product:
        raise HTTPException(
            status_code=400, detail="Product not found"
        )
    return product


@router.put("/", response_model=schemas.Product)
def update_product(
        *,
        db: Session = Depends(deps.get_db),
        product_id: str,
        product_in: schemas.ProductUpdate,
        current_user: models.Product = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a product.
    """
    product = crud.product.get(db, id=product_id)
    if not product:
        raise HTTPException(
            status_code=404,
            detail="The product with this product id does not exist in the system",
        )
    product = crud.product.update(db, db_obj=product, obj_in=product_in)
    return product


@router.delete("/", response_model=Any)
def delete_product(
        *,
        db: Session = Depends(deps.get_db),
        id_product: str,
        current_user: models.Product = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an product.
    """
    product = crud.product.get(db=db, id=id_product)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if not crud.product.is_superproduct(current_user):
        vendors = crud.vendors.get_by_user(db=db, id_user=current_user.id)
        if not vendors:
            raise HTTPException(status_code=400, detail="Not enough permissions")
        my_product = crud.product_vendors.get_by_id_product_and_vendors(
            db=db, id_product=id_product, id_vendors=vendors.id)
        product_details = crud.product_details.get_by_id_product(db=db, id_product=id_product)
        product_user_view = crud.product_user_view.get_by_product(db=db, id_product=id_product)
        product_user_like = crud.product_user_like.get_by_product(db=db, id_product=id_product)
        if len(product_details) > 0 or len(product_user_view) > 0 or len(product_user_like) > 0:
            raise HTTPException(status_code=400, detail="Cannot delete product")

        if my_product:
            crud.product.remove(db=db, id=id_product)

    return product
