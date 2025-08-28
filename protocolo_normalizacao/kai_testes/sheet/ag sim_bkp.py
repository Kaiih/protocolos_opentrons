from opentrons import protocol_api, types
import csv
import os

metadata = {
    'protocolName': 'Teste',
    'author': 'Kai',
    'apiLevel': '2.15'
}

def run(protocolo):
    # Definindo os labwares
    final_plate = protocolo.load_labware('opentrons_96_wellplate_200ul_pcr_full_skirt', '1')
    dna_plate_2 = protocolo.load_labware('corning_24_wellplate_3.4ml_flat', '2')
    dna_plate_3 = protocolo.load_labware('corning_24_wellplate_3.4ml_flat', '3')
    water_reservoir = protocolo.load_labware('usascientific_12_reservoir_22ml', '4')
    dna_plate_5 = protocolo.load_labware('corning_24_wellplate_3.4ml_flat', '5')
    dna_plate_6 = protocolo.load_labware('corning_24_wellplate_3.4ml_flat', '6')
    tip_rack_1 = protocolo.load_labware('opentrons_96_filtertiprack_20ul', '8')
    tip_rack_2 = protocolo.load_labware('opentrons_96_filtertiprack_20ul', '9')

    p20 = protocolo.load_instrument('p20_single_gen2', 'left', tip_racks=[tip_rack_1, tip_rack_2])

    # Caminho do CSV (ajustado para Linux)
    path_csv = 'scripts/tcc/sheet/saida.csv'

    target_concentration = 30.0
    target_volume = 20.0

#quadrante inferior esquerdo | slot 2
    volumes = [1, 2, 1.5, 2.5, 1, 2, 1.5, 2.5, 1, 2, 1.5, 2.5, 1, 2, 1.5, 2.5, 1, 2, 1.5, 2.5, 1, 2, 1.5, 2.5]
    sources = [
        dna_plate_2["A1"], dna_plate_2["B1"], dna_plate_2["C1"], dna_plate_2["D1"],
        dna_plate_2["A2"], dna_plate_2["B2"], dna_plate_2["C2"], dna_plate_2["D2"],
        dna_plate_2["A3"], dna_plate_2["B3"], dna_plate_2["C3"], dna_plate_2["D3"],
        dna_plate_2["A4"], dna_plate_2["B4"], dna_plate_2["C4"], dna_plate_2["D4"],
        dna_plate_2["A5"], dna_plate_2["B5"], dna_plate_2["C5"], dna_plate_2["D5"],
        dna_plate_2["A6"], dna_plate_2["B6"], dna_plate_2["C6"], dna_plate_2["D6"]
    ]
    dests = [
        final_plate["E1"], final_plate["F1"], final_plate["G1"], final_plate["H1"],
        final_plate["E2"], final_plate["F2"], final_plate["G2"], final_plate["H2"],
        final_plate["E3"], final_plate["F3"], final_plate["G3"], final_plate["H3"],
        final_plate["E4"], final_plate["F4"], final_plate["G4"], final_plate["H4"],
        final_plate["E5"], final_plate["F5"], final_plate["G5"], final_plate["H5"],
        final_plate["E6"], final_plate["F6"], final_plate["G6"], final_plate["H6"]
    ]

    for vol, src, dst in zip(volumes, sources, dests):
        p20.pick_up_tip()
        p20.transfer(
            vol,
            src,
            dst,
            new_tip='never'
        )
        p20.drop_tip()

#quadrante inferior esquerdo | slot 3

    for vol, src, dst in zip(volumes, sources, dests):
        p20.pick_up_tip()
        p20.transfer(
            vol,
            src,
            dst,
            new_tip='never'
        )
        p20.drop_tip()

#quadrante superior esquerdo | slot 5

    for vol, src, dst in zip(volumes, sources, dests):
        p20.pick_up_tip()
        p20.transfer(
            vol,
            src,
            dst,
            new_tip='never'
        )
        p20.drop_tip()

#quadrante superior direito | slot 6



    for vol, src, dst in zip(volumes, sources, dests):
        p20.pick_up_tip()
        p20.transfer(
            vol,
            src,
            dst,
            new_tip='never'
        )
        p20.drop_tip()