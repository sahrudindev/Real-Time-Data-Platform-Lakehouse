{{
    config(
        materialized='view'
    )
}}

with source as (
    select * from {{ source('silver', 'customers') }}
),

staged as (
    select
        customer_sk,
        customer_id,
        email,
        first_name,
        last_name,
        concat(first_name, ' ', last_name) as full_name,
        phone,
        address,
        address.city as city,
        address.state as state,
        address.country as country,
        address.zip as zip_code,
        segment,
        lifetime_value,
        _valid_from,
        _valid_to,
        _is_current,
        _processed_at
    from source
)

select * from staged
