from typing import Any, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/get_all/", response_model=schemas.ResponseVendors)
def read_vendorss(
        db: Session = Depends(deps.get_db),
        offset: int = Query(0, description="Offset for pagination"),
        limit: int = Query(100, description="Limit for pagination"),
        wheres: List[Any] = Query([], description="Filter conditions"),
        order: str = "ASC",
        order_by: str = "name",
        current_user: models.Vendors = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve vendors.
    """
    vendors = crud.vendors.get_multi(db=db, limit=limit, skip=offset, order_by=order_by, order=order, where=wheres)
    count = crud.vendors.get_count(db=db)
    response = schemas.ResponseVendors(**{'count': count, 'data': vendors})
    return response


@router.post("/", response_model=schemas.Vendors)
def create_vendors(
        *,
        db: Session = Depends(deps.get_db),
        vendors_in: schemas.VendorsCreate,
) -> Any:
    """
    Create new vendors.
    """
    vendors = crud.vendors.create(db, obj_in=vendors_in)
    return vendors


@router.get("/by_id/", response_model=schemas.Vendors)
def read_vendors_by_id(
        vendors_id: int,
        current_user: models.Vendors = Depends(deps.get_current_active_user),
        db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific vendors by id.
    """
    vendors = crud.vendors.get(db=db, id=vendors_id)
    if not vendors:
        raise HTTPException(
            status_code=400, detail="Vendors not found"
        )
    return vendors


@router.put("/", response_model=schemas.Vendors)
def update_vendors(
        *,
        db: Session = Depends(deps.get_db),
        vendors_id: str,
        vendors_in: schemas.VendorsUpdate,
        current_user: models.Vendors = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a vendors.
    """
    vendors = crud.vendors.get(db, id=vendors_id)
    if not vendors:
        raise HTTPException(
            status_code=404,
            detail="vendors not found",
        )
    vendors = crud.vendors.update(db, db_obj=vendors, obj_in=vendors_in)
    return vendors


@router.delete("/", response_model=Any)
def delete_vendors(
        *,
        db: Session = Depends(deps.get_db),
        id_vendors: str,
        current_user: models.Vendors = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an vendors.
    """
    vendors = crud.vendors.get(db=db, id=id_vendors)

    if not vendors:
        raise HTTPException(status_code=404, detail="Vendors not found")
    if not crud.vendors.is_supervendors(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    crud.vendors.remove(db=db, id=id_vendors)

    return vendors
