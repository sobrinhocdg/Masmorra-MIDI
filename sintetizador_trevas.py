#!/usr/bin/env python3
"""
SINTETIZADOR DAS TREVAS CABULOSO - O ÁPICE DO BURZUM
Uma obra de 10 minutos em 3 atos, inspirada no black metal atmosférico.
Gera um arquivo MIDI com 16 canais (0-15).
"""

from midiutil import MIDIFile
import random
import math

# Configurações Gerais
TEMPO_TOTAL_SEGUNDOS = 600  # 10 minutos
BPM_ATO1 = 75
BPM_ATO2 = 140
BPM_ATO3 = 75

# Duração dos atos em compassos (aproximado para 4/4)
# Ato 1: 0-3 min @ 75 BPM ≈ 28 compassos
# Ato 2: 3-7 min @ 140 BPM ≈ 74 compassos (4 min)
# Ato 3: 7-10 min @ 75 BPM ≈ 28 compassos

COMPASSOS_ATO1 = 28
COMPASSOS_ATO2 = 74
COMPASSOS_ATO3 = 28

# Canais MIDI
CH_DRUMS = 9
CH_BAIXO = 2
CH_GUITAR_L = 4
CH_GUITAR_R = 5
CH_VIOLAO = 6
CH_SINOS = 7
CH_CRAVO = 8
CH_PADS = 10
CH_DRONE = 11
CH_SYNTH_LEAD = 3  # Canal do Caos
CH_CORO = 12

# Escala Menor Harmônica de Lá (A Minor Harmonic)
# A, B, C, D, E, F, G#
ESCOLA_BASE = [57, 59, 60, 62, 64, 65, 68]  # A3 a G#4
ESCOLA_AGUDA = [69, 71, 72, 74, 76, 77, 80]  # A4 a G#5
ESCOLA_GRAVE = [45, 47, 48, 50, 52, 53, 56]  # A2 a G#3

def random_velocity(min_vel, max_vel):
    return random.randint(min_vel, max_vel)

def humanize_time(time_offset, intensity=0.05):
    """Adiciona micro-desvios de tempo para desumanização"""
    return time_offset + (random.gauss(0, intensity))

def add_drone(midi, start_time, duration, base_note, channel):
    """Adiciona drone sub-grave contínuo"""
    for i in range(int(duration)):
        midi.addNote(0, channel, base_note, start_time + i, 1, random_velocity(80, 100))
        # Adiciona harmônicos dissonantes
        if i % 4 == 0:
            midi.addNote(0, channel, base_note + 12, start_time + i, 1, random_velocity(40, 60))

def add_blast_beats(midi, start_time, num_measures):
    """Bateria Blast Beats infernais"""
    for m in range(num_measures):
        for beat in range(4):
            time = start_time + m * 4 + beat
            # Bumbo constante
            midi.addNote(0, CH_DRUMS, 36, time, 0.5, random_velocity(90, 120))
            midi.addNote(0, CH_DRUMS, 36, time + 0.5, 0.5, random_velocity(90, 120))
            
            # Caixa flutuante (fora do tempo)
            if beat % 2 == 0:
                offset = random.uniform(-0.08, 0.08)
                midi.addNote(0, CH_DRUMS, 38, time + offset, 0.25, random_velocity(70, 100))
            
            # Chimbal rápido
            for sub in range(4):
                midi.addNote(0, CH_DRUMS, 42, time + sub * 0.25, 0.125, random_velocity(50, 80))

def add_tribal_drums(midi, start_time, num_measures):
    """Bateria tribal lenta - batidas de coração morrendo"""
    for m in range(num_measures):
        time = start_time + m * 4
        # Bumbo lento e espaçado
        midi.addNote(0, CH_DRUMS, 36, time, 1.5, random_velocity(100, 127))
        if m % 2 == 0:
            midi.addNote(0, CH_DRUMS, 36, time + 2, 1.0, random_velocity(80, 100))
        
        # Caixa rara e distante
        if m % 4 == 0:
            offset = random.uniform(-0.15, 0.15)
            midi.addNote(0, CH_DRUMS, 38, time + 2 + offset, 0.5, random_velocity(40, 60))

def add_tremolo_guitars(midi, start_time, num_measures, chord_notes, channel_l, channel_r):
    """Guitarras fazendo tremolo picking contínuo"""
    for m in range(num_measures):
        for beat in range(4):
            time = start_time + m * 4 + beat
            for sub in range(8):  # 8 notas por tempo = tremolo rápido
                note_time = time + sub * 0.125
                # Randomização severa de velocity
                vel = random_velocity(60, 110)
                
                # L e R com pequenas diferenças
                for note in chord_notes:
                    midi.addNote(0, channel_l, note + 12, note_time, 0.125, vel)
                    midi.addNote(0, channel_r, note + 12, note_time + 0.02, 0.125, max(1, vel - 10))

