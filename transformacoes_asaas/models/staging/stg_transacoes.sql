WITH source AS (
    SELECT *
    FROM public.transacoes_raw
),

renomeado AS (
    SELECT
        transaction_id AS id,
        {{limpar_id('id_cliente')}} AS id_cliente, 
        {{limpar_data_criacao('data_criacao')}} AS data_transacao,
        {{limpar_valor_transacao('valor_transacao')}} AS valor_transacao,
        {{limpar_metodo_pagamento('metodo_pagamento')}} AS metodo_pagamento,
        status_transacao

    FROM source
)

SELECT * FROM renomeado