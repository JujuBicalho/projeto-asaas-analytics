# PROCESSO DE ETL (raw para staging- de bronze para silver)
#Aqui vai se atentar para:
#- Se o id aparecer mais de uma vez ele pega o mais recente(a transação mais atual)
#- Remove os valores negativos(transação não tem como ser negativa)
#- Remore transações futuras(correção temporal - não pode haver transação de amanhã no hoje)
#- Manter integridade dos dados(não tem como ter transação se não há cliente)
import pandas as pd
import os
import time
from datetime import datetime

########## CONFIGURAR OS CAMINHOS - para rodar em qq máquina ##########
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_PATH = os.path.join(BASE_DIR, "data", "01_raw", "transacoes_bruto_bigdata.csv")
STAGING_PATH = os.path.join(BASE_DIR, "data", "02_staging", "transacoes_limpas.csv")

def run_pipeline():
    inicio = time.time()
    print("Iniciando o processamento de dados!!!")

    ######### INÍCIO ETL : ler os arquivos #########
    if not os.path.exists(RAW_PATH):
        print(f"Erro: Arquivo não encontrado em {RAW_PATH}")
        return

    print(f"Lendo arquivo bruto: {RAW_PATH}...")
    df = pd.read_csv(RAW_PATH)
    qtd_inicial = len(df)
    print(f"Total de linhas: {qtd_inicial}")

    ######### LIMPEZA DOS DADOS #########
    # --- RETIRANDO VALORES NEGATIVOS ---
    df_limpeza = df[df['valor_transacao'] > 0].copy()
    removidos_valor = qtd_inicial - len(df_limpeza)
    print(f"Valores negativos removidos: {removidos_valor}")

    # --- CONVERTER DATA PARA DATETIME ---
    df_limpeza['data_criacao'] = pd.to_datetime(df_limpeza['data_criacao'])
    
    # Aqui vai filtrar as datas que são menos ou iguais ao dia de hoje
    agora = datetime.now()
    df_limpeza = df_limpeza[df_limpeza['data_criacao'] <= agora]
    
    removidos_data = (qtd_inicial - removidos_valor) - len(df_limpeza)
    print(f"Datas futuras removidas: {removidos_data}")

    # --- INTEGRIDADE DOS DADOS/DO CLIENTE (não pode ter transação sem cliente) ---
    qtd_antes_null = len(df_limpeza) #Aqui ele vai "contar" quantas linhas tem antes da remoção
    df_limpeza = df_limpeza.dropna(subset=['id_cliente']) #Aqui só apaga a linha se o campo id estiver vazio(por isso o subset)
    print(f"Clientes nulos removidos: {qtd_antes_null - len(df_limpeza)}")

    # --- REMOVER DUPLICATAS (se tiver id duplicado fica com a mais recente) ---
    df_limpeza = df_limpeza.sort_values(by=['transaction_id', 'data_criacao'], ascending=[True, False]) #O sort vai ordenar por id e logo depois por data
    qtd_antes_remover_duplicatas = len(df_limpeza) #Aqui vai contar as linhas antes da remoção
    df_limpeza = df_limpeza.drop_duplicates(subset=['transaction_id'], keep='first') #Mantém a mais recente transação aqui
    
    print(f"Duplicatas removidas (mantendo a mais recente): {qtd_antes_remover_duplicatas - len(df_limpeza)}")

    ########## FIM ETL: salvar no staging
    print("\nSalvando dados tratados na camada Silver!")
    
    # Garante que a pasta staging exista para salvamento correto, se existe ele roda, caso contrário dá erro
    os.makedirs(os.path.dirname(STAGING_PATH), exist_ok=True)
    
    df_limpeza.to_csv(STAGING_PATH, index=False)

    # --- RELATÓRIO FINAL ---
    fim = time.time()
    qtd_final = len(df_limpeza)
    perda_total = qtd_inicial - qtd_final
    
    if qtd_inicial > 0:
        pct_perda_total = (perda_total / qtd_inicial) * 100
    else:
        pct_perda_total = 0
    
    print("="*50)
    print("PIPELINE FINALIZADO COM SUCESSO!")
    print(f"Linhas Iniciais: {qtd_inicial}")
    print(f"Linhas Finais:   {qtd_final}")
    print(f"Linhas removidas:  {perda_total} ({pct_perda_total:.2f}%) registros inválidos")
    print(f"Tempo Total Gasto:    {round(fim - inicio, 2)} segundos")
    print("="*50)

if __name__ == "__main__":
    run_pipeline()