from moose_lib import ConsumptionApi
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Order Lookup API - by ID or order number
class OrderLookupQuery(BaseModel):
    order_id: Optional[str] = None
    order_number: Optional[str] = None
    name: Optional[str] = None
    limit: Optional[int] = 100

class OrderResponse(BaseModel):
    id: str
    name: Optional[str] = None
    order_number: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    total_price: Optional[float] = None
    currency: Optional[str] = None
    financial_status: Optional[str] = None
    fulfillment_status: Optional[str] = None
    customer_id: Optional[str] = None
    customer_email: Optional[str] = None
    test: Optional[bool] = None
    tags: Optional[str] = None
    note: Optional[str] = None
    billing_city: Optional[str] = None
    billing_province: Optional[str] = None
    billing_country: Optional[str] = None
    shipping_city: Optional[str] = None
    shipping_province: Optional[str] = None
    shipping_country: Optional[str] = None

def get_order_lookup_query(client, params: OrderLookupQuery):
    """Query function for order lookup by ID, order number, or name."""
    where_sql_parts = []
    args = {"limit": params.limit or 100}
    
    if params.order_id:
        where_sql_parts.append("id = {order_id}")
        args["order_id"] = params.order_id
    if params.order_number:
        where_sql_parts.append("order_number = {order_number}")
        args["order_number"] = params.order_number
    if params.name:
        where_sql_parts.append("name = {name}")
        args["name"] = params.name
    
    where_clause = f"WHERE {' AND '.join(where_sql_parts)}" if where_sql_parts else ""
    
    return client.query.execute(
        (
            "SELECT id, name, order_number, created_at, updated_at, total_price, currency, "
            "financial_status, fulfillment_status, customer_id, customer_email, test, tags, note, "
            "billing_city, billing_province, billing_country, shipping_city, shipping_province, shipping_country "
            "FROM shopify_orders "
            f"{where_clause} "
            "ORDER BY created_at DESC "
            "LIMIT {limit}"
        ),
        {**args, "limit": int(args["limit"])},
    )

# Orders by Date Range API
class OrdersByDateQuery(BaseModel):
    start_date: Optional[str] = None  # YYYY-MM-DD format
    end_date: Optional[str] = None    # YYYY-MM-DD format
    days_back: Optional[int] = None   # Alternative to date range
    limit: Optional[int] = 100

def get_orders_by_date_query(client, params: OrdersByDateQuery):
    """Query function for orders by date range or recent days."""
    where_sql_parts = []
    args = {"limit": params.limit or 100}
    
    if params.start_date and params.end_date:
        where_sql_parts.append("created_at >= {start_date} AND created_at <= {end_date}")
        args["start_date"] = params.start_date
        args["end_date"] = params.end_date
    elif params.days_back:
        where_sql_parts.append("created_at >= now() - INTERVAL {days_back} DAY")
        args["days_back"] = int(params.days_back)
    
    where_clause = f"WHERE {' AND '.join(where_sql_parts)}" if where_sql_parts else ""
    
    return client.query.execute(
        (
            "SELECT id, name, order_number, created_at, updated_at, total_price, currency, "
            "financial_status, fulfillment_status, customer_id, customer_email, test, tags, note, "
            "billing_city, billing_province, billing_country, shipping_city, shipping_province, shipping_country "
            "FROM shopify_orders "
            f"{where_clause} "
            "ORDER BY created_at DESC "
            "LIMIT {limit}"
        ),
        {**args, "limit": int(args["limit"])},
    )

# Orders by Customer API
class OrdersByCustomerQuery(BaseModel):
    customer_id: Optional[str] = None
    customer_email: Optional[str] = None
    limit: Optional[int] = 100

def get_orders_by_customer_query(client, params: OrdersByCustomerQuery):
    """Query function for orders by customer ID or email."""
    where_sql_parts = []
    args = {"limit": params.limit or 100}
    
    if params.customer_id:
        where_sql_parts.append("customer_id = {customer_id}")
        args["customer_id"] = params.customer_id
    if params.customer_email:
        where_sql_parts.append("customer_email = {customer_email}")
        args["customer_email"] = params.customer_email
    
    where_clause = f"WHERE {' AND '.join(where_sql_parts)}" if where_sql_parts else ""
    
    return client.query.execute(
        (
            "SELECT id, name, order_number, created_at, updated_at, total_price, currency, "
            "financial_status, fulfillment_status, customer_id, customer_email, test, tags, note, "
            "billing_city, billing_province, billing_country, shipping_city, shipping_province, shipping_country "
            "FROM shopify_orders "
            f"{where_clause} "
            "ORDER BY created_at DESC "
            "LIMIT {limit}"
        ),
        {**args, "limit": int(args["limit"])},
    )

