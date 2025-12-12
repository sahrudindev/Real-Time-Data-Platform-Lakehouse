{{
    config(
        materialized='table'
    )
}}

with orders as (
    select * from {{ ref('int_orders_enriched') }}
)

select
    order_date,
    order_year,
    order_month,
    count(order_id) as total_orders,
    count(distinct customer_id) as unique_customers,
    sum(total_amount) as total_revenue,
    avg(total_amount) as avg_order_value,
    max(total_amount) as max_order_value,
    min(total_amount) as min_order_value,
    sum(total_units) as total_units_sold,
    sum(unique_products) as total_product_varieties,
    sum(total_revenue) / nullif(count(distinct customer_id), 0) as revenue_per_customer,
    count(case when order_value_tier = 'high_value' then 1 end) as high_value_orders,
    count(case when order_value_tier = 'medium_value' then 1 end) as medium_value_orders,
    count(case when order_value_tier = 'low_value' then 1 end) as low_value_orders,
    current_timestamp() as _dbt_updated_at
from orders
group by order_date, order_year, order_month
order by order_date
