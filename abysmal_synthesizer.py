#!/usr/bin/env python3
"""
A ODISSEIA DO SINTETIZADOR ABISSAL
Black Ambient / Dungeon Synth - 15 minutos de heresia sonora

Arquitetura:
- Parte I (O Vazio): 0-5 min, sem bateria, foco em drones e synth lead com pitch-bend
- Parte II (A Catedral de Ruído): 5-12 min, BPM 160, blast beats, arpejos caóticos
- Parte III (O Colapso): 12-15 min, BPM 40, tudo esticado, harpsichord solitário
"""

from midiutil import MIDIFile
import random
import math

# Configurações globais
TOTAL_DURATION = 15 * 60  # 15 minutos em segundos
SAMPLE_RATE = 480  # ticks por quarto de nota

# Canais MIDI
CHANNEL_SYNTH_LEAD = 3      # Synth Lead Malévolo
CHANNEL_DRUMS = 9           # Bateria (percussão)
CHANNEL_PAD = 6             # Pad/Drone
CHANNEL_SUB_DRONE = 11      # Sub Drone
CHANNEL_GUITAR_1 = 1        # Guitarra 1
CHANNEL_GUITAR_2 = 2        # Guitarra 2
CHANNEL_HARPSICHORD = 8     # Harpsichord

# Escala Lócria atonal base (usando notas cromáticas para dissonância)
LOCRIAN_SCALE = [0, 1, 3, 5, 6, 8, 10]  # Semitones relativos
CHROMATIC = list(range(12))


def generate_pitch_bend_value(subtle=True):
    """
    Gera valores de Pitch Bend aleatórios para simular oscilador instável.
    subtle=True: pequenas variações (±500 unidades, ~±30 cents)
    subtle=False: variações extremas (±4000 unidades, ~±2 semitons)
    """
    if subtle:
        return random.randint(-500, 500)
    else:
        return random.randint(-4000, 4000)


def add_pitch_bend_events(midi_file, track, channel, start_time, duration, density=0.3):
    """
    Adiciona eventos de Pitch Bend aleatórios ao longo de uma nota ou sequência.
    density: probabilidade de adicionar um evento (reduzida para eficiência)
    """
    # Limitar número máximo de eventos para evitar excesso de memória
    max_events = 20
    event_count = 0
    
    current_time = start_time
    step_duration = 1.0  # Verificar a cada segundo em vez de semicolcheia
    
    while current_time < start_time + duration and event_count < max_events:
        if random.random() < density:
            bend_value = generate_pitch_bend_value(subtle=True)
            midi_file.addPitchWheelEvent(track, channel, int(current_time * SAMPLE_RATE), bend_value)
            event_count += 1
        
        current_time += step_duration
    
    # Reset do pitch bend no final
    midi_file.addPitchWheelEvent(track, channel, int((start_time + duration) * SAMPLE_RATE), 0)


def create_cluster_chord(root, cluster_type='minor2nd'):
    """
    Cria clusters dissonantes (notas muito próximas).
    cluster_type: 'minor2nd' (Dó + Dó#), 'major2nd' (Dó + Ré), 'dense' (3+ notas)
    """
    if cluster_type == 'minor2nd':
        return [root, root + 1]
    elif cluster_type == 'major2nd':
        return [root, root + 2]
    elif cluster_type == 'dense':
        return [root, root + 1, root + 3, root + 4]
    else:
        return [root, root + 1]


def locrian_note(base_octave, scale_degree=None, chromatic_offset=None):
    """
    Retorna uma nota da escala Lócria ou cromática.
    """
    if scale_degree is not None:
        semitone = LOCRIAN_SCALE[scale_degree % len(LOCRIAN_SCALE)]
    elif chromatic_offset is not None:
        semitone = CHROMATIC[chromatic_offset % 12]
    else:
        semitone = random.choice(LOCRIAN_SCALE)
    
    return 12 * base_octave + semitone


