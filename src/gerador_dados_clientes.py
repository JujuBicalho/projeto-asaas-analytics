import pandas as pd
import random
import os
import time
from datetime import datetime, timedelta
from faker import Faker  

DIRETORIO_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAMINHO_DADOS_BRUTOS = os.path.join(DIRETORIO_BASE, "data", "01_raw")

QTD_CLIENTES = 50000 

fake = Faker('pt_BR') 

def gerar_clientes():
    inicio = time.time()
    print(f"Gerando {QTD_CLIENTES} clientes!")

    dados_clientes = []

    # Lista auxiliar para garantir consistência do Estado e Cidade porque as vezes o faker mistura as coisas
    locais_br = {
        'SP': ['São Paulo', 'Campinas', 'Santos', 'Ribeirão Preto'],
        'RJ': ['Rio de Janeiro', 'Niterói', 'Duque de Caxias'],
        'MG': ['Belo Horizonte', 'Uberlândia', 'Contagem'],
        'RS': ['Porto Alegre', 'Caxias do Sul'],
        'PR': ['Curitiba', 'Londrina'],
        'BA': ['Salvador', 'Feira de Santana'],
        'PE': ['Recife', 'Jaboatão dos Guararapes']
    }
    siglas_estados = list(locais_br.keys())

    # --- LOOP PRINCIPAL para gerar os dados fakes ---
    for i in range(1, QTD_CLIENTES + 1):
        
        sexo = random.choice(['M', 'F'])
        
        if sexo == 'M':
            nome_completo = fake.name_male()
        else:
            nome_completo = fake.name_female()

        # Cria um email baseado no nome para parecer real
        primeiro_nome = nome_completo.split()[0].lower()
        ultimo_nome = nome_completo.split()[-1].lower()
        provedor = fake.free_email_domain() 
        email = f"{primeiro_nome}.{ultimo_nome}{random.randint(10,99)}@{provedor}"

        estado = random.choice(siglas_estados)
        cidade = random.choice(locais_br[estado])

        cliente = {
            "id_cliente": i,
            "nome": nome_completo,
            "email": email,
            "data_nascimento": fake.date_of_birth(minimum_age=18, maximum_age=90).strftime("%Y-%m-%d"),
            "estado": estado,
            "cidade": cidade.title(),
            "genero": "Masculino" if sexo == 'M' else "Feminino",
            "profissao": fake.job().title() 
        }
        
        dados_clientes.append(cliente)

        if i % 5000 == 0:
            print(f"Gerado {i} clientes...")

    # --- IInserir erros(bugs) ---
    print("\Inserindo sujeira nos dados...")

    #Email nulo
    dados_clientes.append({
        "id_cliente": 50001,
        "nome": fake.name(),
        "email": None, # ERRO
        "data_nascimento": "1995-05-20",
        "estado": "SP", "cidade": "São Paulo", "genero": "Feminino", "profissao": "Analista"
    })

    # Cliente do futuro(nascerá ainda)
    dados_clientes.append({
        "id_cliente": 50002,
        "nome": "Marty McFly",
        "email": "marty@futuro.com",
        "data_nascimento": "2085-10-21", 
        "estado": "RJ", "cidade": "Rio de Janeiro", "genero": "Masculino", "profissao": "Viajante"
    })
    
    #Estado inexistente
    dados_clientes.append({
        "id_cliente": 50003,
        "nome": "Alien",
        "email": "alien@space.com",
        "data_nascimento": "2000-01-01",
        "estado": "XX", 
        "cidade": "Marte", "genero": "Outro", "profissao": "Invasor"
    })

    df = pd.DataFrame(dados_clientes)
    
    os.makedirs(CAMINHO_DADOS_BRUTOS, exist_ok=True)
    arquivo = os.path.join(CAMINHO_DADOS_BRUTOS, "clientes_bruto.csv")
    df.to_csv(arquivo, index=False)
    
    print(f"SUCESSO! Arquivo gerado em: {arquivo}")

if __name__ == "__main__":
    gerar_clientes()