{% set metodos_pagamento = ['PIX', 'BOLETO', 'Cartão de Débito', 'Cartão de Crédito'] %}

WITH transacoes AS (
    SELECT * FROM {{ ref('stg_transacoes') }}
),

pivot_pagamentos AS (
    SELECT
        data_transacao::date as data, -- aqui vai agrupar por dia
        {% for metodo in metodos_pagamento %} -- LOOP // Para cada item da lista de cima, ele gera uma linha de SUM
        SUM(CASE WHEN metodo_pagamento = '{{ metodo }}' THEN valor_transacao ELSE 0 END) 
        AS total_{{ metodo | replace(' ', '_') | replace('á', 'a') | replace('é', 'e') | lower }},
        {% endfor %}-- fim do loop
        
        COUNT(*) as qtd_transacoes_total

    FROM transacoes
    GROUP BY 1
)

SELECT * FROM pivot_pagamentos
ORDER BY data DESC