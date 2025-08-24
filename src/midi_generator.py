"""
MIDI Generator Module
Part of AI Band Backend by Sergie Code

This module handles MIDI generation for bass and drum tracks using AI models.
Integrates with Magenta and other AI frameworks for intelligent music generation.
"""

import pretty_midi
from typing import List, Dict, Any
import random


class MidiGenerator:
    """
    Generates MIDI tracks for bass and drums based on chord progressions.
    
    This class provides methods to:
    - Generate bass lines that follow chord progressions
    - Create drum patterns that complement the musical style
    - Use AI models for intelligent music generation
    - Export high-quality MIDI files
    """
    
    def __init__(self):
        """Initialize the MIDI generator with default settings."""
        self.default_tempo = 120
        self.ticks_per_beat = 480
        
        # Bass note mappings for common chords
        self.chord_bass_notes = {
            'C': [36, 48],      # C2, C3
            'Am': [33, 45],     # A1, A2  
            'F': [29, 41],      # F1, F2
            'G': [31, 43],      # G1, G2
            'Dm': [38, 50],     # D2, D3
            'Em': [28, 40],     # E1, E2
        }
        
        # Standard drum kit MIDI note mappings
        self.drum_map = {
            'kick': 36,         # Bass Drum 1
            'snare': 38,        # Acoustic Snare
            'hihat_closed': 42, # Closed Hi-Hat
            'hihat_open': 46,   # Open Hi-Hat
            'crash': 49,        # Crash Cymbal 1
            'ride': 51,         # Ride Cymbal 1
        }
    
    def generate_bass_track(self, chord_progression: List[Dict[str, Any]], 
                          tempo: int = 120, key: str = "C") -> pretty_midi.PrettyMIDI:
        """
        Generate a bass track that follows the chord progression.
        
        Args:
            chord_progression: List of chord dictionaries with timing
            tempo: Tempo in BPM
            key: Musical key
            
        Returns:
            PrettyMIDI object containing the bass track
        """
        # Create MIDI object
        midi = pretty_midi.PrettyMIDI(initial_tempo=tempo)
        
        # Create bass instrument (Electric Bass)
        bass_program = pretty_midi.instrument_name_to_program('Electric Bass (pick)')
        bass = pretty_midi.Instrument(program=bass_program, is_drum=False, name='Bass')
        
        # Generate bass notes for each chord
        for chord_info in chord_progression:
            chord_name = chord_info["chord"]
            start_time = chord_info["start_time"]
            duration = chord_info["duration"]
            
            # Get bass notes for this chord
            if chord_name in self.chord_bass_notes:
                bass_notes = self.chord_bass_notes[chord_name]
            else:
                # Default to C if chord not found
                bass_notes = self.chord_bass_notes['C']
            
            # Generate bass pattern
            self._add_bass_pattern(bass, bass_notes, start_time, duration, tempo)
        
        midi.instruments.append(bass)
        return midi
    
    def _add_bass_pattern(self, instrument: pretty_midi.Instrument, 
                         bass_notes: List[int], start_time: float, 
                         duration: float, tempo: int):
        """Add a bass pattern for a chord duration."""
        # Simple bass pattern: root note on beats 1 and 3
        beat_duration = 60.0 / tempo  # Duration of one beat in seconds
        
        # Pattern: Root on beat 1, octave or fifth on beat 3
        patterns = [
            # Pattern 1: Root - Root - Root - Root (whole notes)
            [(0, bass_notes[0], beat_duration * 4)],
            
            # Pattern 2: Root - Rest - Root - Rest (half notes)
            [(0, bass_notes[0], beat_duration * 2),
             (beat_duration * 2, bass_notes[0], beat_duration * 2)],
            
            # Pattern 3: Root - Fifth - Root - Fifth (quarter notes)
            [(0, bass_notes[0], beat_duration),
             (beat_duration, bass_notes[1], beat_duration),
             (beat_duration * 2, bass_notes[0], beat_duration),
             (beat_duration * 3, bass_notes[1], beat_duration)],
        ]
        
        # Choose pattern based on duration
        if duration >= 4.0:
            pattern = patterns[2]  # More active for longer chords
        elif duration >= 2.0:
            pattern = patterns[1]  # Medium activity
        else:
            pattern = patterns[0]  # Simple for short chords
        
        # Add notes to instrument
        for note_start, note_pitch, note_duration in pattern:
            if note_start < duration:  # Make sure note fits in chord duration
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
        Generate a drum track that complements the chord progression.
        
        Args:
            chord_progression: List of chord dictionaries
            tempo: Tempo in BPM
            duration: Total duration in seconds
            
        Returns:
            PrettyMIDI object containing the drum track
        """
        # Create MIDI object
        midi = pretty_midi.PrettyMIDI(initial_tempo=tempo)
        
        # Create drum instrument
        drums = pretty_midi.Instrument(program=0, is_drum=True, name='Drums')
        
        # Generate drum pattern
        self._add_drum_pattern(drums, tempo, duration)
        
        midi.instruments.append(drums)
        return midi
    
    def _add_drum_pattern(self, instrument: pretty_midi.Instrument, 
                         tempo: int, duration: float):
        """Add a basic drum pattern."""
        beat_duration = 60.0 / tempo  # Duration of one beat in seconds
        current_time = 0.0
        
        while current_time < duration:
            # Basic 4/4 pattern: Kick on 1,3 - Snare on 2,4 - Hi-hat on 1,2,3,4
            measure_duration = beat_duration * 4
            
            if current_time + measure_duration > duration:
                break
            
            # Kick drum on beats 1 and 3
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
            
            # Snare drum on beats 2 and 4
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
            
            # Hi-hat on every beat
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
        Generate bass track using AI models (placeholder for Magenta integration).
        
        Args:
            chord_progression: List of chord dictionaries
            tempo: Tempo in BPM
            
        Returns:
            PrettyMIDI object containing AI-generated bass track
            
        Note:
            This is a placeholder for future Magenta/AI integration.
            Current implementation uses rule-based generation with variations.
        """
        # TODO: Integrate with Magenta's MusicVAE or other AI models
        # For now, use enhanced rule-based generation
        
        midi = self.generate_bass_track(chord_progression, tempo)
        
        # Add some AI-like variations
        bass_instrument = midi.instruments[0]
        self._add_bass_variations(bass_instrument)
        
        return midi
    
    def _add_bass_variations(self, instrument: pretty_midi.Instrument):
        """Add variations to make bass line more interesting."""
        # Add some passing notes and rhythmic variations
        for i, note in enumerate(instrument.notes):
            # Occasionally add slight timing variations
            if random.random() < 0.3:
                note.start += random.uniform(-0.05, 0.05)
                note.end += random.uniform(-0.05, 0.05)
            
            # Occasionally change velocity for dynamics
            if random.random() < 0.4:
                note.velocity += random.randint(-20, 20)
                note.velocity = max(30, min(127, note.velocity))
    
    def combine_tracks(self, bass_midi: pretty_midi.PrettyMIDI, 
                      drum_midi: pretty_midi.PrettyMIDI) -> pretty_midi.PrettyMIDI:
        """
        Combine bass and drum tracks into a single MIDI file.
        
        Args:
            bass_midi: Bass track MIDI
            drum_midi: Drum track MIDI
            
        Returns:
            Combined MIDI file
        """
        # Create new MIDI object
        combined = pretty_midi.PrettyMIDI(initial_tempo=bass_midi.get_tempo_changes()[1][0])
        
        # Add bass instrument
        if bass_midi.instruments:
            combined.instruments.append(bass_midi.instruments[0])
        
        # Add drum instrument
        if drum_midi.instruments:
            combined.instruments.append(drum_midi.instruments[0])
        
        return combined