# Orders by Status API
class OrdersByStatusQuery(BaseModel):
    financial_status: Optional[str] = None
    fulfillment_status: Optional[str] = None
    exclude_test: Optional[bool] = True
    limit: Optional[int] = 100

def get_orders_by_status_query(client, params: OrdersByStatusQuery):
    """Query function for orders by financial or fulfillment status."""
    where_sql_parts = []
    args = {"limit": params.limit or 100}
    
    if params.financial_status:
        where_sql_parts.append("financial_status = {financial_status}")
        args["financial_status"] = params.financial_status
    if params.fulfillment_status:
        where_sql_parts.append("fulfillment_status = {fulfillment_status}")
        args["fulfillment_status"] = params.fulfillment_status
    if params.exclude_test:
        where_sql_parts.append("(test = false OR test IS NULL)")
    
    where_clause = f"WHERE {' AND '.join(where_sql_parts)}" if where_sql_parts else ""
    
    return client.query.execute(
        (
            "SELECT id, name, order_number, created_at, updated_at, total_price, currency, "
            "financial_status, fulfillment_status, customer_id, customer_email, test, tags, note, "
            "billing_city, billing_province, billing_country, shipping_city, shipping_province, shipping_country "
            "FROM shopify_orders "
            f"{where_clause} "
            "ORDER BY created_at DESC "
            "LIMIT {limit}"
        ),
        {**args, "limit": int(args["limit"])},
    )

# Order Analytics API - aggregated data
class OrderAnalyticsQuery(BaseModel):
    days_back: Optional[int] = 30
    group_by: Optional[str] = "day"  # day, week, month
    currency: Optional[str] = None

class OrderAnalyticsResponse(BaseModel):
    date_period: str
    total_orders: int
    total_revenue: float
    average_order_value: float
    currency: Optional[str] = None

def get_order_analytics_query(client, params: OrderAnalyticsQuery):
    """Query function for order analytics and aggregations."""
    args = {"days_back": int(params.days_back or 30)}
    
    # Determine date grouping
    date_trunc = "toDate(created_at)"
    if params.group_by == "week":
        date_trunc = "toMonday(created_at)"
    elif params.group_by == "month":
        date_trunc = "toStartOfMonth(created_at)"
    
    currency_filter = ""
    if params.currency:
        currency_filter = "AND currency = {currency}"
        args["currency"] = params.currency
    
    return client.query.execute(
        (
            f"SELECT {date_trunc} as date_period, "
            "count(*) as total_orders, "
            "sum(total_price) as total_revenue, "
            "avg(total_price) as average_order_value, "
            "any(currency) as currency "
            "FROM shopify_orders "
            "WHERE created_at >= now() - INTERVAL {days_back} DAY "
            "AND (test = false OR test IS NULL) "
            f"{currency_filter} "
            "GROUP BY date_period "
            "ORDER BY date_period DESC"
        ),
        args,
    )

# Create the consumption APIs
get_shopify_order_lookup = ConsumptionApi[OrderLookupQuery, OrderResponse](
    name="getShopifyOrderLookup",
    query_function=get_order_lookup_query
)

get_shopify_orders_by_date = ConsumptionApi[OrdersByDateQuery, OrderResponse](
    name="getShopifyOrdersByDate",
    query_function=get_orders_by_date_query
)

get_shopify_orders_by_customer = ConsumptionApi[OrdersByCustomerQuery, OrderResponse](
    name="getShopifyOrdersByCustomer",
    query_function=get_orders_by_customer_query
)

get_shopify_orders_by_status = ConsumptionApi[OrdersByStatusQuery, OrderResponse](
    name="getShopifyOrdersByStatus",
    query_function=get_orders_by_status_query
)

get_shopify_order_analytics = ConsumptionApi[OrderAnalyticsQuery, OrderAnalyticsResponse](
    name="getShopifyOrderAnalytics",
    query_function=get_order_analytics_query
)
