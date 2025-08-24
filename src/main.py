"""
AI Band Backend - Main Entry Point
Created by Sergie Code - AI Tools for Musicians

This is the main entry point for the AI Band Backend that generates
bass and drum tracks from guitar input using AI models.
"""

import sys
from pathlib import Path

# Add src to Python path
sys.path.append(str(Path(__file__).parent))

from chord_detection import ChordDetector
from midi_generator import MidiGenerator


def main():
    """
    Main function that demonstrates the AI Band Backend pipeline:
    1. Detect chords from guitar input (simulated)
    2. Generate bass and drum MIDI tracks
    3. Save output files
    """
    print("AI Band Backend - Generating Music with AI")
    print("=" * 50)
    
    # Initialize components
    chord_detector = ChordDetector()
    midi_generator = MidiGenerator()
    
    # Example chord progression (simulated guitar input)
    print("Analyzing chord progression...")
    sample_chords = [
        {"chord": "C", "start_time": 0.0, "duration": 2.0},
        {"chord": "Am", "start_time": 2.0, "duration": 2.0},
        {"chord": "F", "start_time": 4.0, "duration": 2.0},
        {"chord": "G", "start_time": 6.0, "duration": 2.0},
    ]
    
    # Detect tempo and key information
    tempo = chord_detector.detect_tempo(sample_chords)
    key = chord_detector.detect_key(sample_chords)
    
    print(f"Detected tempo: {tempo} BPM")
    print(f"Detected key: {key}")
    
    # Generate bass track
    print("Generating bass track...")
    bass_midi = midi_generator.generate_bass_track(
        chord_progression=sample_chords,
        tempo=tempo,
        key=key
    )
    
    # Generate drum track
    print("Generating drum track...")
    drum_midi = midi_generator.generate_drum_track(
        chord_progression=sample_chords,
        tempo=tempo,
        duration=8.0  # Total duration in seconds
    )
    
    # Create output directory
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    # Save MIDI files
    bass_file = output_dir / "bass_track.mid"
    drum_file = output_dir / "drum_track.mid"
    
    bass_midi.write(str(bass_file))
    drum_midi.write(str(drum_file))
    
    print(f"Bass track saved: {bass_file}")
    print(f"Drum track saved: {drum_file}")
    print("\nAI Band Backend generation complete!")
    print("Check the 'output' folder for your MIDI files")
    print("Import these files into your DAW to hear the magic!")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure all dependencies are installed:")
        print("pip install -r requirements.txt")
        sys.exit(1)
