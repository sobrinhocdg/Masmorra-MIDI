from midiutil import MIDIFile

# Criar arquivo MIDI com 16 canais (vias)
MyMIDI = MIDIFile(16)

# BPM e configurações
BPM = 130
DURATION_MINUTES = 6
TOTAL_BEATS = DURATION_MINUTES * BPM  # 780 beats

# Escala de Dó Menor (C, D, Eb, F, G, Ab, Bb)
# MIDI notes: C3=48, D3=50, Eb3=51, F3=53, G3=55, Ab3=56, Bb3=58
# Usaremos trítonos e segundas menores para dissonância

# Adicionar tempo a todas as tracks
for track in range(16):
    MyMIDI.addTempo(track, 0, BPM)

# ============================================
# ATO 1: A Vila Podre (0 a 2 min = 0 a 260 beats)
# ============================================

# Violão (Canal 0) - Melodia dissonante e triste
violao_track = 0
cravo_track = 8
pads_track = 6

# Melodia do violão - lenta, dissonante, usando trítonos
violao_melody_ato1 = [
    (48, 2), (51, 2), (48, 2), (54, 2),  # C, Eb, C, F# (trítono)
    (51, 2), (48, 2), (55, 2), (51, 2),  # Eb, C, G, Eb
    (48, 2), (54, 2), (47, 2), (51, 2),  # C, F#, B (segunda menor com C), Eb
    (55, 2), (48, 2), (54, 2), (48, 2),  # G, C, F#, C
]

beat_pos = 0
for note, duration in violao_melody_ato1:
    if beat_pos >= 260:
        break
    MyMIDI.addNote(violao_track, violao_track, note, beat_pos, duration, 80)
    beat_pos += duration

# Cravo (Canal 8) - Contraponto dissonante
cravo_melody_ato1 = [
    (60, 2), (56, 2), (60, 2), (54, 2),  # C4, Ab, C4, F#
    (56, 2), (60, 2), (55, 2), (56, 2),  # Ab, C4, G, Ab
    (60, 2), (54, 2), (59, 2), (56, 2),  # C4, F#, Bb, Ab
    (55, 2), (60, 2), (54, 2), (60, 2),  # G, C4, F#, C4
]

beat_pos = 0
for note, duration in cravo_melody_ato1:
    if beat_pos >= 260:
        break
    MyMIDI.addNote(cravo_track, cravo_track, note, beat_pos, duration, 70)
    beat_pos += duration

# Pads (Canal 6) - Acordes menores sustentados
pad_chords_ato1 = [
    ([48, 51, 55], 8),   # Cm
    ([47, 51, 54], 8),   # Bdim/F# (dissonante)
    ([48, 51, 55], 8),   # Cm
    ([46, 50, 53], 8),   # Bbm
    ([48, 51, 55], 8),   # Cm
    ([47, 51, 54], 8),   # Bdim/F#
    ([48, 51, 55], 8),   # Cm
    ([45, 48, 52], 8),   # Am
]

beat_pos = 0
for chord, duration in pad_chords_ato1:
    if beat_pos >= 260:
        break
    for note in chord:
        MyMIDI.addNote(pads_track, pads_track, note, beat_pos, duration, 60)
    beat_pos += duration

# ============================================
# ATO 2: A Invocação no Chiqueiro (2 a 6 min = 260 a 780 beats)
# ============================================

guitar_l_track = 1
guitar_r_track = 2
bass_track = 4
synth_lead_track = 3
choir_track = 5
bells_track = 7
drums_track = 9
timpani_track = 10
sub_drone_track = 11

# Sub Drone (Canal 11) - Drone contínuo grave
MyMIDI.addNote(sub_drone_track, sub_drone_track, 36, 260, 520, 90)  # C2 drone

# Baixo (Canal 4) - Tremolo picking em colcheias
bass_pattern = [40, 40, 43, 43, 40, 40, 44, 44]  # E, Eb, E, F# (dissonante)
beat_pos = 260
while beat_pos < 780:
    for i, note in enumerate(bass_pattern):
        if beat_pos >= 780:
            break
        MyMIDI.addNote(bass_track, bass_track, note, beat_pos, 0.5, 85)
        beat_pos += 0.5

