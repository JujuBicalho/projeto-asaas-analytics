#Enviar a camada silver para o postgres
#Criar o banco no postgres e depois rodar o script
import pandas as pd
import os
from sqlalchemy import create_engine

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(BASE_DIR, "data", "02_staging", "transacoes_limpas.csv")

# Conexão com o Postgres
DB_CONNECTION_URI = 'postgresql://postgres:admin@localhost:5432/asaas_fintech'

def carregar_para_postgres():
    # Vai verificar se o csv existe, caso contrário dará erro
    if not os.path.exists(CSV_PATH):
        print(f"Erro: Arquivo {CSV_PATH} não encontrado.")
        return
    
    df = pd.read_csv(CSV_PATH)
    
    try:
        engine = create_engine(DB_CONNECTION_URI)
        
        df.to_sql('transacoes_raw', con=engine, if_exists='replace', index=False) # if_exists se já existir, apaga e cria uma nova 
        
        print(f"SUCESSO! Linhas carregadas na tabela 'transacoes_raw'.")
        
    except Exception as e:
        print(f"Erro de Conexão: {e}")

if __name__ == "__main__":
    carregar_para_postgres()
    