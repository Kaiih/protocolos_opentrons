import pandas as pd
from pandas import read_excel
import os

# Corrigido o nome da variável para 'directory'
sample = 'shample_sheet'
map = 'mapa_placa'
dados = []

# Verifica se o diretório existe
if not os.path.exists(directory):
    print(f"Erro: O diretório '{directory}' não existe.")
    exit()

for arquivo in os.listdir(directory):
    if arquivo.endswith(".csv"):
        caminho_arquivo = os.path.join(directory, arquivo)
        try:
            df = pd.read_csv(caminho_arquivo)
            dados.append(df)
        except Exception as e:
            print(f"Erro ao ler o arquivo '{arquivo}': {e}")

# Verifica se há dados antes de concatenar
if dados:
    try:
        consolidado = pd.concat(dados)
        nome_arquivo = 'base_consolidado.csv'
        caminho_completo = os.path.join(directory, nome_arquivo)
        consolidado.to_csv(caminho_completo, index=False)
        print(f"Arquivo consolidado salvo em: {caminho_completo}")
    except Exception as e:
        print(f"Erro ao salvar o arquivo consolidado: {e}")
else:
    print("Nenhum arquivo CSV encontrado no diretório.")