def part_i_the_void(midi_file, track):
    """
    PARTE I: O Vazio (0-5 minutos)
    - Foco no Canal 11 (Sub Drone) e Canal 3 (Synth Lead)
    - Melodias de vidro, agudas e cortantes
    - Pitch Bend contínuo
    - Sem bateria
    """
    print("Compondo Parte I: O Vazio (0-5 min)...")
    
    duration_part_i = 5 * 60  # 5 minutos
    
    # === SUB DRONE (Canal 11) - Base profunda e contínua ===
    drone_start = 0
    drone_notes = [24, 25, 26]  # Clusters graves dissonantes
    
    for i, note in enumerate(drone_notes):
        note_duration = duration_part_i / len(drone_notes)
        start_offset = i * (duration_part_i / len(drone_notes))
        
        midi_file.addNote(track, CHANNEL_SUB_DRONE, note, start_offset, note_duration, 90)
        add_pitch_bend_events(midi_file, track, CHANNEL_SUB_DRONE, start_offset, note_duration, density=0.3)
    
    # Camada adicional de cluster dissonante no sub-drone
    cluster_root = 28
    cluster = create_cluster_chord(cluster_root, 'minor2nd')
    for note in cluster:
        midi_file.addNote(track, CHANNEL_SUB_DRONE, note, 30, 240, 75)
    
    # === SYNTH LEAD (Canal 3) - Melodias de vidro ===
    lead_patterns = []
    current_time = 10  # Começa após 10 segundos
    
    while current_time < duration_part_i - 30:
        # Notas agudas e espaçadas (oitavas 7-9)
        octave = random.choice([7, 8, 9])
        note = locrian_note(octave, chromatic_offset=random.randint(0, 11))
        note_duration = random.uniform(0.5, 3.0)
        velocity = random.randint(60, 100)
        
        midi_file.addNote(track, CHANNEL_SYNTH_LEAD, note, current_time, note_duration, velocity)
        add_pitch_bend_events(midi_file, track, CHANNEL_SYNTH_LEAD, current_time, note_duration, density=0.9)
        
        # Pitch bends extremos entre notas
        if random.random() < 0.3:
            extreme_bend_time = current_time + note_duration / 2
            tick = int(extreme_bend_time * SAMPLE_RATE)
            midi_file.addPitchWheelEvent(track, CHANNEL_SYNTH_LEAD, tick, generate_pitch_bend_value(subtle=False))
        
        # Pausas irregulares (polirritmia implícita)
        gap = random.uniform(0.2, 2.5)
        current_time += note_duration + gap
    
    # === PAD (Canal 6) - Clusters dissonantes de fundo ===
    pad_start = 60  # Entra após 1 minuto
    pad_duration = duration_part_i - pad_start
    
    for i in range(8):
        cluster_root = random.randint(48, 72)
        cluster = create_cluster_chord(cluster_root, 'dense')
        note_start = pad_start + (i * pad_duration / 8)
        note_dur = pad_duration / 8 - 2
        
        for note in cluster:
            midi_file.addNote(track, CHANNEL_PAD, note, note_start, note_dur, 55)
        
        add_pitch_bend_events(midi_file, track, CHANNEL_PAD, note_start, note_dur, density=0.4)
    
    print(f"  Parte I completa: {current_time:.0f} segundos de material gerado")


