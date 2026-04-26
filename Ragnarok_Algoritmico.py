#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
O RAGNAROK ALGORÍTMICO - BRANCH PROFANO
Uma anomalia sonora de 12 minutos possuída pelo espírito do TNBM de 1994.
Geração procedural herética usando matemática avançada para desumanização total.
"""

import math
import random
from midiutil import MIDIFile

# ==============================================================================
# CONFIGURAÇÕES HERÉTICAS
# ==============================================================================
OUTPUT_FILE = "Ragnarok_Algoritmico.mid"
BPM_ACT_1_2 = 135  # Blast Beat frenético
BPM_ACT_3 = 60     # Doom arrastado

# Duração em compassos (4/4)
BARS_ACT_1 = 18
BARS_ACT_2 = 56
BARS_ACT_3 = 60
TOTAL_BARS = BARS_ACT_1 + BARS_ACT_2 + BARS_ACT_3
BEATS_PER_BAR = 4

# Escala Lá Lócrio: A, Bb, C, D, Eb, F, G
SCALE_LOCRIAN = [0, 1, 3, 5, 6, 8, 10]
ROOT_NOTE = 57  # A3

# ==============================================================================
# FUNÇÕES DE CORRUPÇÃO MATEMÁTICA
# ==============================================================================

def hellish_velocity_tremolo(t, intensity=0.6):
    """Gera velocity baseado em onda senoidal + ruído caótico."""
    carrier = math.sin(t * 0.5)
    modulator = math.sin(t * 3.7) * 0.5
    noise = random.uniform(-0.8, 0.8)
    raw_value = (carrier * 0.4) + (modulator * 0.3) + (noise * 0.3)
    base_vel = 90
    variation = int(raw_value * intensity * 30)
    vel = base_vel + variation
    return max(40, min(127, vel))

def chaotic_micro_timing(time_pos, instrument_type="drums"):
    """Aplica micro-timing caótico simulando fita K7 derretendo."""
    if instrument_type == "drums":
        chaos_factor = random.gauss(0, 0.04)
        if random.random() > 0.5:
            chaos_factor -= 0.02
        else:
            chaos_factor += 0.01
        return time_pos + chaos_factor
    elif instrument_type == "guitar":
        return time_pos + random.uniform(-0.03, 0.05)
    elif instrument_type == "doom":
        return time_pos - abs(random.gauss(0, 0.08))
    else:
        return time_pos + random.uniform(-0.02, 0.02)

def get_locrian_note(scale_degree, octave_offset=0):
    """Retorna a nota MIDI baseada no modo Lócrio de Lá."""
    root = ROOT_NOTE + (octave_offset * 12)
    interval = SCALE_LOCRIAN[scale_degree % len(SCALE_LOCRIAN)]
    return root + interval + (12 * (scale_degree // len(SCALE_LOCRIAN)))

# ==============================================================================
# INICIALIZAÇÃO DO ARQUIVO MIDI (16 CANAIS)
# ==============================================================================
midi = MIDIFile(16)

track_names = [
    "Nylon Guitar", "Guitar L (Dist)", "Guitar R (Dist)", "Synth Lead",
    "Bass", "Choir", "Pads", "Bells",
    "Harpsichord", "Drums", "Timpani", "Sub Drone",
    "Brass", "FX 1", "FX 2", "FX 3"
]

for i in range(16):
    midi.addTrackName(i, 0, track_names[i])
    midi.addTempo(i, 0, BPM_ACT_1_2)

# ==============================================================================
# ATO 1: O DESPERTAR PROFANO (0 - 2 min)
# ==============================================================================
print("Forjando Ato 1: O Despertar Profano...")

# Drones Sub-graves (Canal 11)
drone_root = 45  # A2
drone_tritone = 51  # Eb2

for bar in range(BARS_ACT_1):
    start_time = bar * BEATS_PER_BAR
    duration = BEATS_PER_BAR * 2
    note = drone_root if bar % 4 < 2 else drone_tritone
    midi.addNote(11, 0, note, start_time, duration, random.randint(100, 120))

# Synth Lead (Canal 3)
melody_pattern = [0, 3, 4, 2, 1, 5, 0, 6]

for bar in range(BARS_ACT_1):
    for beat in range(BEATS_PER_BAR):
        if random.random() > 0.6:
            start_time = (bar * BEATS_PER_BAR) + beat
            start_time = chaotic_micro_timing(start_time, "doom")
            degree = random.choice(melody_pattern)
            note = get_locrian_note(degree, octave_offset=2)
            dur = BEATS_PER_BAR if random.random() > 0.7 else 2
            vel = hellish_velocity_tremolo(start_time, intensity=0.3)
            midi.addNote(3, 0, note, start_time, dur, vel)

# Pads (Canal 6)
if BARS_ACT_1 > 4:
    pad_start_bar = 4
    for bar in range(pad_start_bar, BARS_ACT_1, 4):
        start_time = bar * BEATS_PER_BAR
        root = get_locrian_note(0, 1)
        third = get_locrian_note(2, 1)
        fifth = get_locrian_note(4, 1)
        for n in [root, third, fifth]:
            midi.addNote(6, 0, n, start_time, BEATS_PER_BAR * 4, 70)

# FX / Ruídos (Canais 13-15)
for bar in range(BARS_ACT_1):
    if random.random() > 0.7:
        t = (bar * BEATS_PER_BAR) + random.uniform(0, 4)
        note = random.randint(80, 100)
        midi.addNote(13, 0, note, t, 0.5, random.randint(30, 60))

# ==============================================================================
# ATO 2: O RITUAL DE SANGUE (2 - 8 min)
# ==============================================================================
print("Invocando Ato 2: O Ritual de Sangue...")

start_bar_act2 = BARS_ACT_1
end_bar_act2 = start_bar_act2 + BARS_ACT_2

# BATERIA (Canal 9) - BLAST BEAT CAÓTICO
for bar in range(start_bar_act2, end_bar_act2):
    bar_start_time = bar * BEATS_PER_BAR
    notes_in_bar = 16
    step_duration = BEATS_PER_BAR / notes_in_bar
    
    for i in range(notes_in_bar):
        theoretical_time = bar_start_time + (i * step_duration)
        actual_time = chaotic_micro_timing(theoretical_time, "drums")
        
        if i % 2 == 0:
            vel_kick = hellish_velocity_tremolo(actual_time, intensity=0.8)
            vel_cymbal = hellish_velocity_tremolo(actual_time + 0.1, intensity=0.6)
            midi.addNote(9, 0, 36, actual_time, 0.2, vel_kick)
            midi.addNote(9, 0, 49, actual_time, 0.5, vel_cymbal)
        else:
            vel_snare = hellish_velocity_tremolo(actual_time, intensity=0.9)
            midi.addNote(9, 0, 38, actual_time, 0.2, vel_snare)

# GUITARRAS (Canais 1 e 2) - TREMOLO PICKING DISSONANTE
guitar_chords = [
    (get_locrian_note(0, 2), get_locrian_note(4, 2)),
    (get_locrian_note(1, 2), get_locrian_note(5, 2)),
    (get_locrian_note(3, 2), get_locrian_note(0, 3)),
    (get_locrian_note(4, 2), get_locrian_note(1, 3)),
]

chord_change_interval = 4

for bar in range(start_bar_act2, end_bar_act2):
    chord_idx = ((bar - start_bar_act2) // chord_change_interval) % len(guitar_chords)
    root, tritone = guitar_chords[chord_idx]
    bar_start_time = bar * BEATS_PER_BAR
    
    picking_speed = 4
    total_picks = BEATS_PER_BAR * picking_speed
    pick_duration = 1.0 / picking_speed
    
    for p in range(total_picks):
        t_theoretical = bar_start_time + (p * pick_duration)
        t_actual = chaotic_micro_timing(t_theoretical, "guitar")
        vel = hellish_velocity_tremolo(t_actual, intensity=0.7)
        dur = pick_duration * 0.8
        offset_r = random.uniform(0.01, 0.03)
        
        midi.addNote(1, 0, root, t_actual, dur, vel)
        midi.addNote(1, 0, tritone, t_actual, dur, int(vel * 0.9))
        midi.addNote(2, 0, root, t_actual + offset_r, dur, int(vel * 0.95))
        midi.addNote(2, 0, tritone, t_actual + offset_r, dur, int(vel * 0.85))

# BAIXO (Canal 4)
for bar in range(start_bar_act2, end_bar_act2):
    chord_idx = ((bar - start_bar_act2) // chord_change_interval) % len(guitar_chords)
    root, _ = guitar_chords[chord_idx]
    bass_note = root - 12
    start_time = bar * BEATS_PER_BAR
    vel = random.randint(90, 115)
    midi.addNote(4, 0, bass_note, start_time, BEATS_PER_BAR, vel)

# CORO (Canal 5) - Lamentos contínuos
choir_start_bar = start_bar_act2
for bar in range(choir_start_bar, TOTAL_BARS, 2):
    t = bar * BEATS_PER_BAR
    dur = BEATS_PER_BAR * 2
    notes_choir = [get_locrian_note(0, 1), get_locrian_note(4, 1), get_locrian_note(0, 2)]
    for n in notes_choir:
        v = 80 + random.randint(-10, 10)
        midi.addNote(5, 0, n, t, dur, v)

# PADS (Canal 6) - Reforço
for bar in range(start_bar_act2, end_bar_act2, 2):
    t = bar * BEATS_PER_BAR
    dur = BEATS_PER_BAR * 2
    root = get_locrian_note((bar // 2) % 4, 2)
    third = get_locrian_note(2, 2)
    fifth = get_locrian_note(4, 2)
    for n in [root, third, fifth]:
        midi.addNote(6, 0, n, t, dur, 65)

# TÍMPANOS (Canal 10) e METAIS (Canal 12)
for bar in range(start_bar_act2, end_bar_act2):
    bar_start = bar * BEATS_PER_BAR
    timp_note = get_locrian_note(0, 0)
    midi.addNote(10, 0, timp_note, bar_start, 1.5, 100)
    if bar % 2 == 0:
        brass_root = get_locrian_note(0, 1)
        brass_tri = get_locrian_note(4, 1)
        midi.addNote(12, 0, brass_root, bar_start, 0.5, 95)
        midi.addNote(12, 0, brass_tri, bar_start, 0.5, 90)

# ==============================================================================
# ATO 3: A MORTE DA FITA (8 - 12 min)
# ==============================================================================
print("Executando Ato 3: A Morte da Fita...")

start_bar_act3 = end_bar_act2
total_bars_final = start_bar_act3 + BARS_ACT_3

# Mudança de BPM para 60
act3_start_beat = start_bar_act3 * BEATS_PER_BAR
midi.addTempo(0, act3_start_beat, BPM_ACT_3)

# VIOLÃO DE NYLON (Canal 0) - Arpejos desmoronando
arp_pattern = [0, 4, 2, 0, 3, 1]

for bar in range(start_bar_act3, total_bars_final):
    progress = (bar - start_bar_act3) / BARS_ACT_3
    density = 1.0 - (progress ** 2)
    
    if random.random() > density:
        continue
    
    bar_start = bar * BEATS_PER_BAR
    num_notes = max(1, int(random.randint(1, 4) * density))
    
    for i in range(num_notes):
        degree = random.choice(arp_pattern)
        note = get_locrian_note(degree, octave_offset=2)
        delay = random.uniform(0.2, 1.5) * (1 + progress)
        t_play = bar_start + (i * 1.5) + delay
        dur = random.uniform(2.0, 5.0)
        vel = max(20, int(80 * (1 - progress) * random.uniform(0.5, 1.0)))
        midi.addNote(0, 0, note, t_play, dur, vel)

# SINOS GÉLIDOS (Canal 7)
for bar in range(start_bar_act3, total_bars_final):
    if random.random() > 0.7:
        bar_start = bar * BEATS_PER_BAR
        t = bar_start + random.uniform(0, 4)
        note = get_locrian_note(random.randint(0, 6), octave_offset=3)
        dur = random.uniform(4.0, 8.0)
        vel = random.randint(40, 70)
        midi.addNote(7, 0, note, t, dur, vel)

# DRONES (Canal 11) - Fade out
for bar in range(start_bar_act3, total_bars_final, 4):
    t = bar * BEATS_PER_BAR
    dur = BEATS_PER_BAR * 4
    progress = (bar - start_bar_act3) / BARS_ACT_3
    octave = 0 if progress < 0.5 else -1
    note = get_locrian_note(0, octave)
    vel = max(10, int(100 * (1 - progress)))
    if vel > 10:
        midi.addNote(11, 0, note, t, dur, vel)

# CORO FINAL (Canal 5)
final_chord_time = (total_bars_final - 4) * BEATS_PER_BAR
final_notes = [get_locrian_note(0, 1), get_locrian_note(0, 2)]
for n in final_notes:
    midi.addNote(5, 0, n, final_chord_time, BEATS_PER_BAR * 4, 60)

# HARPSICHORD FANTASMA (Canal 8)
if BARS_ACT_3 > 10:
    ghost_bar = total_bars_final - 5
    t = ghost_bar * BEATS_PER_BAR
    note = get_locrian_note(4, 2)
    midi.addNote(8, 0, note, t, BEATS_PER_BAR * 4, 50)

# ==============================================================================
# GRAVAÇÃO
# ==============================================================================
print(f"Composição profana finalizada. Estrutura: {TOTAL_BARS} compassos.")
print(f"Ato 1: Bars 0-{BARS_ACT_1} (135 BPM)")
print(f"Ato 2: Bars {BARS_ACT_1}-{end_bar_act2} (135 BPM)")
print(f"Ato 3: Bars {end_bar_act2}-{total_bars_final} (60 BPM - Doom)")
print("Gravando arquivo MIDI...")

with open(OUTPUT_FILE, 'wb') as f:
    midi.writeFile(f)

print(f"SUCESSO: '{OUTPUT_FILE}' gerado no diretório atual.")
print("Importe no FL Studio. Ajuste os VSTs nos canais 0-15 conforme o mapa.")
