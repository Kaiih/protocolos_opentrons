import pandas as pd
import numpy as np

# Define o nome do arquivo de entrada e de saída
arquivo_entrada = 'scripts/tcc/sheet/QubitData_30-06-2025_17-29-34.csv'
arquivo_saida = 'scripts/tcc/sheet/saida.csv'

# Define as colunas que você quer manter
colunas_desejadas = ['Sample Name', 'Original Sample Conc.']

# Gera o mapeamento de wells e plates para 96 amostras conforme sua lógica
well_list = []
plate_list = []
for bloco in range(12):  # 12 blocos de 8 (4+4) = 96
    row = bloco % 6 + 1  # Vai de 1 a 6, depois repete
    # plate 5/6: A-D
    for i in range(4):
        well_list.append(f"{chr(65+i)}{row}")
        plate_list.append("5" if bloco < 6 else "6")
    # plate 2/3: A-D
    for i in range(4):
        well_list.append(f"{chr(65+i)}{row}")
        plate_list.append("2" if bloco < 6 else "3")

well_samples_map = {
    f"S{i+1}": well_list[i] for i in range(96)
}
well_plate_map = {
    f"S{i+1}": plate_list[i] for i in range(96)
}

# Mapeamento final para o destino (exemplo: placa final 96 poços)
well_final_map = {
    f"S{i+1}": well for i, well in enumerate([
        "A1","B1","C1","D1","E1","F1","G1","H1",
        "A2","B2","C2","D2","E2","F2","G2","H2",
        "A3","B3","C3","D3","E3","F3","G3","H3",
        "A4","B4","C4","D4","E4","F4","G4","H4",
        "A5","B5","C5","D5","E5","F5","G5","H5",
        "A6","B6","C6","D6","E6","F6","G6","H6",
        "A7","B7","C7","D7","E7","F7","G7","H7",
        "A8","B8","C8","D8","E8","F8","G8","H8",
        "A9","B9","C9","D9","E9","F9","G9","H9",
        "A10","B10","C10","D10","E10","F10","G10","H10",
        "A11","B11","C11","D11","E11","F11","G11","H11",
        "A12","B12","C12","D12","E12","F12","G12","H12"
    ])
}

target_volume = 20.0
target_concentration = 30.0

try:
    df = pd.read_csv(arquivo_entrada, usecols=colunas_desejadas)
    # Preencher as colunas de origem e destino
    df['Well'] = df['Sample Name'].map(well_final_map)
    df['Well_samples'] = df['Sample Name'].map(well_samples_map)
    df['Plate'] = df['Sample Name'].map(well_plate_map)

    # Calcula volumes linha a linha
    dna_vols = []
    dil_vols = []
    for conc in df['Original Sample Conc.']:
        if conc <= target_concentration:
            volume_dna_ul = target_volume
            volume_diluente_ul = 0.0
        else:
            volume_dna_ul = (target_concentration * target_volume) / conc
            volume_diluente_ul = target_volume - volume_dna_ul
            volume_dna_ul = float(f"{volume_dna_ul:.1f}")
            volume_diluente_ul = float(f"{volume_diluente_ul:.1f}")
        dna_vols.append(volume_dna_ul)
        dil_vols.append(volume_diluente_ul)
    df['DNA Volume (uL)'] = dna_vols
    df['Diluent Volume (uL)'] = dil_vols
    
    df.to_csv(arquivo_saida, index=False)

    print(f'As colunas foram importadas, a coluna "Well" foi preenchida e o resultado foi salvo em "{arquivo_saida}".')

except FileNotFoundError:
    print(f'Erro: O arquivo "{arquivo_entrada}" não foi encontrado. '
          f'Verifique se o nome e o caminho estão corretos.')
except ValueError:
    print('Erro: Uma ou mais das colunas especificadas não existem no arquivo CSV.')
except Exception as e:
    print(f'Ocorreu um erro inesperado: {e}')