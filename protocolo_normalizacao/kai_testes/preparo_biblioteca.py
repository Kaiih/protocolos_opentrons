import pandas as pd

def diluir_bibliotecas(caminho_csv_qubit,
                              conc_desejada_ng_ul,
                              volume_final_ul,
                              coluna_sample_name='Sample Name',
                              coluna_concentracao='Original Sample Conc.'):
    """
    Calcula os volumes de DNA e diluente necessários para normalizar amostras.

    Args:
        caminho_csv_qubit (str): Caminho para o arquivo CSV gerado pelo Qubit.
        conc_desejada_ng_ul (float): Concentração final desejada em ng/µL (C2).
        volume_final_ul (float): Volume final desejado na placa em µL (V2).
        coluna_sample_name (str): Nome da coluna de identificação da amostra no CSV do Qubit.
        coluna_concentracao (str): Nome da coluna de concentração da amostra no CSV do Qubit.

    Returns:
        pandas.DataFrame: Um DataFrame com os volumes calculados para cada amostra.
    """
    try:
        # 1. Carregar o arquivo CSV do Qubit
        df_qubit = pd.read_csv(caminho_csv_qubit)
        print(f"CSV do Qubit carregado com sucesso de: {caminho_csv_qubit}")
        print(f"Colunas disponíveis: {df_qubit.columns.tolist()}")

    except FileNotFoundError:
        print(f"Erro: Arquivo CSV não encontrado em {caminho_csv_qubit}")
        return None
    except KeyError as e:
        print(f"Erro: Coluna {e} não encontrada no CSV. Verifique os nomes das colunas.")
        return None
    except Exception as e:
        print(f"Ocorreu um erro ao ler o CSV: {e}")
        return None

    # Criar um DataFrame para os resultados
    df_resultados = pd.DataFrame(columns=[
        coluna_sample_name,
        'Concentration (Qubit) ng/µL',
        'DNA Volume (µL)',
        'Diluent Volume (µL)',
        'Observação'
    ])

    for index, row in df_qubit.iterrows():
        sample_name = row[coluna_sample_name]
        conc_qubit = row[coluna_concentracao] # C1

        # Garantir que a concentração é um número
        try:
            conc_qubit = float(conc_qubit)
        except ValueError:
            print(f"Aviso: Concentração inválida para a amostra '{sample_name}': {conc_qubit}. Pulando esta amostra.")
            continue

        volume_dna_ul = 0.0
        volume_diluente_ul = 0.0
        observacao = ""

        # 4. Realizar o Cálculo de Diluição (C1V1 = C2V2)
        # 5. Tratar Amostras Abaixo da Concentração Desejada
        if conc_qubit > conc_desejada_ng_ul:
            # V1 = (C2 * V2) / C1
            volume_dna_ul = (conc_desejada_ng_ul * volume_final_ul) / conc_qubit
            volume_diluente_ul = volume_final_ul - volume_dna_ul
            observacao = "Amostra diluída para concentração desejada."
        else:
            # Se C1 <= C2, não é possível atingir a concentração desejada com diluição.
            # Usa-se o volume total da amostra original, e a concentração final será a C1.
            volume_dna_ul = 0.0
            volume_diluente_ul = 0.0
            observacao = f"Concentração original ({conc_qubit:.2f} ng/µL) já está abaixo da desejada ({conc_desejada_ng_ul:.2f} ng/µL)."

        # Arredondar os volumes para um número razoável de casas decimais (ex: 2 ou 3)
        volume_dna_ul = round(volume_dna_ul, 3)
        volume_diluente_ul = round(volume_diluente_ul, 3)

        # Adicionar os resultados ao DataFrame
        df_resultados.loc[len(df_resultados)] = [
            plate,
            Well,
            sample_name,
            conc_qubit,
            #volume_dna_ul,
            #volume_diluente_ul,
            #observacao
            concentracao_desejada,
            volume_total_placa
        ]

    return df_resultados

# --- Como usar o script ---
if __name__ == "__main__":
    # Defina o caminho para o seu arquivo CSV do Qubit
    caminho_csv_qubit = "/home/kai/Biotrop/opentrons/scripts/tcc/sheet/QubitData_30-06-2025_17-29-34.csv" # Substitua pelo nome do seu arquivo

    # Defina a concentração e o volume final desejados
    concentracao_desejada = 30.0 # ng/µL [User Query]
    volume_total_placa = 20.0    # µL [User Query]

    # Chama a função para calcular os volumes
    #sequenciamento = diluir_bibliotecas(
    #    caminho_csv_qubit,
    #    concentracao_desejada,
    #    volume_total_placa
    #)

    if sequenciamento is not None:
        # Exibe os resultados
        print("\n--- Resultados dos Cálculos de Normalização ---")
        print(sequenciamento)

        # 6. Gerar uma Nova Planilha de Saída
        nome_arquivo_saida = '/home/kai/Biotrop/opentrons/scripts/tcc/sheet/diluicoes_bibliotecas.csv'
        sequenciamento.to_csv(nome_arquivo_saida, index=False)
        print(f"\nResultados salvos em: {nome_arquivo_saida}")

        # Exemplo de como essa saída se relaciona com o input do Opentrons (Tabela 3 na fonte)
        # Se você precisar de um formato específico para o Opentrons,
        # pode reformatar df_volumes_calculados para se adequar.
        # Por exemplo, para a Tabela 3 da fonte, as colunas seriam:
        # Plate, Well, SampleID, Concentration, VolumeToDispense, TargetConcentration, TargetVolume, DiluentVolume
        # Você já tem Concentration, VolumeToDispense (DNA Volume), TargetConcentration, TargetVolume, DiluentVolume.
        # As colunas Plate, Well e SampleID precisariam ser extraídas do 'mapa da placa' JSON
        # ou do próprio CSV do Qubit (se 'Well' e 'Sample ID' estiverem presentes, como indicado [User Query]).
        # Isso permitiria gerar um CSV no formato da Tabela 3 [1] para os protocolos Opentrons [2].
