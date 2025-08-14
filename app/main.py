"""
Moose Python app entrypoint. Keep imports light to avoid side effects.
Register datamodels, views, and apis here when added.
"""

# Import pipelines so Moose can discover and register them
# Datamodels / Ingest Pipelines
from app.datamodels.shopify_inventory_levels import pipeline as shopify_inventory_levels_pipeline  # noqa: F401
from app.datamodels.shopify_customers import pipeline as shopify_customers_pipeline  # noqa: F401
from app.datamodels.shopify_orders import pipeline as shopify_orders_pipeline  # noqa: F401

# If you add more pipelines or APIs, import them here to ensure they are discoverable






import app.datamodels.shopify_inventory_levels as shopify_inventory_levels_datamodels
import app.datamodels.shopify_customers as shopify_customers_datamodels
import app.datamodels.shopify_orders as shopify_orders_datamodels

import app.apis.__init__ as __init___apis
import app.apis.get_customers_by_email as get_customers_by_email_apis
import app.apis.get_shopify_customers as get_shopify_customers_apis
import app.apis.get_shopify_inventory_levels as get_shopify_inventory_levels_apis
import app.apis.get_shopify_orders as get_shopify_orders_apis

