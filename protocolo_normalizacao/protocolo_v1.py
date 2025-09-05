from opentrons import protocol_api
from opentrons.protocol_api import ProtocolContext
import csv

metadata = {
    'protocolName': 'Normalização de DNA',
    'author': 'Kailane',
    'description': 'Leitura de CSV, calculo de volumes de diluição, normalização e criação de relatório',
    'apiLevel': '2.15'}

class Normalizacao(ProtocolContext):
    def __init__(self, protocol: ProtocolContext):
        self.protocol = protocol
        self.target_conc = 30.0  # ng/µL
        self.final_volume = 20.0  # µL

    def run(self,ctx):
        pass
    
    def load_data(self):
        pass
    
    def calculate_volumes(self, original_conc):
        pass

    def transfer_tris(self):
        pass

    def transfer_dna(self):
        pass