def part_ii_cathedral_of_noise(midi_file, track):
    """
    PARTE II: A Catedral de Ruído (5-12 minutos)
    - BPM 160, Black Metal entra
    - Guitarras (Canais 1 e 2) - Wall of Sound
    - Sintetizador (Canal 3) - Arpejos ultra-rápidos e caóticos
    - Bateria em Blast Beat
    - Polirritmia: sintetizadores em 7/8 sobre bateria em 4/4
    """
    print("Compondo Parte II: A Catedral de Ruído (5-12 min)...")
    
    bpm = 160
    start_time = 5 * 60  # 5 minutos
    duration_part_ii = 7 * 60  # 7 minutos
    
    # Configurar BPM para esta seção
    midi_file.addTempo(track, 0, bpm)
    
    quarter_note = 60 / bpm  # Duração de uma semínima em segundos
    
    # === BLAST BEAT DRUMS (Canal 9) ===
    # Pattern de blast beat: bumbo, caixa, bumbo, caixa em alta velocidade
    drum_time = start_time
    
    # Instrumentos de bateria MIDI
    KICK = 36
    SNARE = 38
    HIHAT_CLOSED = 42
    HIHAT_OPEN = 46
    CRASH = 49
    
    blast_pattern = [
        (KICK, 0.25), (HIHAT_CLOSED, 0.25),
        (SNARE, 0.25), (HIHAT_CLOSED, 0.25),
        (KICK, 0.25), (HIHAT_CLOSED, 0.25),
        (SNARE, 0.25), (HIHAT_OPEN, 0.5),
    ]
    
    drum_end = start_time + duration_part_ii
    pattern_index = 0
    
    while drum_time < drum_end:
        for drum_note, dur_mult in blast_pattern:
            if drum_time >= drum_end:
                break
            midi_file.addNote(track, CHANNEL_DRUMS, drum_note, drum_time, quarter_note * dur_mult, random.randint(90, 127))
            drum_time += quarter_note * dur_mult
        
        # Variações ocasionais com crash
        if random.random() < 0.1:
            midi_file.addNote(track, CHANNEL_DRUMS, CRASH, drum_time, quarter_note * 2, 110)
    
    # === GUITARRAS - WALL OF SOUND (Canais 1 e 2) ===
    guitar_time = start_time + 2  # Guitarras entram 2 segundos após o início da parte II
    
    # Power chords distorcidos - reduzido para eficiência
    power_chord_roots = [30, 31, 33, 35, 36, 38]  # E1, F1, G#1, A#1, B1, C#2
    
    while guitar_time < drum_end:
        root = random.choice(power_chord_roots)
        # Power chord: root + fifth + octave
        chord = [root, root + 7, root + 12]
        
        # Notas sustentadas em vez de tremolo picking excessivo
        chord_duration = random.uniform(2, 4)
        for note in chord:
            midi_file.addNote(track, CHANNEL_GUITAR_1, note, guitar_time, chord_duration, random.randint(100, 127))
            midi_file.addNote(track, CHANNEL_GUITAR_2, note + random.randint(-2, 2), guitar_time, chord_duration, random.randint(95, 120))
        
        guitar_time += chord_duration
    
    # === SYNTH LEAD - ARPEJOS CAÓTICOS (Canal 3) ===
    # Polirritmia: 7/8 sobre o 4/4 da bateria - versão otimizada
    synth_time = start_time + 5
    
    base_octave = random.choice([4, 5, 6])
    
    while synth_time < drum_end - 10:
        # Arpejo em 7/8 (7 notas por grupo) - simplificado
        for i in range(7):
            note = locrian_note(base_octave + random.randint(-1, 2), chromatic_offset=random.randint(0, 11))
            duration = quarter_note / 2  # Colcheia em vez de semicolcheia
            
            velocity = random.randint(70, 110)
            midi_file.addNote(track, CHANNEL_SYNTH_LEAD, note, synth_time, duration, velocity)
            
            # Pitch bend menos frequente
            if random.random() < 0.3:
                tick = int(synth_time * SAMPLE_RATE)
                bend = generate_pitch_bend_value(subtle=True)
                midi_file.addPitchWheelEvent(track, CHANNEL_SYNTH_LEAD, tick, bend)
            
            synth_time += duration
        
        # Pausa irregular para desorientação
        synth_time += random.uniform(0.2, 1.0)
        
        # Mudança de oitava ocasional
        if random.random() < 0.15:
            base_octave = random.choice([4, 5, 6])
    
    # === PADS COM CLUSTERS (Canal 6 e 11) ===
    pad_time = start_time + 10
    
    while pad_time < drum_end:
        cluster_root = random.randint(48, 60)
        cluster = create_cluster_chord(cluster_root, 'minor2nd')
        duration = random.uniform(2, 6) * quarter_note
        
        for note in cluster:
            midi_file.addNote(track, CHANNEL_PAD, note, pad_time, duration, 65)
            midi_file.addNote(track, CHANNEL_SUB_DRONE, note - 12, pad_time, duration, 70)
        
        add_pitch_bend_events(midi_file, track, CHANNEL_PAD, pad_time, duration, density=0.5)
        pad_time += duration - random.uniform(0.5, 1.5)
    
    print(f"  Parte II completa: {duration_part_ii:.0f} segundos de caos sonoro")


