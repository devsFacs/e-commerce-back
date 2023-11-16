from fastapi import APIRouter

from app.api.api_v1.endpoints import (
    login,
    users,
    product,
    category,
    attribute,
    vendors,
    vendors_product,
    user_product,
    product_user_view,
    product_user_like,
    upload,
)

api_router = APIRouter()

api_router.include_router(login.router, tags=["login"])
api_router.include_router(upload.router, tags=["upload"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(product.router, prefix="/product", tags=["product"])
api_router.include_router(category.router, prefix="/category", tags=["category"])
api_router.include_router(attribute.router, prefix="/attribute", tags=["attribute"])
api_router.include_router(vendors.router, prefix="/vendors", tags=["vendors"])
api_router.include_router(
    vendors_product.router, prefix="/vendors_product", tags=["vendors product"]
)
api_router.include_router(
    user_product.router, prefix="/user_product", tags=["user product"]
)
api_router.include_router(
    product_user_view.router, prefix="/product_user_view", tags=["product user view"]
)
api_router.include_router(
    product_user_like.router, prefix="/product_user_like", tags=["product user like"]
)
