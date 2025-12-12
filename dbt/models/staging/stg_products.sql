{{
    config(
        materialized='view'
    )
}}

with source as (
    select * from {{ source('silver', 'products') }}
),

staged as (
    select
        product_sk,
        product_id,
        name as product_name,
        description,
        category,
        subcategory,
        price,
        currency,
        sku,
        brand,
        attributes,
        is_active,
        event_ts as event_timestamp,
        created_at,
        updated_at,
        _processed_at
    from source
)

select * from staged
