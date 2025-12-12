{{
    config(
        materialized='table'
    )
}}

with order_items as (
    select * from {{ ref('stg_order_items') }}
),

products as (
    select * from {{ ref('stg_products') }}
)

select
    p.product_sk,
    p.product_id,
    p.product_name,
    p.description,
    p.category,
    p.subcategory,
    p.brand,
    p.price as list_price,
    p.currency,
    p.sku,
    p.is_active,
    coalesce(count(oi.order_item_sk), 0) as times_ordered,
    coalesce(sum(oi.quantity), 0) as total_quantity_sold,
    coalesce(sum(oi.line_total), 0) as total_revenue,
    coalesce(avg(oi.unit_price), p.price) as avg_selling_price,
    coalesce(count(distinct oi.customer_id), 0) as unique_buyers,
    case
        when sum(oi.line_total) >= 50000 then 'star'
        when sum(oi.line_total) >= 10000 then 'performer'
        when sum(oi.line_total) >= 1000 then 'average'
        else 'underperformer'
    end as product_tier,
    current_timestamp() as _dbt_updated_at
from products p
left join order_items oi on p.product_id = oi.product_id
group by
    p.product_sk, p.product_id, p.product_name, p.description,
    p.category, p.subcategory, p.brand, p.price, p.currency, p.sku, p.is_active
