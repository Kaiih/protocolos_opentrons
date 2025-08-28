metadata = {
    'protocolName': 'Melhoria Processo NGS',
    'author': ' <>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.11'
}

# Lista de dados extraída do CSV
dados = [
    ['S1', 39.40],
    ['S2', 10.40],
    ['S3', 40.40],
    ['S4', 48.30],
    ['S5', 62.70],
    # ...adicione todas as linhas do seu CSV aqui...
    ['S68', 56.00],
    ['S69', 68.00],
    ['S70', 141.00],
    ['S71', 3.32],
    ['S72', 7.20]
]

# Mapeamento S1-S72 para A1-H12 (96-well plate)
rows = "ABCDEFGH"
s_to_well = {}
for i in range(72):
    row = rows[i % 8]
    col = i // 8 + 1
    s_to_well[f"S{i+1}"] = f"{row}{col:02d}"  # <-- dois dígitos

def run(ctx):
    # labware
    reservoir = ctx.load_labware('nest_12_reservoir_15ml', 1)
    dna_plate = ctx.load_labware('corning_96_wellplate_360ul_flat', 2)
    final_plate = ctx.load_labware('nest_96_wellplate_100ul_pcr_full_skirt', 3)
    tips = [ctx.load_labware('opentrons_96_filtertiprack_20ul', slot) for slot in [10, 11]]
    p20 = ctx.load_instrument('p20_single_gen2', 'left', tip_racks=tips)

    water = reservoir.wells()[0]

    # Parâmetros desejados
    c2 = 30  # concentração desejada em ng/µL
    v2 = 20  # volume final em µL

    ctx.comment('\n------------ADICIONANDO ÁGUA (TRIS) NA PLACA-------------\n\n')
    for dest_well_name, c1 in dados:
        well_name = s_to_well[dest_well_name]
        dest_well = final_plate.wells_by_name()[well_name]

        if c1 <= 0:
            ctx.comment(f"Concentração inválida para {dest_well_name}, pulando.")
            continue

        v1 = (c2 * v2) / c1  # volume de DNA
        agua = v2 - v1       # volume de água

        # Garante volumes positivos e dentro do range da pipeta
        if v1 > v2 or v1 < 0 or agua < 0:
            ctx.comment(f"Volume calculado inválido para {dest_well_name}, pulando.")
            continue

        # Adiciona água primeiro
        if agua > 0:
            p20.pick_up_tip()
            p20.transfer(agua, water, dest_well, new_tip='never',
                         blow_out=True,
                         blowout_location="destination well")
            p20.drop_tip()

    ctx.comment('\n------------ADICIONANDO DNA NA PLACA-------------\n\n')
    for source_well_name, c1 in dados:
        well_name = s_to_well[source_well_name]
        source_well = dna_plate.wells_by_name()[well_name]
        dest_well = final_plate.wells_by_name()[well_name]

        if c1 <= 0:
            continue

        v1 = (c2 * v2) / c1  # volume de DNA

        if v1 > v2 or v1 < 0:
            continue

        p20.pick_up_tip()
        p20.transfer(v1, source_well.bottom(z=1), dest_well, new_tip='never',
                     blow_out=True,
                     blowout_location="destination well")
        p20.drop_tip()