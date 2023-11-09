from .crud_user import user
from .crud_product import product
from .crud_category import category
from .crud_user_product import user_product
from .crud_vendor import vendors
from .crud_product_details import product_details
from .crud_product_user_view import product_user_view
from .crud_product_user_like import product_user_like
from .crud_vendors_product import vendors_product
# For a new basic set of CRUD operations you could just do

# from .base import CRUDBase
# from app.models.item import Item
# from app.schemas.item import ItemCreate, ItemUpdate

# item = CRUDBase[Item, ItemCreate, ItemUpdate](Item)
