{{
    config(
        materialized='table'
    )
}}

with customers as (
    select * from {{ ref('stg_customers') }}
    where _is_current = true
),

orders as (
    select * from {{ ref('stg_orders') }}
),

customer_orders as (
    select
        customer_id,
        count(order_id) as total_orders,
        sum(total_amount) as total_revenue,
        avg(total_amount) as avg_order_value,
        min(order_date) as first_order_date,
        max(order_date) as last_order_date,
        sum(item_count) as total_items_purchased,
        datediff(current_date(), min(order_date)) as days_since_first_order,
        datediff(current_date(), max(order_date)) as days_since_last_order
    from orders
    group by customer_id
)

select
    c.customer_sk,
    c.customer_id,
    c.email,
    c.full_name,
    c.first_name,
    c.last_name,
    c.phone,
    c.city,
    c.state,
    c.country,
    c.segment,
    c.lifetime_value,
    coalesce(co.total_orders, 0) as total_orders,
    coalesce(co.total_revenue, 0) as total_revenue,
    coalesce(co.avg_order_value, 0) as avg_order_value,
    co.first_order_date,
    co.last_order_date,
    coalesce(co.total_items_purchased, 0) as total_items_purchased,
    coalesce(co.days_since_first_order, 0) as days_since_first_order,
    coalesce(co.days_since_last_order, 0) as days_since_last_order,
    case
        when co.total_revenue >= 10000 then 'platinum'
        when co.total_revenue >= 5000 then 'gold'
        when co.total_revenue >= 1000 then 'silver'
        else 'bronze'
    end as customer_tier,
    case
        when co.days_since_last_order <= 30 then 'active'
        when co.days_since_last_order <= 90 then 'at_risk'
        when co.days_since_last_order <= 180 then 'dormant'
        when co.days_since_last_order > 180 then 'churned'
        else 'new'
    end as customer_status,
    current_timestamp() as _dbt_updated_at
from customers c
left join customer_orders co on c.customer_id = co.customer_id