def add_synth_lead_chaos(midi, start_time, num_measures, is_funebre=False):
    """Synth Lead agudo, estridente e melancólico"""
    for m in range(num_measures):
        for beat in range(4):
            time = start_time + m * 4 + beat
            
            # Padrão repetitivo e hipnótico
            if is_funebre:
                # Melodia mais lenta e dolorosa
                if beat % 2 == 0:
                    note = random.choice(ESCOLA_AGUDA)
                    duration = 1.5
                    vel = random_velocity(70, 100)
                    midi.addNote(0, CH_SYNTH_LEAD, note, time, duration, vel)
            else:
                # Melodia rápida e cortante
                note = random.choice(ESCOLA_AGUDA)
                duration = 0.5
                vel = random_velocity(80, 120)
                midi.addNote(0, CH_SYNTH_LEAD, note, time, duration, vel)
                
                # Notas de passagem estridentes
                if beat % 4 == 0:
                    passing_note = note + random.choice([1, 3, -2])
                    midi.addNote(0, CH_SYNTH_LEAD, passing_note, time + 0.5, 0.25, max(1, vel - 20))

def add_acoustic_arpeggios(midi, start_time, num_measures):
    """Violão acústico - arpejos dolorosos e fora do tempo"""
    for m in range(num_measures):
        for beat in range(4):
            time = start_time + m * 4 + beat
            
            # Arpejo fora do tempo
            for i, note in enumerate(random.sample(ESCOLA_BASE, 4)):
                offset = random.uniform(-0.3, 0.3)  # Muito fora do tempo
                vel = random_velocity(30, 70)  # Randomização severa
                midi.addNote(0, CH_VIOLAO, note, time + offset, 0.5, vel)

def add_pads_atmospheric(midi, start_time, num_measures, chord_notes):
    """Pads incrivelmente longos"""
    for m in range(num_measures):
        time = start_time + m * 4
        for note in chord_notes:
            duration = 4  # Nota inteira
            vel = random_velocity(50, 80)
            midi.addNote(0, CH_PADS, note, time, duration, vel)

def add_bells_ice(midi, start_time, num_measures):
    """Sinos Gélidos"""
    for m in range(num_measures):
        if m % 2 == 0:  # Apenas em compassos pares
            time = start_time + m * 4
            note = random.choice(ESCOLA_AGUDA)
            vel = random_velocity(40, 70)
            midi.addNote(0, CH_SINOS, note + 12, time, 2, vel)

def add_harpsichord(midi, start_time, num_measures):
    """Cravo - linhas barrocas distorcidas"""
    for m in range(num_measures):
        for beat in range(4):
            time = start_time + m * 4 + beat
            if random.random() > 0.5:
                note = random.choice(ESCOLA_BASE)
                vel = random_velocity(50, 80)
                midi.addNote(0, CH_CRAVO, note, time, 0.5, vel)

def add_funeral_choir(midi, start_time, num_measures):
    """Coro Fúnebre - notas dissonantes"""
    for m in range(num_measures):
        time = start_time + m * 4
        # Acordes dissonantes
        dissonant_chord = [ESCOLA_BASE[0], ESCOLA_BASE[2], ESCOLA_BASE[5]]  # A, C, F
        for note in dissonant_chord:
            vel = random_velocity(60, 90)
            midi.addNote(0, CH_CORO, note, time, 4, vel)

def add_bass_line(midi, start_time, num_measures, root_notes):
    """Baixo acompanhando as guitarras"""
    for m in range(num_measures):
        for beat in range(4):
            time = start_time + m * 4 + beat
            # Baixo seguindo a raiz
            root = random.choice(root_notes)
            vel = random_velocity(80, 110)
            midi.addNote(0, CH_BAIXO, root, time, 1, vel)

