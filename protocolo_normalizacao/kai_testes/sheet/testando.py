from opentrons import protocol_api
import csv
import os

metadata = {
    'protocolName': 'Teste',
    'author': 'Kai',
    'apiLevel': '2.15'
}

def identificar_plate(well):
    # Plate 2: E1-E6, F1-F6, G1-G6, H1-H6
    if well[0] in 'EFGH' and int(well[1:]) in range(1, 7):
        return '2'
    # Plate 3: E7-E12, F7-F12, G7-G12, H7-H12
    if well[0] in 'EFGH' and int(well[1:]) in range(7, 13):
        return '3'
    # Plate 5: A1-A6, B1-B6, C1-C6, D1-D6
    if well[0] in 'ABCD' and int(well[1:]) in range(1, 7):
        return '5'
    # Plate 6: A7-A12, B7-B12, C7-C12, D7-D12
    if well[0] in 'ABCD' and int(well[1:]) in range(7, 13):
        return '6'
    # Default (caso não encontre)
    return '2'

def run(protocolo):
    # Definindo os labwares
    final_plate = protocolo.load_labware('opentrons_96_wellplate_200ul_pcr_full_skirt', '1')
    dna_plate_2 = protocolo.load_labware('corning_24_wellplate_3.4ml_flat', '2')
    dna_plate_3 = protocolo.load_labware('corning_24_wellplate_3.4ml_flat', '3')
    water_reservoir = protocolo.load_labware('usascientific_12_reservoir_22ml', '4')
    dna_plate_5 = protocolo.load_labware('corning_24_wellplate_3.4ml_flat', '5')
    dna_plate_6 = protocolo.load_labware('corning_24_wellplate_3.4ml_flat', '6')
    tiprack_20ul_1 = protocolo.load_labware('opentrons_96_filtertiprack_20ul', '8')
    tiprack_20ul_2 = protocolo.load_labware('opentrons_96_filtertiprack_20ul', '9')

    p20 = protocolo.load_instrument('p20_single_gen2', 'left', tip_racks=[tiprack_20ul_1, tiprack_20ul_2])

    path_csv = 'scripts/tcc/sheet/saida.csv'

    if not os.path.exists(path_csv):
        protocolo.comment(f"ERRO: Arquivo CSV não encontrado no caminho: {path_csv}")
        return  

    protocolo.comment(f"Arquivo CSV encontrado!")
    
    volumes = []
    try:
        with open(path_csv, mode='r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                # Converte os campos de volume para float
                Well = row['Well']
                volumes.append({
                    'sample_id': row['Sample Name'],
                    'well': Well,
                    'volume_diluente_ul': float(row['volume_diluente_ul']),
                    'volume_dna_ul': float(row['volume_dna_ul']),
                    'plate': identificar_plate(Well)  # identifica plate pelo well
                })
        protocolo.comment(f"CSV carregado com sucesso! {len(volumes)} amostras encontradas.")
    except Exception as e:
        protocolo.comment(f"ERRO: Não foi possível ler o arquivo CSV. Verifique o formato do arquivo. Erro: {e}")
        return

    # Mapeamento de placas
    dna_plate_map = {
        '2': dna_plate_2,
        '3': dna_plate_3,
        '5': dna_plate_5,
        '6': dna_plate_6
    }

    # Distribui diluente
    protocolo.comment("\n---- Adicionando TRIS (diluente) nos poços ----\n")
    p20.pick_up_tip()
    for v in volumes:
        if v['volume_diluente_ul'] > 0:
            p20.transfer(
                v['volume_diluente_ul'],
                water_reservoir.wells()[7],
                final_plate.wells_by_name()[v['well']],
                new_tip='never',
                blow_out=True,
                blowout_location="destination well")
            protocolo.comment(f"{v['sample_id']} ({v['well']}): Diluente: {v['volume_diluente_ul']:.1f} µL")
        else:
            protocolo.comment(f"{v['sample_id']} ({v['well']}): Diluente: 0.0 µL (concentração já abaixo do alvo)")
    p20.drop_tip()

    # Adiciona DNA
    protocolo.comment("\n\n---- Adicionando DNA nos poços ----\n")
    for v in volumes:
        dna_plate = dna_plate_map.get(v['plate'], dna_plate_2)
        p20.pick_up_tip()
        p20.transfer(
            v['volume_dna_ul'],
            dna_plate.wells_by_name()[v['well']],
            final_plate.wells_by_name()[v['well']],
            new_tip='never',
            blow_out=True,
            blowout_location="destination well")
        p20.drop_tip()
        protocolo.comment(f"{v['sample_id']} ({v['well']}): DNA: {v['volume_dna_ul']:.1f} µL")