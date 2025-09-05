from opentrons import protocol_api
from opentrons.protocol_api import ProtocolContext
import csv

metadata = {
    'protocolName': 'Normalização de DNA',
    'author': 'Kailane',
    'description': 'Leitura de CSV, calculo de volumes de diluição, normalização e criação de relatório',
    'apiLevel': '2.15'}

class Normalizacao:
    def __init__(self, protocol: ProtocolContext):
        self.protocol = protocol
        self.target_conc = 30.0  # ng/µL
        self.final_volume = 20.0  # µL
        self.original_conc = 0.0
        self.dna_plate_1 = None
        self.dna_plate_2 = None
        self.dna_plate_3 = None
        self.dna_plate_4 = None
        self.final_plate = None
        self.water_reservoir = None
        self.tip_rack_1 = None
        self.tip_rack_2 = None
        self.p300 = None
        self.source_plates = {}

    def run(self,ctx):
        dna_plate_1 = ctx.load_labware('opentrons_24_tuberack_nest_1.5ml_snapcap', '2', 'Placa de amostras 1')
        dna_plate_2 = ctx.load_labware('opentrons_24_tuberack_nest_1.5ml_snapcap', '3', 'Placa de amostras 2')
        dna_plate_3 = ctx.load_labware('opentrons_24_tuberack_nest_1.5ml_snapcap', '5', 'Placa de amostras 3')
        dna_plate_4 = ctx.load_labware('opentrons_24_tuberack_nest_1.5ml_snapcap', '6', 'Placa de amostras 4')
        final_plate = ctx.load_labware('opentrons_96_wellplate_200ul_pcr_full_skirt', '1', 'Placa Final (96 poços)')
        water_reservoir = ctx.load_labware('usascientific_12_reservoir_22ml', '4', 'Reservatório de Água')
        tip_rack_1 = ctx.load_labware('opentrons_96_tiprack_300ul', '8', 'Rack de ponteiras 1')
        tip_rack_2 = ctx.load_labware('opentrons_96_tiprack_300ul', '9', 'Rack de ponteiras 2')
        #tip_rack_1 = ctx.load_labware('opentrons_96_filtertiprack_20ul', '8', 'Rack de ponteiras 1')
        #tip_rack_2 = ctx.load_labware('opentrons_96_filtertiprack_20ul', '9', 'Rack de ponteiras 2')
        #p20 = ctx.load_instrument('p20_single_gen2', 'left', tip_racks=[tip_rack_1, tip_rack_2])
        p300 = ctx.load_instrument('p300_single_gen2', 'left', tip_racks=[tip_rack_1, tip_rack_2])
        source_plates = {
            'dna_plate_1': dna_plate_1,
            'dna_plate_2': dna_plate_2,
            'dna_plate_3': dna_plate_3,
            'dna_plate_4': dna_plate_4,
        }
        self.load_data()
        self.calculate_volumes()
        self.transfer_tris()
        self.transfer_dna()
    
    def load_data(self):
        pass
    
    def calculate_volumes(self, original_conc):
        pass

    def transfer_tris(self):
        pass

    def transfer_dna(self):
        pass

