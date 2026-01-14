WITH source AS (
    SELECT *
    FROM public.clientes_raw
),

limpeza_basica AS (
    SELECT
        {{limpar_id('id_cliente')}} AS id_cliente,
        {{limpar_nome('nome')}} AS nome_cliente,
        {{limpar_email('email')}} AS email_cliente,
        CAST(data_nascimento AS DATE) AS data_nascimento_original,
        {{limpar_texto('estado')}} AS estado_cliente,
        {{limpar_texto('genero')}} AS genero,
        {{limpar_texto('profissao')}} AS profissao,
        {{limpar_texto('cidade')}} AS cidade_cliente

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