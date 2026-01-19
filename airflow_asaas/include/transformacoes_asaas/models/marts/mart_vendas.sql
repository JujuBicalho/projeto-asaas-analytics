WITH transacoes AS (
    SELECT *
    FROM {{ ref('stg_transacoes') }}
),

clientes AS (
    SELECT *
    FROM {{ ref('stg_clientes') }}
),

deduplicacao AS ( -- (MDM)Se o id repetir ele vai pegar o mais recente
    SELECT 
        *,
        ROW_NUMBER() OVER(
            PARTITION BY id 
            ORDER BY data_transacao DESC
        ) as linha_unica
    FROM transacoes
),

final AS (
    SELECT
        t.id,
        t.id_cliente,
        t.data_transacao,
        t.valor_transacao,
        t.metodo_pagamento,
        t.status_transacao,
        c.nome_cliente,
        c.email_cliente,
        c.cidade_cliente,
        c.estado_cliente,
        c.profissao,      
        c.genero,
        c.data_nascimento, 
        c.idade_atual,
        CASE 
            WHEN c.idade_atual < 18 THEN 'Menor de Idade'
            WHEN c.idade_atual BETWEEN 18 AND 59 THEN 'Adulto'
            WHEN c.idade_atual >= 60 THEN 'Idoso'
            ELSE 'Não Identificado'
        END AS faixa_etaria,

        CASE 
            WHEN t.valor_transacao < 1000 THEN 'Baixo Valor'
            WHEN t.valor_transacao BETWEEN 1000 AND 5000 THEN 'Médio Valor'
            WHEN t.valor_transacao > 5000 THEN 'Alto Valor'
        END AS categoria_ticket

    FROM deduplicacao t
        LEFT JOIN clientes c ON t.id_cliente = c.id_cliente
    WHERE t.linha_unica = 1 -- aqui remove a duplicata
      AND t.id_cliente IS NOT NULL -- faz com que nõa tenha cliente nulo
)

SELECT * FROM final