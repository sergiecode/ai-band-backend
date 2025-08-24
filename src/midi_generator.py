"""
Módulo Generador MIDI
Parte del AI Band Backend por Sergie Code

Este módulo maneja la generación MIDI para pistas de bajo y batería usando modelos de IA.
Se integra con Magenta y otros frameworks de IA para generación musical inteligente.
"""

import pretty_midi
from typing import List, Dict, Any
import random


class MidiGenerator:
    """
    Genera pistas MIDI para bajo y batería basándose en progresiones de acordes.
    
    Esta clase proporciona métodos para:
    - Generar líneas de bajo que siguen progresiones de acordes
    - Crear patrones de batería que complementan el estilo musical
    - Usar modelos de IA para generación musical inteligente
    - Exportar archivos MIDI de alta calidad
    """
    
    def __init__(self):
        """Inicializar el generador MIDI con configuraciones por defecto."""
        self.default_tempo = 120
        self.ticks_per_beat = 480
        
        # Mapeos de notas de bajo para acordes comunes
        self.chord_bass_notes = {
            'C': [36, 48],      # C2, C3
            'Am': [33, 45],     # A1, A2  
            'F': [29, 41],      # F1, F2
            'G': [31, 43],      # G1, G2
            'Dm': [38, 50],     # D2, D3
            'Em': [28, 40],     # E1, E2
        }
        
        # Mapeos de notas MIDI estándar de batería
        self.drum_map = {
            'kick': 36,         # Bombo 1
            'snare': 38,        # Caja Acústica
            'hihat_closed': 42, # Hi-Hat Cerrado
            'hihat_open': 46,   # Hi-Hat Abierto
            'crash': 49,        # Platillo Crash 1
            'ride': 51,         # Platillo Ride 1
        }
    
    def generate_bass_track(self, chord_progression: List[Dict[str, Any]], 
                          tempo: int = 120, key: str = "C") -> pretty_midi.PrettyMIDI:
        """
        Generar una pista de bajo que sigue la progresión de acordes.
        
        Args:
            chord_progression: Lista de diccionarios de acordes con timing
            tempo: Tempo en BPM
            key: Tonalidad musical
            
        Returns:
            Objeto PrettyMIDI conteniendo la pista de bajo
        """
        # Crear objeto MIDI
        midi = pretty_midi.PrettyMIDI(initial_tempo=tempo)
        
        # Crear instrumento de bajo (Bajo Eléctrico)
        bass_program = pretty_midi.instrument_name_to_program('Electric Bass (pick)')
        bass = pretty_midi.Instrument(program=bass_program, is_drum=False, name='Bass')
        
        # Generar notas de bajo para cada acorde
        for chord_info in chord_progression:
            # Manejar información de acordes faltante de forma elegante
            chord_name = chord_info.get("chord", "C")  # Por defecto C
            start_time = chord_info.get("start_time", 0.0)
            duration = chord_info.get("duration", 2.0)
            
            # Omitir acordes vacíos o inválidos
            if not chord_name or not isinstance(chord_name, str):
                chord_name = "C"
            
            # Obtener notas de bajo para este acorde
            if chord_name in self.chord_bass_notes:
                bass_notes = self.chord_bass_notes[chord_name]
            else:
                # Por defecto C si no se encuentra el acorde
                bass_notes = self.chord_bass_notes['C']
            
            # Generar patrón de bajo
            self._add_bass_pattern(bass, bass_notes, start_time, duration, tempo)
        
        midi.instruments.append(bass)
        return midi
    
    def _add_bass_pattern(self, instrument: pretty_midi.Instrument, 
                         bass_notes: List[int], start_time: float, 
                         duration: float, tempo: int):
        """Agregar un patrón de bajo para la duración de un acorde."""
        # Patrón de bajo simple: nota fundamental en tiempos 1 y 3
        beat_duration = 60.0 / tempo  # Duración de un tiempo en segundos
        
        # Patrón: Fundamental en tiempo 1, octava o quinta en tiempo 3
        patterns = [
            # Patrón 1: Fundamental - Fundamental - Fundamental - Fundamental (notas enteras)
            [(0, bass_notes[0], beat_duration * 4)],
            
            # Patrón 2: Fundamental - Silencio - Fundamental - Silencio (blancas)
            [(0, bass_notes[0], beat_duration * 2),
             (beat_duration * 2, bass_notes[0], beat_duration * 2)],
            
            # Patrón 3: Fundamental - Quinta - Fundamental - Quinta (negras)
            [(0, bass_notes[0], beat_duration),
             (beat_duration, bass_notes[1], beat_duration),
             (beat_duration * 2, bass_notes[0], beat_duration),
             (beat_duration * 3, bass_notes[1], beat_duration)],
        ]
        
        # Elegir patrón basado en duración
        if duration >= 4.0:
            pattern = patterns[2]  # Más activo para acordes largos
        elif duration >= 2.0:
            pattern = patterns[1]  # Actividad media
        else:
            pattern = patterns[0]  # Simple para acordes cortos
        
        # Agregar notas al instrumento
        for note_start, note_pitch, note_duration in pattern:
            if note_start < duration:  # Asegurar que la nota quepa en la duración del acorde
                actual_duration = min(note_duration, duration - note_start)
                note = pretty_midi.Note(
                    velocity=80,
                    pitch=note_pitch,
                    start=start_time + note_start,
                    end=start_time + note_start + actual_duration
                )
                instrument.notes.append(note)
    
    def generate_drum_track(self, chord_progression: List[Dict[str, Any]], 
                          tempo: int = 120, duration: float = 8.0) -> pretty_midi.PrettyMIDI:
        """
        Generar una pista de batería que complementa la progresión de acordes.
        
        Args:
            chord_progression: Lista de diccionarios de acordes
            tempo: Tempo en BPM
            duration: Duración total en segundos
            
        Returns:
            Objeto PrettyMIDI conteniendo la pista de batería
        """
        # Crear objeto MIDI
        midi = pretty_midi.PrettyMIDI(initial_tempo=tempo)
        
        # Crear instrumento de batería
        drums = pretty_midi.Instrument(program=0, is_drum=True, name='Drums')
        
        # Generar patrón de batería
        self._add_drum_pattern(drums, tempo, duration)
        
        midi.instruments.append(drums)
        return midi
    
    def _add_drum_pattern(self, instrument: pretty_midi.Instrument, 
                         tempo: int, duration: float):
        """Agregar un patrón básico de batería."""
        beat_duration = 60.0 / tempo  # Duración de un tiempo en segundos
        current_time = 0.0
        
        while current_time < duration:
            # Patrón básico 4/4: Bombo en 1,3 - Caja en 2,4 - Hi-hat en 1,2,3,4
            measure_duration = beat_duration * 4
            
            if current_time + measure_duration > duration:
                break
            
            # Bombo en tiempos 1 y 3
            kick_note1 = pretty_midi.Note(
                velocity=100, pitch=self.drum_map['kick'],
                start=current_time, end=current_time + 0.1
            )
            kick_note2 = pretty_midi.Note(
                velocity=90, pitch=self.drum_map['kick'],
                start=current_time + beat_duration * 2, 
                end=current_time + beat_duration * 2 + 0.1
            )
            instrument.notes.extend([kick_note1, kick_note2])
            
            # Caja en tiempos 2 y 4
            snare_note1 = pretty_midi.Note(
                velocity=95, pitch=self.drum_map['snare'],
                start=current_time + beat_duration, 
                end=current_time + beat_duration + 0.1
            )
            snare_note2 = pretty_midi.Note(
                velocity=95, pitch=self.drum_map['snare'],
                start=current_time + beat_duration * 3, 
                end=current_time + beat_duration * 3 + 0.1
            )
            instrument.notes.extend([snare_note1, snare_note2])
            
            # Hi-hat en cada tiempo
            for beat in range(4):
                hihat_note = pretty_midi.Note(
                    velocity=70, pitch=self.drum_map['hihat_closed'],
                    start=current_time + beat * beat_duration,
                    end=current_time + beat * beat_duration + 0.05
                )
                instrument.notes.append(hihat_note)
            
            current_time += measure_duration
    
    def generate_ai_bass_track(self, chord_progression: List[Dict[str, Any]], 
                              tempo: int = 120) -> pretty_midi.PrettyMIDI:
        """
        Generar pista de bajo usando modelos de IA (placeholder para integración con Magenta).
        
        Args:
            chord_progression: Lista de diccionarios de acordes
            tempo: Tempo en BPM
            
        Returns:
            Objeto PrettyMIDI conteniendo pista de bajo generada por IA
            
        Note:
            Este es un placeholder para futura integración con Magenta/IA.
            La implementación actual usa generación basada en reglas con variaciones.
        """
        # TODO: Integrar con MusicVAE de Magenta u otros modelos de IA
        # Por ahora, usar generación basada en reglas mejorada
        
        midi = self.generate_bass_track(chord_progression, tempo)
        
        # Agregar algunas variaciones similares a IA
        bass_instrument = midi.instruments[0]
        self._add_bass_variations(bass_instrument)
        
        return midi
    
    def _add_bass_variations(self, instrument: pretty_midi.Instrument):
        """Agregar variaciones para hacer la línea de bajo más interesante."""
        # Agregar algunas notas de paso y variaciones rítmicas
        for i, note in enumerate(instrument.notes):
            # Ocasionalmente agregar ligeras variaciones de timing
            if random.random() < 0.3:
                note.start += random.uniform(-0.05, 0.05)
                note.end += random.uniform(-0.05, 0.05)
            
            # Ocasionalmente cambiar velocidad para dinámicas
            if random.random() < 0.4:
                note.velocity += random.randint(-20, 20)
                note.velocity = max(30, min(127, note.velocity))
    
    def combine_tracks(self, bass_midi: pretty_midi.PrettyMIDI, 
                      drum_midi: pretty_midi.PrettyMIDI) -> pretty_midi.PrettyMIDI:
        """
        Combinar pistas de bajo y batería en un solo archivo MIDI.
        
        Args:
            bass_midi: MIDI de pista de bajo
            drum_midi: MIDI de pista de batería
            
        Returns:
            Archivo MIDI combinado
        """
        # Crear nuevo objeto MIDI
        combined = pretty_midi.PrettyMIDI(initial_tempo=bass_midi.get_tempo_changes()[1][0])
        
        # Agregar instrumento de bajo
        if bass_midi.instruments:
            combined.instruments.append(bass_midi.instruments[0])
        
        # Agregar instrumento de batería
        if drum_midi.instruments:
            combined.instruments.append(drum_midi.instruments[0])
        
        return combined