def generate_midi():
    # Criar arquivo MIDI com 16 pistas (uma para cada canal)
    # Desativar deinterleave para evitar erro com notas sobrepostas
    midi = MIDIFile(16, deinterleave=False, removeDuplicates=False)
    
    track = 0
    time = 0
    
    # Configurar tempos para cada seção
    midi.addTempo(track, 0, BPM_ATO1)
    
    print("🎹 Forjando Ato 1: A Masmorra Gélida (0-3 min)...")
    
    # === ATO 1: A MASMORRA GÉLIDA ===
    # Drones e Pads
    add_drone(midi, 0, COMPASSOS_ATO1 * 4, 45, CH_DRONE)  # A1 drone
    add_pads_atmospheric(midi, 0, COMPASSOS_ATO1, [ESCOLA_BASE[0], ESCOLA_BASE[2], ESCOLA_BASE[4]])
    
    # Sinos e Violão
    add_bells_ice(midi, 0, COMPASSOS_ATO1)
    add_acoustic_arpeggios(midi, 0, COMPASSOS_ATO1)
    
    # Cravo esporádico
    add_harpsichord(midi, 0, COMPASSOS_ATO1 // 2)
    
    # Bateria tribal (entra depois de alguns compassos)
    add_tribal_drums(midi, 4, COMPASSOS_ATO1 - 4)
    
    # Transição para Ato 2
    midi.addTempo(track, COMPASSOS_ATO1, BPM_ATO2)
    
    print("🔥 Forjando Ato 2: O Sintetizador das Trevas (3-7 min)...")
    
    # === ATO 2: O SINTETIZADOR DAS TREVAS ===
    ato2_start = COMPASSOS_ATO1
    
    # Drones continuam
    add_drone(midi, ato2_start, COMPASSOS_ATO2 * 4, 45, CH_DRONE)
    
    # Guitarras em tempestade
    guitar_chord = [ESCOLA_BASE[0], ESCOLA_BASE[3], ESCOLA_BASE[5]]  # A, D, F
    add_tremolo_guitars(midi, ato2_start, COMPASSOS_ATO2, guitar_chord, CH_GUITAR_L, CH_GUITAR_R)
    
    # Baixo agressivo
    add_bass_line(midi, ato2_start, COMPASSOS_ATO2, [ESCOLA_GRAVE[0], ESCOLA_GRAVE[3], ESCOLA_GRAVE[5]])
    
    # Blast Beats
    add_blast_beats(midi, ato2_start, COMPASSOS_ATO2)
    
    # SYNTH LEAD DO CAOS (protagonista)
    add_synth_lead_chaos(midi, ato2_start, COMPASSOS_ATO2, is_funebre=False)
    
    # Pads de fundo
    add_pads_atmospheric(midi, ato2_start, COMPASSOS_ATO2, [ESCOLA_BASE[0], ESCOLA_BASE[2], ESCOLA_BASE[6]])
    
    # Transição para Ato 3
    midi.addTempo(track, ato2_start + COMPASSOS_ATO2, BPM_ATO3)
    
    print("💀 Forjando Ato 3: A Ascensão ao Vazio (7-10 min)...")
    
    # === ATO 3: A ASCENSÃO AO VAZIO ===
    ato3_start = ato2_start + COMPASSOS_ATO2
    
    # Metal cessa abruptamente - só restam Synth Lead e Coro
    
    # Synth Lead mais lento e doloroso
    add_synth_lead_chaos(midi, ato3_start, COMPASSOS_ATO3, is_funebre=True)
    
    # Coro Fúnebre dissonante
    add_funeral_choir(midi, ato3_start, COMPASSOS_ATO3)
    
    # Drone final que vai desaparecendo
    for m in range(COMPASSOS_ATO3):
        time_pos = ato3_start + m * 4
        volume_decay = int(100 * (1 - m / COMPASSOS_ATO3))
        if volume_decay > 0:
            midi.addNote(0, CH_DRONE, 45, time_pos, 4, max(20, volume_decay))
    
    # Sinos finais espaçados
    for m in range(0, COMPASSOS_ATO3, 4):
        time_pos = ato3_start + m * 4
        midi.addNote(0, CH_SINOS, ESCOLA_AGUDA[0], time_pos, 6, 30)
    
    # Simular fita cassete derretendo - notas cada vez mais espaçadas
    for i in range(5):
        time_pos = ato3_start + COMPASSOS_ATO3 * 4 - (5 - i) * 8
        if time_pos > ato3_start:
            midi.addNote(0, CH_SYNTH_LEAD, ESCOLA_AGUDA[0], time_pos, 2, 20)
    
    # Salvar arquivo
    filename = "sintetizador_das_trevas_cabuloso.mid"
    with open(filename, 'wb') as f:
        midi.writeFile(f)
    
    print(f"\n✅ OBRA COMPLETA: {filename}")
    print("📊 Estrutura:")
    print(f"   Ato 1: 0-{COMPASSOS_ATO1 * (60/BPM_ATO1 * 4):.0f}s - A Masmorra Gélida")
    print(f"   Ato 2: {COMPASSOS_ATO1 * (60/BPM_ATO1 * 4):.0f}-{(COMPASSOS_ATO1 + COMPASSOS_ATO2) * (60/BPM_ATO2 * 4):.0f}s - O Sintetizador das Trevas")
    print(f"   Ato 3: {(COMPASSOS_ATO1 + COMPASSOS_ATO2) * (60/BPM_ATO2 * 4):.0f}-600s - A Ascensão ao Vazio")
    print("\n🎹 Canais utilizados:")
    print("   0-2, 4-8, 10-12: Instrumentos melódicos")
    print("   3: Canal do Caos (Synth Lead)")
    print("   9: Bateria")
    print("   13-15: Reservados")

if __name__ == "__main__":
    generate_midi()