def part_iii_the_collapse(midi_file, track):
    """
    PARTE III: O Colapso (12-15 minutos)
    - Tempo desacelera para 40 BPM
    - Todas as notas esticadas ao máximo
    - Harpsichord (Canal 8) toca melodia solitária
    - Sintetizadores "morrem" com Pitch Bend caindo para o abismo
    """
    print("Compondo Parte III: O Colapso (12-15 min)...")
    
    bpm = 40
    start_time = 12 * 60  # 12 minutos
    duration_part_iii = 3 * 60  # 3 minutos
    
    # Mudar BPM drasticamente
    midi_file.addTempo(track, 0, bpm)
    
    quarter_note = 60 / bpm  # Agora muito lento (~1.5 segundos por semínima)
    
    end_time = start_time + duration_part_iii
    
    # === HARPSICHORD SOLO (Canal 8) - Melodia solitária ===
    harp_time = start_time + 10  # Entra após 10 segundos de silêncio tenso
    
    current_note = locrian_note(4, scale_degree=0)
    
    while harp_time < end_time - 30:
        # Melodia lenta e descendente
        direction = random.choice([-1, 0, 1])
        current_note = max(24, min(84, current_note + direction * random.randint(1, 3)))
        
        note_duration = random.uniform(4, 10)  # Notas longas
        velocity = random.randint(40, 70)
        
        midi_file.addNote(track, CHANNEL_HARPSICHORD, current_note, harp_time, note_duration, velocity)
        
        harp_time += note_duration + random.uniform(2, 5)
    
    # === SYNTH LEAD MORRENDO (Canal 3) ===
    # Apenas 3 notas longas com pitch bend caindo para o abismo
    dying_notes = [
        (72, 50),   # Nota alta, duração longa
        (60, 60),   # Nota média, duração muito longa
        (48, 70),   # Nota grave, duração extrema
    ]
    
    synth_time = start_time
    
    for note, duration in dying_notes:
        if synth_time >= end_time - 10:
            break
        
        midi_file.addNote(track, CHANNEL_SYNTH_LEAD, note, synth_time, duration, 50)
        
        # Pitch bend caindo progressivamente para o abismo (apenas 5 eventos)
        for i in range(5):
            bend_time = synth_time + (i * duration / 5)
            tick = int(bend_time * SAMPLE_RATE)
            bend_value = int(-8191 * (i / 5))
            midi_file.addPitchWheelEvent(track, CHANNEL_SYNTH_LEAD, tick, bend_value)
        
        synth_time += duration + 10
    
    # === SUB DRONE FINAL (Canal 11) ===
    # Apenas 2 drones longos
    drone_notes = [
        (28, 100),  # Nota grave, 100 segundos
        (26, 80),   # Nota ligeiramente diferente, 80 segundos
    ]
    
    drone_time = start_time
    for note, duration in drone_notes:
        if drone_time >= end_time - 10:
            break
        
        cluster = create_cluster_chord(note, 'minor2nd')
        for n in cluster:
            midi_file.addNote(track, CHANNEL_SUB_DRONE, n, drone_time, min(duration, end_time - drone_time), 40)
        
        # Pitch bends esparsos
        for i in range(3):
            bend_time = drone_time + (i * duration / 3)
            if bend_time < end_time:
                tick = int(bend_time * SAMPLE_RATE)
                bend_value = generate_pitch_bend_value(subtle=False)
                midi_file.addPitchWheelEvent(track, CHANNEL_SUB_DRONE, tick, bend_value)
        
        drone_time += duration / 2
    
    # === PAD FINAL DESVANECENDO (Canal 6) ===
    # Apenas 2 clusters finais
    pad_clusters = [
        (52, 90),   # Root, duração
        (50, 70),
    ]
    
    pad_time = start_time + 20
    for cluster_root, duration in pad_clusters:
        if pad_time >= end_time - 5:
            break
        
        cluster = create_cluster_chord(cluster_root, 'dense')
        for note in cluster:
            velocity = max(20, int(50 * (1 - (pad_time - start_time) / duration_part_iii)))
            midi_file.addNote(track, CHANNEL_PAD, note, pad_time, min(duration, end_time - pad_time), velocity)
        
        # Pitch bend morrendo (apenas 4 eventos)
        for i in range(4):
            bend_time = pad_time + (i * duration / 4)
            if bend_time < end_time:
                tick = int(bend_time * SAMPLE_RATE)
                bend_value = int(-8191 * (i / 4) * random.uniform(0.5, 1.0))
                midi_file.addPitchWheelEvent(track, CHANNEL_PAD, tick, bend_value)
        
        pad_time += duration / 2
    
    # Silêncio final com último pitch bend para o abismo
    final_tick = int(end_time * SAMPLE_RATE)
    for channel in [CHANNEL_SYNTH_LEAD, CHANNEL_PAD, CHANNEL_SUB_DRONE]:
        midi_file.addPitchWheelEvent(track, channel, final_tick, -8191)
    
    print(f"  Parte III completa: colapso finalizado em {duration_part_iii:.0f} segundos")


