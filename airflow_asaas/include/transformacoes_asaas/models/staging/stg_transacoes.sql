WITH source AS (
    SELECT *
    FROM {{ source('asaas_fintech', 'transacoes_raw') }} 
),

deduplicado AS (
    SELECT 
        *,
        ROW_NUMBER() OVER(
            PARTITION BY transaction_id  
            ORDER BY data_criacao DESC   
        ) as duplicatas
    FROM source
),

renomeado AS (
    SELECT
        transaction_id AS id,
        {{limpar_id('id_cliente')}} AS id_cliente, 
        {{limpar_data_criacao('data_criacao')}} AS data_transacao,
        {{limpar_valor_transacao('valor_transacao')}} AS valor_transacao,
        {{limpar_metodo_pagamento('metodo_pagamento')}} AS metodo_pagamento,        
        UPPER(status_transacao) AS status_transacao 

    FROM deduplicado
    WHERE duplicatas = 1 --  Mantém apenas o primeiro registro de cada cliente
        AND id_cliente IS NOT NULL
)

SELECT * FROM renomeado