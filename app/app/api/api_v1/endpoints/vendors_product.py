from typing import Any, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/get_all/", response_model=schemas.ResponseVendorsProduct)
def read_vendors_products(
        db: Session = Depends(deps.get_db),
        offset: int = Query(0, description="Offset for pagination"),
        limit: int = Query(100, description="Limit for pagination"),
        wheres: List[Any] = Query([], description="Filter conditions"),
        order: str = "ASC",
        order_by: str = "name",
        current_user: models.VendorsProduct = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve vendors_product.
    """
    vendor = crud.vendors.get_by_user(db=db, id_user=current_user.id)
    if vendor:
        vendors_product = crud.vendors_product.get_multi(
            db=db, limit=limit, skip=offset, order_by=order_by, order=order, where=wheres,
            user_id=vendor.id, column='id_vendors')
    else:
        vendors_product = crud.vendors_product.get_multi(
            db=db, limit=limit, skip=offset, order_by=order_by, order=order, where=wheres)
    count = crud.vendors_product.get_count(db=db)
    response = schemas.ResponseVendorsProduct(**{'count': count, 'data': vendors_product})
    return response


@router.post("/", response_model=schemas.VendorsProduct)
def create_vendors_product(
        *,
        db: Session = Depends(deps.get_db),
        vendors_product_in: schemas.VendorsProductCreate,
        current_user: models.VendorsProduct = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new vendors_product.
    """
    vendor = crud.vendors.get_by_user(db=db, id_user=current_user.id)
    if not vendor:
        raise HTTPException(
            status_code=400, detail="You are not vendor"
        )
    vendors_product_in.id_vendor = vendor.id
    vendors_product = crud.vendors_product.create(db, obj_in=vendors_product_in)
    return vendors_product


@router.get("/by_id/", response_model=schemas.VendorsProduct)
def read_vendors_product_by_id(
        vendors_product_id: int,
        current_user: models.VendorsProduct = Depends(deps.get_current_active_user),
        db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific vendors_product by id.
    """
    vendors_product = crud.vendors_product.get(db=db, id=vendors_product_id)
    if not vendors_product:
        raise HTTPException(
            status_code=400, detail="VendorsProduct not found"
        )
    return vendors_product


@router.put("/", response_model=schemas.VendorsProduct)
def update_vendors_product(
        *,
        db: Session = Depends(deps.get_db),
        vendors_product_id: str,
        vendors_product_in: schemas.VendorsProductUpdate,
        current_user: models.VendorsProduct = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a vendors_product.
    """
    vendors_product = crud.vendors_product.get(db, id=vendors_product_id)
    if not vendors_product:
        raise HTTPException(
            status_code=404,
            detail="vendors_product not found",
        )
    vendors_product = crud.vendors_product.update(db, db_obj=vendors_product, obj_in=vendors_product_in)
    return vendors_product


@router.delete("/", response_model=Any)
def delete_vendors_product(
        *,
        db: Session = Depends(deps.get_db),
        id_vendors_product: str,
        current_user: models.VendorsProduct = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an vendors_product.
    """
    vendors_product = crud.vendors_product.get(db=db, id=id_vendors_product)

    if not vendors_product:
        raise HTTPException(status_code=404, detail="VendorsProduct not found")
    if not crud.vendors_product.is_supervendors_product(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    crud.vendors_product.remove(db=db, id=id_vendors_product)

    return vendors_product
