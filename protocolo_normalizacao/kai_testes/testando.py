from opentrons import protocol_api
import csv

metadata = {
    'protocolName': 'Teste',
    'author': 'Kai',
    'description': "",
    'apiLevel': '2.15'
}

def run(protocolo):
    #volume_dna = 0.0
    #volume_diluente = 0.0
    #conc.abaixo =
    final_plate = protocolo.load_labware('opentrons_96_wellplate_200ul_pcr_full_skirt', '1') # Placa de destino
    dna_plate_1 = protocolo.load_labware('corning_24_wellplate_3.4ml_flat', '2') # Placa de amostras de origem
    dna_plate_2 = protocolo.load_labware('corning_24_wellplate_3.4ml_flat', '3') # Placa de amostras de origem
    water_reservoir = protocolo.load_labware('usascientific_12_reservoir_22ml', '4') # Reservatório de diluente (água/buffer)
    dna_plate_3 = protocolo.load_labware('corning_24_wellplate_3.4ml_flat', '5') # Placa de amostras de origem
    dna_plate_4 = protocolo.load_labware('corning_24_wellplate_3.4ml_flat', '6') # Placa de amostras de origem
    tiprack_20ul_1 = protocolo.load_labware('opentrons_96_filtertiprack_20ul', '8') # Rack de pontas
    tiprack_20ul_2 = protocolo.load_labware('opentrons_96_filtertiprack_20ul', '9') # Rack de pontas

    p20 = protocolo.load_instrument('p20_single_gen2', 'left', tip_racks=[tiprack_20ul_1, tiprack_20ul_2])

    # CSV
    csv_path = "/home/kai/Biotrop/opentrons/scripts/tcc/sheet/diluicao_teste.csv"

    # 4. Read CSV
    dados_biblioteca = []
    try:
        with open(csv_path, mode='r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                dados_biblioteca.append(row)
    except FileNotFoundError:
        protocolo.comment(f"Erro: Arquivo CSV não encontrado em {csv_path}.")
        protocolo.pause("Protocolo interrompido devido a arquivo CSV ausente.")
        return 

    volumes = []
    for i, data in enumerate(dados_biblioteca):
        try:
            sample_Plate = data['Plate']
            sample_well_name = data['Well']
            if len(sample_well_name) == 3 and sample_well_name[1] == '0':
                sample_well_name = sample_well_name[0] + sample_well_name[2]
            sample_id = data['Sample Name']
            sample_concentration = float(data['Concentration (Qubit) ng/µL'])
            target_concentration = float(data['TargetConcentration'])
            target_volume = float(data['TargetVolume'])
            
        except (ValueError, KeyError) as e:
            protocolo.comment(f"Erro nos dados da linha {i+1} do CSV: {e}. Pulando amostra {sample_id}.")
            continue

        if sample_concentration <= target_concentration:
            volume_dna_ul = target_concentration
            volume_diluente_ul = 0
            #protocolo.comment(f"Concentração da amostra {sample_id} já está abaixo da desejada.")
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

    #protocolo.comment(f"Amostra {sample_id} diluída para concentração desejada. Volume de DNA: {volume_dna_ul:.1f} µL, Volume de diluente: {volume_diluente_ul:.1f} µL.")
    for v in volumes:
        if v['volume_diluente_ul'] > 0:
            protocolo.comment("\n---- Adicionando TRIS nos poços ----\n")
            p20.pick_up_tip()
            p20.transfer(
                v['volume_diluente_ul'],
                water_reservoir.wells()[7],
                final_plate.wells_by_name()[v['well']],
                new_tip='never',
                blow_out=True,
                blowout_location="destination well")
            p20.drop_tip()
            protocolo.comment(
                f"{v['sample_id']} ({v['well']}): Diluente: {v['volume_diluente_ul']:.1f} µL\n")
            
            protocolo.comment("\n---- Adicionando DNA nos poços ----\n")

            dna_plate = dna_plate_map.get(v['plate'], dna_plate_1)
            # Aqui você pode escolher de qual placa de DNA aspirar, se necessário
            # Exemplo: sempre da dna_plate_1
            p20.pick_up_tip()
            p20.transfer(
                v['volume_dna_ul'],
                dna_plate.wells_by_name()[v['well']],
                final_plate.wells_by_name()[v['well']],
                new_tip='never',
                blow_out=True,
                blowout_location="destination well")
            
            p20.drop_tip()
            protocolo.comment(
                f"{v['sample_id']} ({v['well']}): DNA: {v['volume_dna_ul']:.1f} µL\n")
        else:
            protocolo.comment("\n---- TRIS ----\n")
            protocolo.comment(
                f"{v['sample_id']} ({v['well']}): Diluente: 0.0 µL (concentração já abaixo do alvo)\n")
            
            protocolo.comment("\n---- DNA ----\n")
            dna_plate = dna_plate_map.get(v['plate'], dna_plate_1)
            p20.pick_up_tip()
            p20.transfer(
                v['volume_dna_ul'],
                dna_plate.wells_by_name()[v['well']],
                final_plate.wells_by_name()[v['well']],
                new_tip='never',
                blow_out=True,
                blowout_location="destination well")
            protocolo.comment(
                f"{v['sample_id']} ({v['well']}): DNA: {v['volume_dna_ul']:.1f} µL. Concentração já abaixo do alvo, transferindo volume calculado\n")
            p20.drop_tip()