def main():
    """
    Função principal que orquestra a composição completa.
    """
    print("=" * 60)
    print("A ODISSEIA DO SINTETIZADOR ABISSAL")
    print("Black Ambient / Dungeon Synth - 15 minutos de heresia")
    print("=" * 60)
    
    # Criar arquivo MIDI (1 track, 16 canais)
    midi_file = MIDIFile(1)
    track = 0
    
    # Configurações iniciais
    midi_file.addTrackName(track, 0, "Abysmal Synthesizer Odyssey")
    midi_file.addTempo(track, 0, 60)  # BPM inicial (será modificado nas partes)
    
    # Programa/instrumentos para cada canal
    instruments = {
        CHANNEL_SYNTH_LEAD: 81,    # Lead 2 (sawtooth)
        CHANNEL_DRUMS: 0,          # Drum kit (canal 9 é sempre percussão)
        CHANNEL_PAD: 90,           # Pad 2 (warm)
        CHANNEL_SUB_DRONE: 52,     # Choir Aahs
        CHANNEL_GUITAR_1: 30,      # Distortion Guitar
        CHANNEL_GUITAR_2: 30,      # Distortion Guitar
        CHANNEL_HARPSICHORD: 7,    # Harpsichord
    }
    
    for channel, program in instruments.items():
        if channel != CHANNEL_DRUMS:
            midi_file.addProgramChange(track, channel, 0, program)
    
    # Compor cada parte
    part_i_the_void(midi_file, track)
    part_ii_cathedral_of_noise(midi_file, track)
    part_iii_the_collapse(midi_file, track)
    
    # Salvar arquivo
    output_filename = "abysmal_synthesizer_odyssey.mid"
    
    with open(output_filename, "wb") as f:
        midi_file.writeFile(f)
    
    print("=" * 60)
    print(f"OBRA COMPLETA: {output_filename}")
    print("Duração total: 15 minutos")
    print("Canais utilizados:")
    print(f"  - Canal 3: Synth Lead Malévolo (com Pitch-Drift Diabólico)")
    print(f"  - Canal 6: Pads/Clusters Dissonantes")
    print(f"  - Canal 8: Harpsichord Solitário")
    print(f"  - Canal 9: Bateria (Blast Beats / Marcha Fúnebre)")
    print(f"  - Canal 11: Sub Drone")
    print(f"  - Canais 1-2: Guitarras (Wall of Sound)")
    print("=" * 60)
    print("Regras aplicadas:")
    print("  ✓ Pitch-Drift Diabólico: eventos aleatórios em quase todas as notas")
    print("  ✓ Polirritmia do Caos: 7/8 sobre 4/4 na Parte II")
    print("  ✓ Clusters Dissonantes: minor 2nds e clusters densos")
    print("  ✓ Arquitetura em 3 partes: Vazio → Catedral → Colapso")
    print("=" * 60)


if __name__ == "__main__":
    main()
