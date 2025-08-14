from moose_lib import ConsumptionApi
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Customer Lookup API - by email or ID
class CustomerLookupQuery(BaseModel):
    email: Optional[str] = None
    customer_id: Optional[str] = None
    limit: Optional[int] = 100

class CustomerResponse(BaseModel):
    id: str
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    verified_email: Optional[bool] = None
    state: Optional[str] = None
    address1: Optional[str] = None
    address2: Optional[str] = None
    city: Optional[str] = None
    province: Optional[str] = None
    country: Optional[str] = None
    zip: Optional[str] = None

def get_customer_lookup_query(client, params: CustomerLookupQuery):
    """Query function for customer lookup by email or ID (parameterized)."""
    where_sql_parts = []
    args = {"limit": params.limit or 100}
    if params.email:
        where_sql_parts.append("email = {email}")
        args["email"] = params.email
    if params.customer_id:
        where_sql_parts.append("id = {customer_id}")
        args["customer_id"] = params.customer_id
    where_clause = f"WHERE {' AND '.join(where_sql_parts)}" if where_sql_parts else ""
    return client.query.execute(
        (
            "SELECT id, email, first_name, last_name, phone, created_at, updated_at, "
            "verified_email, state, address1, address2, city, province, country, zip "
            "FROM shopify_customers "
            f"{where_clause} "
            "ORDER BY id "
            "LIMIT {limit}"
        ),
        {**args, "limit": int(args["limit"])},
    )

# Customer Segmentation API - by location
class CustomerSegmentationQuery(BaseModel):
    city: Optional[str] = None
    province: Optional[str] = None
    country: Optional[str] = None
    limit: Optional[int] = 100

def get_customer_segmentation_query(client, params: CustomerSegmentationQuery):
    """Query function for customer segmentation by location (parameterized)."""
    where_sql_parts = []
    args = {"limit": params.limit or 100}
    if params.city:
        where_sql_parts.append("city = {city}")
        args["city"] = params.city
    if params.province:
        where_sql_parts.append("province = {province}")
        args["province"] = params.province
    if params.country:
        where_sql_parts.append("country = {country}")
        args["country"] = params.country
    where_clause = f"WHERE {' AND '.join(where_sql_parts)}" if where_sql_parts else ""
    return client.query.execute(
        (
            "SELECT id, email, first_name, last_name, phone, created_at, updated_at, "
            "verified_email, state, address1, address2, city, province, country, zip "
            "FROM shopify_customers "
            f"{where_clause} "
            "ORDER BY id "
            "LIMIT {limit}"
        ),
        {**args, "limit": int(args["limit"])},
    )

# Customer Activity API - recent customers by created_at
class CustomerActivityQuery(BaseModel):
    days_back: Optional[int] = 30
    limit: Optional[int] = 100

def get_customer_activity_query(client, params: CustomerActivityQuery):
    """Query function for recent customer activity (parameterized)."""
    return client.query.execute(
        (
            "SELECT id, email, first_name, last_name, phone, created_at, updated_at, "
            "verified_email, state, address1, address2, city, province, country, zip "
            "FROM shopify_customers "
            "WHERE created_at >= now() - INTERVAL {days_back} DAY "
            "ORDER BY created_at DESC "
            "LIMIT {limit}"
        ),
        {"days_back": int(params.days_back or 30), "limit": int(params.limit or 100)},
    )

# Create the three consumption APIs
get_shopify_customer_lookup = ConsumptionApi[CustomerLookupQuery, CustomerResponse](
    name="getShopifyCustomerLookup",
    query_function=get_customer_lookup_query
)

get_shopify_customer_segmentation = ConsumptionApi[CustomerSegmentationQuery, CustomerResponse](
    name="getShopifyCustomerSegmentation", 
    query_function=get_customer_segmentation_query
)

get_shopify_customer_activity = ConsumptionApi[CustomerActivityQuery, CustomerResponse](
    name="getShopifyCustomerActivity",
    query_function=get_customer_activity_query
)

