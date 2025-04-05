"""Import all routers and add them to routers_list."""
from .admin import admin_router
from .start import start_router
from .products import product_router
routers_list = [
    start_router,
    admin_router,
    product_router
]

__all__ = [
    "routers_list",
]
