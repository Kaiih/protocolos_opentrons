import pandas as pd

colunas= ["Sample Name","Original Sample Conc."]
# Ler o arquivo CSV
df = pd.read_csv("/home/kai/Biotrop/opentrons/scripts/tcc/QubitData_30-06-2025_17-29-34.csv", usecols=colunas)

#desejada=Sample Name,Original Sample Conc.
# Remover colunas indesejadas (exemplo: 'coluna1', 'coluna2')


print(df)