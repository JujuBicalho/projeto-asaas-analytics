-- faz atualizção incremental
{{
    config(
        materialized = 'incremental',
        unique_key = 'id_cliente'
    )
}}

-- cria uma variável para guardar a lista de métodos (Pix, Boleto, etc)
{% set lista_metodos = dbt_utils.get_column_values(table=ref('stg_transacoes'), column='metodo_pagamento') %}

SELECT
    id_cliente,
    {{ dbt_utils.pivot(
        'metodo_pagamento',
        lista_metodos,
        agg='sum',
        then_value='valor_transacao',
        else_value=0
    ) }},

    sum(valor_transacao) as valor_total_gasto,
    count(*) as qtd_total_transacoes,
    max(data_transacao) as ultima_transacao -- Pega a data mais recente de transação do cliente para o incremental


FROM {{ ref('stg_transacoes') }}

WHERE 1=1 -- se a tabela existir no branco o dbt roda as linhas e traz os dados após a data rodada do último dia
{% if is_incremental() %}
  AND data_transacao > (SELECT max(ultima_transacao) FROM {{ this }})
{% endif %}

GROUP BY 1