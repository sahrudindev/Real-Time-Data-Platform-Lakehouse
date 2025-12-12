{{
    config(
        materialized='view'
    )
}}

with source as (
    select * from {{ source('silver', 'order_items') }}
),

staged as (
    select
        order_item_sk,
        order_id,
        customer_id,
        line_number,
        product_id,
        product_name,
        quantity,
        unit_price,
        line_total,
        currency,
        event_ts as event_timestamp,
        _processed_at
    from source
)

select * from staged
