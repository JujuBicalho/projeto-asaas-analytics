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
    count(*) as qtd_total_transacoes

FROM {{ ref('stg_transacoes') }}
GROUP BY 1