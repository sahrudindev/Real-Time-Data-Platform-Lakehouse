{{
    config(
        materialized='view'
    )
}}

with source as (
    select * from {{ source('silver', 'orders') }}
),

staged as (
    select
        order_sk,
        order_id,
        customer_id,
        items,
        item_count,
        total_amount,
        currency,
        status,
        shipping_address,
        payment_method,
        order_date,
        order_year,
        order_month,
        order_day,
        event_ts as event_timestamp,
        created_at,
        updated_at,
        _processed_at
    from source
)

select * from staged
