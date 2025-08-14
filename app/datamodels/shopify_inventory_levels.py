from moose_lib import IngestPipeline, IngestPipelineConfig, OlapConfig
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ShopifyInventoryLevels(BaseModel):
    sku: Optional[str] = None
    location_id: str
    updated_at: Optional[datetime] = None
    available: Optional[float] = None
    tracked: bool
    location_name: Optional[str] = None

config = IngestPipelineConfig(
    table=OlapConfig(
        order_by_fields=["sku", "location_id", "updated_at"],
        deduplicate=True
    ),
    stream=True,
    ingest=True
)

pipeline = IngestPipeline[ShopifyInventoryLevels](
    "shopify_inventory_levels",
    config
)