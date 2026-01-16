{% snapshot snapshot_clientes %}
{{
    config(
        target_schema = 'snapshots',
        unique_key = 'id_cliente',
        strategy='check',
        check_cols=['nome_cliente', 'email_cliente']
    )
}}
    
SELECT * FROM {{ ref('stg_clientes') }}

{% endsnapshot %}