{{
    config(
        materialized='table'
    )
}}

with orders as (
    select * from {{ ref('stg_orders') }}
),

order_items as (
    select * from {{ ref('stg_order_items') }}
),

order_metrics as (
    select
        order_id,
        sum(quantity) as total_units,
        count(distinct product_id) as unique_products,
        avg(unit_price) as avg_unit_price,
        max(unit_price) as max_unit_price,
        min(unit_price) as min_unit_price
    from order_items
    group by order_id
)

select
    o.order_sk,
    o.order_id,
    o.customer_id,
    o.item_count,
    o.total_amount,
    o.currency,
    o.status,
    o.payment_method,
    o.order_date,
    o.order_year,
    o.order_month,
    o.order_day,
    o.event_timestamp,
    m.total_units,
    m.unique_products,
    m.avg_unit_price,
    m.max_unit_price,
    m.min_unit_price,
    case
        when o.total_amount >= 1000 then 'high_value'
        when o.total_amount >= 100 then 'medium_value'
        else 'low_value'
    end as order_value_tier,
    current_timestamp() as _dbt_updated_at
from orders o
left join order_metrics m on o.order_id = m.order_id
