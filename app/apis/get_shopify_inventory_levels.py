from moose_lib import ConsumptionApi
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class InventoryLevelsQuery(BaseModel):
    limit: Optional[int] = 100

class InventoryLevelsResponse(BaseModel):
    sku: str
    tracked: bool
    available: float
    location_id: str
    location_name: Optional[str]
    updated_at: datetime

def get_shopify_inventory_levels_query(client, params: InventoryLevelsQuery):
    """Query function for retrieving Shopify inventory levels (parameterized)."""
    return client.query.execute(
        (
            "SELECT sku, tracked, available, location_id, location_name, updated_at "
            "FROM shopify_inventory_levels "
            "ORDER BY updated_at DESC "
            "LIMIT {limit}"
        ),
        {"limit": int(params.limit or 100)},
    )

get_shopify_inventory_levels = ConsumptionApi[InventoryLevelsQuery, InventoryLevelsResponse](
    name="getShopifyInventoryLevels",
    query_function=get_shopify_inventory_levels_query
)