from moose_lib import ConsumptionApi
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Define the response model for a Shopify customer
class ShopifyCustomer(BaseModel):
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

# Define the query parameters model
class CustomersByEmailQuery(BaseModel):
    email: Optional[str] = None
    limit: Optional[int] = 10

# Query handler to get customers by email; returns rows validated against ShopifyCustomer
def get_customers_by_email(client, params: CustomersByEmailQuery):
    """
    Lookup Shopify customers by email address or return all customers with pagination
    
    Args:
        client: Database client for executing queries
        params: Contains email (optional) and limit parameters
        
    Returns:
        CustomersByEmailResponse containing a list of matching customers
    """
    # Set default limit (cap at 100)
    limit = int(min(params.limit or 10, 100))

    # Build LIKE pattern; if no email provided, '%%' returns all
    email_pattern = f"%{params.email or ''}%"

    # Execute parameterized query; Moose validates rows against ShopifyCustomer
    return client.query.execute(
        (
            "SELECT id, email, first_name, last_name, phone, created_at, updated_at, "
            "verified_email, state, address1, address2, city, province, country, zip "
            "FROM shopify_customers "
            "WHERE email LIKE {email} "
            "ORDER BY id "
            "LIMIT {limit}"
        ),
        {"email": email_pattern, "limit": limit},
    )

# Create the consumption API
get_customers_by_email_api = ConsumptionApi[CustomersByEmailQuery, ShopifyCustomer](
    "getCustomersByEmail",
    query_function=get_customers_by_email,
)