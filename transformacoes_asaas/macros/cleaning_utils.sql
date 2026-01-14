-- Macro 1: **Padronização de texto** Maiúscula e sem espaços extras
{% macro limpar_texto(coluna) %}
    TRIM(
        TRANSLATE(
            UPPER({{ coluna }}), 
            'áàãâäéèêëíìîïóòõôöúùûüçñ', 
            'ÁÀÃÂÄÉÈÊËÍÌÎÏÓÒÕÔÖÚÙÛÜÇÑ'
        )
    )
{% endmacro %}

-- Macro 2: **Limpeza de ID's** Transforma texto 12.0 em 12
{% macro limpar_id(coluna) %}
    CAST(NULLIF(REGEXP_REPLACE(CAST({{ coluna }} AS TEXT), '\.0$', ''), '') AS INTEGER)
{% endmacro %}

-- Macro 3: **Limpeza de Email** Minúsculo e sem acento 
{% macro limpar_email(coluna) %}
    LOWER(
        TRANSLATE(
            REPLACE({{ coluna }}, '..', '.'), 
            'áàãâäéèêëíìîïóòõôöúùûüçñÁÀÃÂÄÉÈÊËÍÌÎÏÓÒÕÔÖÚÙÛÜÇÑ',
            'aaaaaeeeeiiiiooooouuuucnAAAAAEEEEIIIIOOOOOUUUUCN'
        )
    )
{% endmacro %}

-- Macro 4: **Limpeza de Nome** Tirar abreviações
{% macro limpar_nome(coluna) %}
    TRIM(
        TRANSLATE(
            REGEXP_REPLACE(
                UPPER({{ coluna }}), 
                '^(DR\.|DRA\.|SR\.|SRA\.|SRTA\.|PROF\.|PROFA\.)\s*', 
                ''
            ),
            'áàãâäéèêëíìîïóòõôöúùûüçñ', 
            'ÁÀÃÂÄÉÈÊËÍÌÎÏÓÒÕÔÖÚÙÛÜÇÑ'
        )
    )
{%endmacro%}

-- Macro 4: *Limpeza de Data Criação*
{% macro limpar_data_criacao(coluna) %}
    CAST({{ coluna }} AS TIMESTAMP)
{% endmacro %}

-- Macro 5: *Limpeza de Valor Transação* Colocar com os pontos corretos
{% macro limpar_valor_transacao(coluna) %}
    CAST({{ coluna }} AS NUMERIC)
{%endmacro%}

-- Macro 6: *Limpeza de Método de Pagamento* Mudar os nomes 
{% macro limpar_metodo_pagamento(coluna) %}
    CASE 
        WHEN {{ coluna }} = 'CARTAO_DEBITO' THEN TRANSLATE(UPPER('Cartão de Débito'),'áàãâäéèêëíìîïóòõôöúùûüçñ', 
            'ÁÀÃÂÄÉÈÊËÍÌÎÏÓÒÕÔÖÚÙÛÜÇÑ')
        WHEN {{ coluna }} = 'CARTAO_CREDITO' THEN TRANSLATE(UPPER('Cartão de Crédito'), 'áàãâäéèêëíìîïóòõôöúùûüçñ', 
            'ÁÀÃÂÄÉÈÊËÍÌÎÏÓÒÕÔÖÚÙÛÜÇÑ')
        ELSE {{ coluna }} 
    END
{% endmacro %}