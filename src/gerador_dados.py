#Este script vai simular 500.000 transações de Pix e Boleto, porém com alguns bugs para análise, como: valores negativos, IDs duplicados, erros de timezone, erro de integridade,datas estranhas... A ideia é simular uma realidade
import pandas as pd
import random
import os
import time
from datetime import datetime, timedelta

# Define onde esta no computador para não dar erro de "pasta não encontrada"
DIRETORIO_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAMINHO_DADOS_BRUTOS = os.path.join(DIRETORIO_BASE, "data", "01_raw")

QTD_REGISTROS = 500000 

def gerar_dados_simulados():

    # Marca o tempo inicial para saber quanto tempo demorou a criação dos dados fictícios
    inicio = time.time()
    
    print(f"🏦 [Simulador Asaas] Iniciando a geração de {QTD_REGISTROS} registros...")\
    # LUma lista para que seja escolhido aleatoriamente pelo código(o mock data)
    lista_metodos = ['PIX', 'BOLETO', 'CARTAO_CREDITO', 'CARTAO_DEBITO', 'TED']
    lista_status = ['CONFIRMADO', 'PENDENTE', 'FALHA', 'ESTORNADO', 'PROCESSANDO']
    
    # Lista vazia que vai guardar todas as transações antes de virar DataFrame
    dados_transacoes = []

    ############### LOOP PRINCIPAL ###############
    # Nesta etapa é gerado 99% do arquivo correto, sem os bugs
    for i in range(QTD_REGISTROS):
        
        # Cria aleatoriamente quantos dias atrás a venda aconteceu (entre hoje e 60 dias atrás)
        dias_atras = random.randint(0, 60)
        data_base = datetime.now() - timedelta(days=dias_atras)
        
        # Cria um dicionário representando uma linha da tabela
        transacao = {
            # ID único falso: "PAY-" + numero aleatorio de 7 digitos
            "transaction_id": f"PAY-{random.randint(1000000, 9999999)}",
            
            # Formata a data como texto (String)
            "data_criacao": data_base.strftime("%Y-%m-%d %H:%M:%S"),
            
            # Sorteia um ID de cliente entre 1 e 5000
            "id_cliente": random.randint(1, 5000),
            
            # Escolhe aleatoriamente um método e um status das listas lá de cima
            "metodo_pagamento": random.choice(lista_metodos),
            "status_transacao": random.choice(lista_status),
            
            # Gera um valor financeiro entre R$1.00 e R$15.000,00
            "valor_transacao": round(random.uniform(1.00, 15000.00), 2)
        }
        
        # Adiciona essa transação na lista principal
        dados_transacoes.append(transacao)

        # A cada 100.000 linhas, avisa no terminal para saber que não travou
        if (i + 1) % 100000 == 0:
            print(f"Gerado {i + 1} linhas.")

    ############### INJETANDO OS BUGS ###############
    print("\nInserindo erros propositais para testar o Analytics Engineer...")

    # -- Duplicidade
    # Pega a transação da posição 10 e duplica ela no final da lista
    # Porém, muda o status. Isso simula quando o sistema grava 2 logs para o mesmo ID.
    transacao_duplicada = dados_transacoes[10].copy()
    transacao_duplicada['status_transacao'] = 'PENDENTE' # O original pode ser outro
    transacao_duplicada['data_criacao'] = (datetime.now() - timedelta(minutes=5)).strftime("%Y-%m-%d %H:%M:%S")
    dados_transacoes.append(transacao_duplicada)
    print("Erro de Duplicidade inserido.")

    # -- Data no Futuro
    # Cria uma transação com data de amanhã(futura)
    dados_transacoes.append({
        "transaction_id": f"PAY-{random.randint(1000000, 9999999)}",
        "data_criacao": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S"), 
        "id_cliente": 1050,
        "metodo_pagamento": "PIX",
        "status_transacao": "CONFIRMADO",
        "valor_transacao": 500.00
    })
    print("Erro de Data Futura inserido.")

    # -- Valor Quebrado
    # Um valor com muitas casas decimais que pode quebrar arredondamentos
    dados_transacoes.append({
        "transaction_id": f"PAY-{random.randint(1000000, 9999999)}",
        "data_criacao": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "id_cliente": 2020,
        "metodo_pagamento": "CARTAO_CREDITO",
        "status_transacao": "CONFIRMADO",
        "valor_transacao": 150.3333333333 # O sistema esqueceu de arredondar!
    })
    print("Erro de Valor Decimal Infinito inserido.")

    # -- Valor Negativo 
    # Transação financeira não pode ser negativa
    dados_transacoes.append({
        "transaction_id": f"PAY-{random.randint(1000000, 9999999)}",
        "data_criacao": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "id_cliente": 3030,
        "metodo_pagamento": "PIX",
        "status_transacao": "FALHA",
        "valor_transacao": -150.00 # ERRO GRAVE
    })
    print("Erro de Valor Negativo inserido.")

    # -- Transação Órfã (Integridade)
    # Cliente nulo (None)
    dados_transacoes.append({
        "transaction_id": f"PAY-{random.randint(1000000, 9999999)}",
        "data_criacao": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "id_cliente": None, # Sem dono!
        "metodo_pagamento": "BOLETO",
        "status_transacao": "PENDENTE",
        "valor_transacao": 1200.00
    })
    print("Erro de Cliente Nulo inserido.")

    ############### SALVANDO O ARQUIVO ###############
    
    # Transforma a lista de dicionários em um df do Pandas
    df_final = pd.DataFrame(dados_transacoes)
    
    # Faz com que a pasta de destino existea e se não ele cria
    os.makedirs(CAMINHO_DADOS_BRUTOS, exist_ok=True)
    
    arquivo_saida = os.path.join(CAMINHO_DADOS_BRUTOS, "transacoes_bruto_bigdata.csv")
    
    df_final.to_csv(arquivo_saida, index=False) #sem o índice, o número da linha
    
    ############### FINALIZAÇÃO E MÉTRICAS ###############
    fim = time.time()
    tempo_total = round(fim - inicio, 2)
    tamanho_mb = os.path.getsize(arquivo_saida) / (1024 * 1024)
    
    print("\n" + "="*50)
    print(f"SUCESSO! Pipeline de Geração Finalizado.")
    print(f"Arquivo salvo em: {arquivo_saida}")
    print(f"Total de Linhas: {len(df_final)}")
    print(f"Tamanho do Arquivo: {tamanho_mb:.2f} MB")
    print(f"Tempo de Execução: {tempo_total} segundos")
    print("="*50)
    
if __name__ == "__main__":
    gerar_dados_simulados()