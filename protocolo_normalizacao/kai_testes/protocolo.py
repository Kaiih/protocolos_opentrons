from opentrons import protocol_api
import csv
import os

metadata = {
    'protocolName': 'Teste',
    'apiLevel': '2.15'
}

def run(protocolo):
    # Definindo os labwares
    final_plate = protocolo.load_labware('opentrons_96_wellplate_200ul_pcr_full_skirt', '1')
    dna_plate_1 = protocolo.load_labware('corning_24_wellplate_3.4ml_flat', '2')
    dna_plate_2 = protocolo.load_labware('corning_24_wellplate_3.4ml_flat', '3')
    water_reservoir = protocolo.load_labware('usascientific_12_reservoir_22ml', '4')
    dna_plate_3 = protocolo.load_labware('corning_24_wellplate_3.4ml_flat', '5')
    dna_plate_4 = protocolo.load_labware('corning_24_wellplate_3.4ml_flat', '6')
    tiprack_20ul_1 = protocolo.load_labware('opentrons_96_filtertiprack_20ul', '8')
    tiprack_20ul_2 = protocolo.load_labware('opentrons_96_filtertiprack_20ul', '9')

    p20 = protocolo.load_instrument('p20_single_gen2', 'left', tip_racks=[tiprack_20ul_1, tiprack_20ul_2])

    # caminho csv
    #path_csv = "\data\user_storage\protocolos\diluicao_teste.csv"
    path_csv = "diluicao_teste.csv"

    if not os.path.exists(path_csv):
        protocolo.comment(f"Arquivo CSV não encontrado")
        return  

    protocolo.comment(f"Arquivo CSV encontrado!")
    
    dados_biblioteca = []
    try:
        with open(path_csv, mode='r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                dados_biblioteca.append(row)
        protocolo.comment(f"csv ok!{len(dados_biblioteca)} amostras encontradas.")
    except Exception as e:
        protocolo.comment(f"Erro: {e}")
        return

    # calcular volumes
    volumes = []
    for i, data in enumerate(dados_biblioteca):
        try:
            sample_Plate = data['Plate']
            sample_well_name = data['Well']
            if len(sample_well_name) == 3 and sample_well_name[1] == '0':
                sample_well_name = sample_well_name[0] + sample_well_name[2]
            sample_id = data['Sample Name']
            sample_concentration = float(data['Concentration (Qubit) ng/µL'])
            target_concentration = 30.0
            target_volume = 20.0
        except (ValueError, KeyError) as e:
            protocolo.comment(f"Erro: {e}. Pulando amostra {data.get('Sample Name', 'N/A')}.")
            continue

        if sample_concentration <= target_concentration:
            volume_dna_ul = target_volume
            volume_diluente_ul = 0
        else:
            volume_dna_ul = (target_concentration * target_volume) / sample_concentration
            volume_diluente_ul = target_volume - volume_dna_ul

        volume_dna_ul = float(f"{volume_dna_ul:.1f}")
        volume_diluente_ul = float(f"{volume_diluente_ul:.1f}")

        volumes.append({
            'sample_id': sample_id,
            'well': sample_well_name,
            'volume_dna_ul': volume_dna_ul,
            'volume_diluente_ul': volume_diluente_ul,
            'plate': sample_Plate
        })

    dna_plate_map = {
        'Plate1': dna_plate_1,
        'Plate2': dna_plate_2,
        'Plate3': dna_plate_3,
        'Plate4': dna_plate_4
    }

  
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

    protocolo.comment("\n\n---- Adicionando DNA nos poços ----\n")
    for v in volumes:
        dna_plate = dna_plate_map.get(v['plate'], dna_plate_1)
        #p20.pick_up_tip() #new_tip está true
        p20.transfer(
            v['volume_dna_ul'],
            dna_plate.wells_by_name()[v['well']],
            final_plate.wells_by_name()[v['well']],
            new_tip='always', 
            blow_out=True,
            blowout_location="destination well")
        #p20.drop_tip()#new_tip está true
        protocolo.comment(f"{v['sample_id']} ({v['well']}): DNA: {v['volume_dna_ul']:.1f} µL")