# Guitarra L (Canal 1) - Tremolo picking
guitar_l_pattern = [52, 52, 55, 55, 52, 52, 56, 56]  # E3, Eb3, E3, F#3
beat_pos = 260
while beat_pos < 780:
    for i, note in enumerate(guitar_l_pattern):
        if beat_pos >= 780:
            break
        MyMIDI.addNote(guitar_l_track, guitar_l_track, note, beat_pos, 0.5, 90)
        beat_pos += 0.5

# Guitarra R (Canal 2) - Harmônicos/trítonos
guitar_r_pattern = [59, 59, 52, 52, 59, 59, 54, 54]  # Bb, E, Bb, F# (trítono)
beat_pos = 260
while beat_pos < 780:
    for i, note in enumerate(guitar_r_pattern):
        if beat_pos >= 780:
            break
        MyMIDI.addNote(guitar_r_track, guitar_r_track, note, beat_pos, 0.5, 90)
        beat_pos += 0.5

# Bateria (Canal 9) - Blast beats
# Bumbo = 36, Caixa = 38
beat_pos = 260
while beat_pos < 780:
    # Blast beat pattern:bumbo-caixa-bumbo-caixa rápido
    MyMIDI.addNote(drums_track, drums_track, 36, beat_pos, 0.25, 100)      # Bumbo
    MyMIDI.addNote(drums_track, drums_track, 38, beat_pos + 0.25, 0.25, 95)  # Caixa
    MyMIDI.addNote(drums_track, drums_track, 36, beat_pos + 0.5, 0.25, 100)  # Bumbo
    MyMIDI.addNote(drums_track, drums_track, 38, beat_pos + 0.75, 0.25, 95)  # Caixa
    beat_pos += 1

# Sintetizador Macabro (Canal 3) - Melodia principal aguda, fria e maligna
synth_melody = [
    (72, 4), (71, 4), (72, 4), (66, 4),   # C5, B, C5, F# (trítono)
    (73, 4), (72, 4), (71, 4), (68, 4),   # Db, C, B, G
    (72, 4), (66, 4), (70, 4), (71, 4),   # C5, F#, B, B
    (67, 4), (72, 4), (66, 4), (72, 4),   # G, C5, F#, C5
    (74, 4), (73, 4), (72, 4), (65, 4),   # D, Db, C, F
    (71, 4), (72, 4), (66, 4), (71, 4),   # B, C5, F#, B
    (72, 4), (66, 4), (70, 4), (66, 4),   # C5, F#, B, F#
    (64, 4), (72, 4), (66, 4), (72, 4),   # E, C5, F#, C5
]

beat_pos = 260
melody_idx = 0
while beat_pos < 780:
    note, duration = synth_melody[melody_idx % len(synth_melody)]
    MyMIDI.addNote(synth_lead_track, synth_lead_track, note, beat_pos, duration, 95)
    beat_pos += duration
    melody_idx += 1

# Coro (Canal 5) - Marca início de compasso (a cada 4 beats)
beat_pos = 260
while beat_pos < 780:
    coro_notes = [55, 58, 62]  # G3, Bb3, D4 (Cm chord)
    for note in coro_notes:
        MyMIDI.addNote(choir_track, choir_track, note, beat_pos, 2, 65)
    beat_pos += 4

# Sinos (Canal 7) - Marca início de compasso
bell_notes = [72, 60, 67, 60]  # C5, C4, G4, C4
beat_pos = 260
bell_idx = 0
while beat_pos < 780:
    MyMIDI.addNote(bells_track, bells_track, bell_notes[bell_idx % 4], beat_pos, 1.5, 75)
    beat_pos += 4
    bell_idx += 1

# Timpani (Canal 10) - Reforça batidas fortes
beat_pos = 260
while beat_pos < 780:
    MyMIDI.addNote(timpani_track, timpani_track, 48, beat_pos, 1, 80)  # C3
    MyMIDI.addNote(timpani_track, timpani_track, 48, beat_pos + 2, 1, 80)
    beat_pos += 4

# Salvar arquivo MIDI
with open("/workspace/blasphemy_village.mid", "wb") as f:
    MyMIDI.writeFile(f)

print("Arquivo MIDI criado: blasphemy_village.mid")
print("Duração: 6 minutos | BPM: 130 | Escala: Dó Menor com dissonâncias")
