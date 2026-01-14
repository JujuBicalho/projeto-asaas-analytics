# 🏦 Projeto de Analytics Engineering - ASAAS Fintech
**Desenvolvido por Juliana Bicalho** 
**Linkedin: https://www.linkedin.com/in/jujubicalho**

Este projeto simula um ambiente real de Analytics Engineering de uma Fintech escolhida aleatoriamente, a Asaas, focando na construção de um **Data Warehouse** moderno, escalável e confiável.

O objetivo principal foi ingerir dados brutos (Raw), tratá-los e limpá-los (Staging) e criar tabelas analíticas de negócio (Marts) prontas para consumo no Power BI.

## Arquitetura do Projeto (ELT)

O projeto segue a arquitetura de **ELT**:

1.  **Extract & Load (Python):** Scripts em Python (`Faker`) geram dados sintéticos de Clientes e Transações (com ruídos propositais para simular o mundo real) e carregam na camada `Raw` do Postgres.
2.  **Transform (dbt Core):** O dbt é responsável por toda a limpeza, testagem e modelagem dos dados dentro do Data Warehouse.

### Stacks
* **Linguagem:** Python 3.12 (Geração de Dados) & SQL (Transformação)
* **Orquestração e Modelagem:** dbt Core 
* **Data Warehouse:** PostgreSQL
* **Controle de Versão:** Git & GitHub

---

## 🔄 Pipeline de Dados (Linhagem)

### 1. Camada Raw (Bronze)
Dados brutos carregados via Python, contendo erros de tipagem, duplicatas e sujeira de texto.
* `public.clientes_raw`
* `public.transacoes_raw`

### 2. Camada Staging (Silver)
* **Limpeza de Texto:** Padronização de nomes (Title Case), emails (minúsculo/sem acento) e correção de erros de digitação (ex: "GastrôNomo" -> "Gastrônomo").
* **Tipagem:** Conversão de strings para `INTEGER`, `DATE` e `NUMERIC`.
* **Feature Engineering:** Cálculo de idade atual e formatação de datas (padrão BR).
* **Testes:** `Unique`, `Not Null`, `Accepted Values`.

### 3. Camada Marts (Gold)
* **`mart_vendas`**: Tabela fato que une Vendas e Clientes.
    * **Deduplicação Inteligente:** Uso de `ROW_NUMBER()` para remover transações duplicadas, priorizando a mais recente.
    * **Regras de Negócio:** Categorização de clientes por **Faixa Etária** (Menor de Idade, Adulto, Idoso) e Vendas por **Categoria de Ticket** (Alto/Médio/Baixo Valor).

---

## 🚀 Como Rodar o Projeto

### Pré-requisitos
* Python 3.10+
* dbt Core instalado
* Acesso a um banco Postgres

### Passo a Passo

1.  **Geração e Carga de Dados:**
    ```bash
    python src/gerador_dados_clientes.py
    python src/gerador_dados_transacoes.py
    # Importar CSVs gerados para o Postgres (Schema public)
    ```

2.  **Rodar as Transformações (dbt):**
    Entre na pasta do projeto dbt:
    ```bash
    cd transformacoes_asaas
    ```

    Execute e teste os modelos:
    ```bash
    dbt run       # Cria as tabelas/views
    dbt test      # Executa testes de qualidade 
    ```

3.  **Gerar Documentação:**
    ```bash
    dbt docs generate
    dbt docs serve
    ```

---

## 🧪 Qualidade de Dados (Data Quality)

O projeto implementa testes automatizados para garantir a confiança nos dados:
* **Integridade Referencial:** Garante que toda venda tenha um cliente válido.
* **Unicidade:** Garante que não existam IDs duplicados na camada final.
* **Consistência:** Valida se campos de categoria (Status, Pagamento) contêm apenas valores esperados.

