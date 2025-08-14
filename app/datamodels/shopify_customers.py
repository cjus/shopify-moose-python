from moose_lib import IngestPipeline, IngestPipelineConfig, OlapConfig
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ShopifyCustomers(BaseModel):
    id: str
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    verified_email: Optional[bool] = None
    state: Optional[str] = None
    # Flattened address fields
    address1: Optional[str] = None
    address2: Optional[str] = None
    city: Optional[str] = None
    province: Optional[str] = None
    country: Optional[str] = None
    zip: Optional[str] = None

config = IngestPipelineConfig(
    table=OlapConfig(
        order_by_fields=["id"],
        deduplicate=True
    ),
    stream=True,
    ingest=True
)

pipeline = IngestPipeline[ShopifyCustomers](
    "shopify_customers",
    config
)

