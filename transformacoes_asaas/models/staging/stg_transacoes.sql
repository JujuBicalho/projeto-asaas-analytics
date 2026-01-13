WITH source AS (
    SELECT *
    FROM public.transacoes_raw
),

renomeado AS (
    SELECT
        transaction_id AS id,
        CAST(NULLIF(REGEXP_REPLACE(CAST(id_cliente AS TEXT), '\.0$', ''), '') AS INTEGER) AS id_cliente,
        CAST(data_criacao AS TIMESTAMP) AS data_transacao,
        CAST(valor_transacao AS NUMERIC) AS valor_transacao,
        CASE 
            WHEN metodo_pagamento = 'CARTAO_DEBITO' THEN 'Cartão de Débito'
            WHEN metodo_pagamento = 'CARTAO_CREDITO' THEN 'Cartão de Crédito'
            ELSE metodo_pagamento 
        END AS metodo_pagamento,

        status_transacao

    FROM source
)

SELECT * FROM renomeado