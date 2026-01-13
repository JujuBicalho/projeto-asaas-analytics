WITH source AS (
    SELECT *
    FROM public.clientes_raw
),

limpeza_basica AS (
    SELECT
        CAST(id_cliente AS INTEGER) AS id_cliente,
        TRIM(
            REGEXP_REPLACE(nome, '^(Dr\.|Dra\.|Sr\.|Sra\.|Srta\.)\s*', '', 'i')
        ) AS nome_cliente,
        LOWER(
            TRANSLATE(
                REPLACE(email, '..', '.'),
                'áàãâäéèêëíìîïóòõôöúùûüçñÁÀÃÂÄÉÈÊËÍÌÎÏÓÒÕÔÖÚÙÛÜÇÑ',
                'aaaaaeeeeiiiiooooouuuucnAAAAAEEEEIIIIOOOOOUUUUCN'
            )
        ) AS email_cliente,
        
        CAST(data_nascimento AS DATE) AS data_nascimento_original,
        INITCAP(genero) AS genero,
        UPPER(estado) AS estado_cliente,
        profissao,
        cidade AS cidade_cliente

    FROM source
),

renomeado AS (
    SELECT
        id_cliente,
        nome_cliente,
        email_cliente,
        TO_CHAR(data_nascimento_original, 'DD/MM/YYYY') AS data_nascimento,
        DATE_PART('year', AGE(CURRENT_DATE, data_nascimento_original)) AS idade_atual,
        genero,
        profissao,
        estado_cliente,
        cidade_cliente

    FROM limpeza_basica
)

SELECT * FROM renomeado