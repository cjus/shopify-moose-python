from moose_lib import IngestPipeline, IngestPipelineConfig, OlapConfig
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Shopify Orders data model for ingesting order information

class ShopifyOrders(BaseModel):
    id: str
    name: Optional[str] = None
    order_number: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    processed_at: Optional[datetime] = None
    cancelled_at: Optional[datetime] = None
    closed_at: Optional[datetime] = None
    
    # Financial information
    total_price: Optional[float] = None
    subtotal_price: Optional[float] = None
    total_tax: Optional[float] = None
    total_discounts: Optional[float] = None
    currency: Optional[str] = None
    presentment_currency: Optional[str] = None
    
    # Status fields
    financial_status: Optional[str] = None
    fulfillment_status: Optional[str] = None
    confirmation_number: Optional[str] = None
    
    # Customer information
    customer_id: Optional[str] = None
    customer_email: Optional[str] = None
    customer_phone: Optional[str] = None
    
    # Address information (flattened billing address)
    billing_address1: Optional[str] = None
    billing_address2: Optional[str] = None
    billing_city: Optional[str] = None
    billing_province: Optional[str] = None
    billing_country: Optional[str] = None
    billing_zip: Optional[str] = None
    
    # Address information (flattened shipping address)
    shipping_address1: Optional[str] = None
    shipping_address2: Optional[str] = None
    shipping_city: Optional[str] = None
    shipping_province: Optional[str] = None
    shipping_country: Optional[str] = None
    shipping_zip: Optional[str] = None
    
    # Order metadata
    test: Optional[bool] = None
    tags: Optional[str] = None
    note: Optional[str] = None
    source_name: Optional[str] = None
    referring_site: Optional[str] = None
    
    # Line items summary
    total_line_items_quantity: Optional[int] = None
    line_items_count: Optional[int] = None

config = IngestPipelineConfig(
    table=OlapConfig(
        order_by_fields=["id"],
        deduplicate=True
    ),
    stream=True,
    ingest=True
)

pipeline = IngestPipeline[ShopifyOrders](
    "shopify_orders",
    config
)
