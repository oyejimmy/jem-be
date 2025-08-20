from app.db.base_class import Base

# Import all models so that Base.metadata has them before being used by Alembic or create_all
from app.models.category import Category  # noqa: F401
from app.models.model import Product  # noqa: F401
from app.models.user import User  # noqa: F401
from app.models.order import Order, OrderItem  # noqa: F401


