#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Taverna das Sombras - Black Metal / Dungeon Synth Generator
Gera um arquivo MIDI de 8 minutos com 2 Atos distintos.
Arquitetura: 16 Canais, Escala Lá Menor Frígio, BPM 85.
"""

import random
from midiutil import MIDIFile

# ==============================================================================
# CONFIGURAÇÕES GERAIS
# ==============================================================================
BPM = 85
DURACAO_TOTAL_COMPASSOS = 68  # ~8 minutos a 85 BPM (4/4)
ATO1_COMPASSOS = 26           # ~3 minutos
ATO2_COMPASSOS = DURACAO_TOTAL_COMPASSOS - ATO1_COMPASSOS

# Escala Lá Menor Frígio: A, Bb, C, D, E, F, G
# Notas MIDI (Oitava 2 a 4 para base, 4 a 5 para melodia)
ROOT_NOTE = 57  # A3
SCALE_PHRYGIAN = [0, 1, 4, 5, 7, 8, 10]  # Intervalos em semitons relativos à tônica

def get_note_from_scale(degree, octave_offset=0):
    """Retorna a nota MIDI baseada no grau da escala frígia."""
    base = ROOT_NOTE + (octave_offset * 12)
    return base + SCALE_PHRYGIAN[degree % len(SCALE_PHRYGIAN)]

def humanize_time(time, intensity='high'):
    """Aplica micro-atrasos/adiantamentos (Desumanização)."""
    if intensity == 'high':
        # Fita cassete danificada / Músicos exaustos
        return time + random.uniform(-0.05, 0.08)
    elif intensity == 'medium':
        return time + random.uniform(-0.03, 0.05)
    else:
        return time + random.uniform(-0.01, 0.02)

def humanize_velocity(base_vel, intensity='high'):
    """Variação brusca de velocity."""
    if intensity == 'high':
        return int(max(10, min(127, base_vel + random.randint(-40, 40))))
    elif intensity == 'medium':
        return int(max(10, min(127, base_vel + random.randint(-20, 20))))
    else:
        return int(max(10, min(127, base_vel + random.randint(-10, 10))))

# ==============================================================================
# INICIALIZAÇÃO DO MIDI (16 PISTAS)
# ==============================================================================
midi = MIDIFile(16)

# Mapeamento de Canais (0-15)
# 0: Violão, 1: Guitarra L, 2: Guitarra R, 3: Synth Lead, 4: Baixo
# 5: Coro, 6: Pads, 7: Sinos, 8: Harpsichord, 9: Bateria, 10: Tímpanos
# 11: Drones, 12: Trombones, 13-15: FX
channels = list(range(16))
track_names = [
    "Nylon Guitar", "Guitar L", "Guitar R", "Synth Lead", "Bass",
    "Choir", "Pads", "Bells", "Harpsichord", "Drums",
    "Timpani", "Sub Drone", "Brass", "FX1", "FX2", "FX3"
]

for i in range(16):
    midi.addTrackName(i, 0, track_names[i])
    midi.addTempo(i, 0, BPM)
    # Definir instrumentos (Program Change) - GM Standard
    # addProgramChange(track, channel, time, program)
    if i == 0: midi.addProgramChange(i, 0, 0, 25)      # Nylon Guitar
    elif i == 1: midi.addProgramChange(i, 1, 0, 27)    # Clean Guitar (será distorcido no mixer)
    elif i == 2: midi.addProgramChange(i, 2, 0, 27)    # Clean Guitar
    elif i == 3: midi.addProgramChange(i, 3, 0, 81)    # Lead 2 (Sawtooth)
    elif i == 4: midi.addProgramChange(i, 4, 0, 33)    # Bass Electric
    elif i == 5: midi.addProgramChange(i, 5, 0, 52)    # Choir Aahs
    elif i == 6: midi.addProgramChange(i, 6, 0, 90)    # Pad 4 (Choir)
    elif i == 7: midi.addProgramChange(i, 7, 0, 14)    # Tubular Bells
    elif i == 8: midi.addProgramChange(i, 8, 0, 6)     # Harpsichord
    elif i == 9: midi.addProgramChange(i, 9, 0, 0)     # Drum Kit
    elif i == 10: midi.addProgramChange(i, 10, 0, 47)   # Timpani
    elif i == 11: midi.addProgramChange(i, 11, 0, 38)   # Synth Bass 2
    elif i == 12: midi.addProgramChange(i, 12, 0, 58)   # Trombone
    # 13-15 Livres

# Nota: No padrão MIDI, o canal 9 (index 9) é percussivo. 
# A biblioteca midiutil trata o channel 9 como percussivo automaticamente em algumas versões,
# mas vamos garantir que as notas de bateria sejam inseridas corretamente.

# ==============================================================================
# FUNÇÕES DE COMPOSIÇÃO POR ATO
# ==============================================================================

def compose_act_1():
    """
    ATO 1: Dungeon Synth Atmosférico
    Violão (arpejos), Harpsichord (melodia), Pads (drones), Sinos (marcacao).
    """
    print("Compondo Ato 1 (Dungeon Synth)...")
    
    current_bar = 0
    
    # -- PADS (Canal 6) --
    # Acordes menores eternos. Duração de 4 compassos cada bloco.
    pad_chords = [
        (get_note_from_scale(0, 2), get_note_from_scale(2, 3), get_note_from_scale(4, 3)), # Am
        (get_note_from_scale(5, 2), get_note_from_scale(0, 3), get_note_from_scale(2, 3)), # Dm
        (get_note_from_scale(4, 2), get_note_from_scale(0, 3), get_note_from_scale(1, 3)), # Em (Frígio!)
        (get_note_from_scale(3, 2), get_note_from_scale(0, 3), get_note_from_scale(2, 3)), # Dm/A
    ]
    
    for i in range(0, ATO1_COMPASSOS, 4):
        chord_idx = (i // 4) % len(pad_chords)
        notes = pad_chords[chord_idx]
        start_time = i * 4.0  # 4 tempos por compasso
        
        # Humanização leve no início do acorde para não soar robótico demais
        st = humanize_time(start_time, 'low')
        
        for note in notes:
            # Velocity baixa e constante para fundo
            vel = humanize_velocity(60, 'low')
            midi.addNote(6, 6, note, st, 16.0, vel) # Duração de 4 compassos (16 beats)

    # -- VIOLÃO (Canal 0) --
    # Arpejos melancólicos e fora do tempo
    arp_pattern = [0, 4, 7, 4, 0, 3, 7, 3] # Graus da escala (relativo)
    
    for bar in range(ATO1_COMPASSOS):
        # Escolhe um grau base para o arpejo variar
        root_deg = random.choice([0, 3, 4, 5]) 
        
        for step, deg in enumerate(arp_pattern):
            beat_pos = (step * 0.5) # Oitavos
            abs_time = (bar * 4.0) + beat_pos
            
            # Desumanização ALTA no tempo (fita danificada)
            final_time = humanize_time(abs_time, 'high')
            
            note_val = get_note_from_scale((root_deg + deg) % len(SCALE_PHRYGIAN), 3)
            # Velocity variável
            vel = humanize_velocity(random.randint(50, 80), 'medium')
            
            duration = random.uniform(0.8, 1.5) # Duração irregular
            midi.addNote(0, 0, note_val, final_time, duration, vel)

    # -- HARPSICHORD (Canal 8) --
    # Melodia fantasmagórica, espaçada
    melody_notes = [0, 1, 4, 3, 0, 6, 5, 4] # Motivo Frígio
    
    for bar in range(0, ATO1_COMPASSOS, 2):
        # Toca a melodia a cada 2 compassos, lenta
        for i, deg in enumerate(melody_notes):
            beat_pos = i * 1.5 # Notas longas, fora do grid exato
            abs_time = (bar * 4.0) + beat_pos
            
            final_time = humanize_time(abs_time, 'medium')
            note_val = get_note_from_scale(deg, 4) # Oitava mais alta
            vel = humanize_velocity(random.randint(60, 90), 'medium')
            
            midi.addNote(8, 8, note_val, final_time, 2.0, vel)

    # -- SINOS (Canal 7) --
    # Apenas a cada 4 compassos
    for bar in range(0, ATO1_COMPASSOS, 4):
        abs_time = bar * 4.0
        # Atraso proposital do sino, soando tarde
        final_time = humanize_time(abs_time, 'high') 
        
        # Nota tônica ou quinta aguda
        bell_note = get_note_from_scale(0, 5) if (bar % 8 == 0) else get_note_from_scale(4, 5)
        vel = humanize_velocity(100, 'low') # Sino forte mas com variação
        
        midi.addNote(7, 7, bell_note, final_time, 6.0, vel)

def compose_act_2():
    """
    ATO 2: Black Metal Invasion
    Guitarras (Power Chords longos), Baixo, Bateria Tribal, Tímpanos, Trombones, Coro.
    """
    print("Compondo Ato 2 (Black Metal)...")
    
    start_bar = ATO1_COMPASSOS
    
    # -- CORO (Canal 5) --
    # Nota tônica sem parar até o fim
    choir_note = get_note_from_scale(0, 3) # A3
    choir_start = start_bar * 4.0
    choir_duration = (ATO2_COMPASSOS * 4.0)
    
    # O coro entra "acordando", talvez um leve delay ou volume crescente (simulado com vel)
    midi.addNote(5, 5, choir_note, humanize_time(choir_start, 'low'), choir_duration, 90)
    # Adicionar uma segunda voz uma oitava abaixo para engrossar
    midi.addNote(5, 5, get_note_from_scale(0, 2), humanize_time(choir_start, 'low'), choir_duration, 85)


    # -- GUITARRAS (Canais 1 e 2) & BAIXO (Canal 4) --
    # Power Chords longos (1 compasso inteiro = 4 beats)
    # Progressão simples e pesada: I - bII - IV - v (Frígio típico)
    # A5 - Bb5 - D5 - E5
    riff_roots = [0, 1, 3, 4] # Graus
    
    for bar in range(start_bar, DURACAO_TOTAL_COMPASSOS):
        progress_idx = (bar - start_bar) % len(riff_roots)
        root_deg = riff_roots[progress_idx]
        
        root_note = get_note_from_scale(root_deg, 2) # Guitarra grave
        fifth_note = get_note_from_scale((root_deg + 4) % len(SCALE_PHRYGIAN), 2) # Quinta (aproximada na escala)
        # Para power chord real, precisamos da quinta justa. 
        # Na escala frígia de A: A(0)-E(4) é quinta justa. Bb(1)-F(5) é quinta justa.
        # Vamos calcular a quinta justa matematicamente (+7 semitons) para garantir o som "Metal"
        root_midi = get_note_from_scale(root_deg, 2)
        fifth_midi = root_midi + 7 
        
        bass_note = root_midi - 12 # Baixo uma oitava abaixo
        
        start_time = bar * 4.0
        
        # GUITARRA ESQUERDA (Canal 1)
        t1 = humanize_time(start_time, 'medium')
        v1 = humanize_velocity(110, 'medium')
        midi.addNote(1, 1, root_midi, t1, 4.0, v1)
        midi.addNote(1, 1, fifth_midi, t1, 4.0, v1)
        midi.addNote(1, 1, root_midi+12, t1, 4.0, v1) # Oitava
        
        # GUITARRA DIREITA (Canal 2) - Levemente dessincronizada para largura estéreo
        t2 = humanize_time(start_time + 0.05, 'medium') 
        v2 = humanize_velocity(110, 'medium')
        midi.addNote(2, 2, root_midi, t2, 4.0, v2)
        midi.addNote(2, 2, fifth_midi, t2, 4.0, v2)
        midi.addNote(2, 2, root_midi+12, t2, 4.0, v2)
        
        # BAIXO (Canal 4)
        tb = humanize_time(start_time, 'low')
        vb = humanize_velocity(100, 'medium')
        midi.addNote(4, 4, bass_note, tb, 4.0, vb)

    # -- BATERIA (Canal 9) --
    # Ritmo tribal arrastado: Bumbo (36) no 1, Caixa (38) no 3
    # Crash (49) nas viradas ou inícios de seção
    drum_start = start_bar * 4.0
    total_beats = ATO2_COMPASSOS * 4
    
    beat_count = 0
    current_beat_abs = drum_start
    
    while beat_count < total_beats:
        # Compasso de 4/4
        # Tempo 1: Bumbo
        t_kick = humanize_time(current_beat_abs, 'high') # Alta desumanização
        v_kick = humanize_velocity(120, 'high')
        midi.addNote(9, 9, 36, t_kick, 0.5, v_kick)
        
        # Tempo 2: Vazio ou Chimbal leve (opcional, vamos manter vazio para aridez)
        
        # Tempo 3: Caixa Forte
        t_snare = humanize_time(current_beat_abs + 2.0, 'high')
        v_snare = humanize_velocity(125, 'high')
        midi.addNote(9, 9, 38, t_snare, 0.5, v_snare)
        
        # Tempo 4: Vazio
        
        # A cada 4 compassos, um prato (Crash/Ride) para marcar frase
        if (beat_count % 16) == 0:
            t_crash = humanize_time(current_beat_abs, 'high')
            v_crash = humanize_velocity(110, 'high')
            midi.addNote(9, 9, 49, t_crash, 1.0, v_crash)
            
        current_beat_abs += 4.0
        beat_count += 4

    # -- TÍMPANOS (Canal 10) & TROMBONES (Canal 12) --
    # Acompanham a batida da caixa (Tempo 3)
    timpani_note = get_note_from_scale(0, 2) # A2
    brass_root = get_note_from_scale(0, 2)   # A2
    brass_fifth = brass_root + 7
    
    for bar in range(start_bar, DURACAO_TOTAL_COMPASSOS):
        start_time = (bar * 4.0) + 2.0 # No tempo 3 (onde está a caixa)
        
        # Tímpano
        tt = humanize_time(start_time, 'medium')
        vt = humanize_velocity(100, 'medium')
        midi.addNote(10, 10, timpani_note, tt, 1.5, vt)
        
        # Trombone (Acordes curtos e agressivos)
        tb = humanize_time(start_time, 'medium')
        vb = humanize_velocity(110, 'medium')
        midi.addNote(12, 12, brass_root, tb, 1.5, vb)
        midi.addNote(12, 12, brass_fifth, tb, 1.5, vb)

# ==============================================================================
# EXECUÇÃO
# ==============================================================================

if __name__ == "__main__":
    print(f"Iniciando geração de 'Taverna das Sombras' ({DURACAO_TOTAL_COMPASSOS} compassos, {BPM} BPM)...")
    
    compose_act_1()
    compose_act_2()
    
    output_filename = "Taverna_das_Sombras.mid"
    
    with open(output_filename, "wb") as f:
        midi.writeFile(f)
        
    print(f"Sucesso! Arquivo '{output_filename}' gerado na pasta atual.")
    print("Importe no FL Studio e roteie os canais conforme a documentação do projeto.")
