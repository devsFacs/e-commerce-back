# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base  # noqa
from app.models.user import User  # noqa
from app.models.category import Category  # noqa
from app.models.attribute import Attribute  # noqa
from app.models.product import Product  # noqa
from app.models.user_product import UserProduct  # noqa
from app.models.product_user_view import ProductUserView  # noqa
from app.models.product_user_like import ProductUserLike  # noqa
from app.models.vendors import Vendors  # noqa
from app.models.vendors_product import VendorsProduct  # noqa
