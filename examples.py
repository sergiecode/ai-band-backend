"""
Example Usage of AI Band Backend
Created by Sergie Code

This script demonstrates various ways to use the AI Band Backend
for generating bass and drum tracks from chord progressions.
"""

import sys
from pathlib import Path

# Add src to Python path
sys.path.append(str(Path(__file__).parent / "src"))

from chord_detection import ChordDetector
from midi_generator import MidiGenerator


def example_basic_generation():
    """Example 1: Basic chord progression generation."""
    print("\nExample 1: Basic Generation")
    print("-" * 40)
    
    # Initialize components
    detector = ChordDetector()
    generator = MidiGenerator()
    
    # Define a simple chord progression
    chords = [
        {"chord": "C", "start_time": 0.0, "duration": 2.0},
        {"chord": "Am", "start_time": 2.0, "duration": 2.0},
        {"chord": "F", "start_time": 4.0, "duration": 2.0},
        {"chord": "G", "start_time": 6.0, "duration": 2.0},
    ]
    
    # Analyze the progression
    analysis = detector.analyze_chord_progression(chords)
    print(f"Analysis: {analysis}")
    
    # Generate tracks
    bass_midi = generator.generate_bass_track(chords, tempo=analysis["tempo"])
    drum_midi = generator.generate_drum_track(chords, tempo=analysis["tempo"])
    
    # Save files
    output_dir = Path("examples_output")
    output_dir.mkdir(exist_ok=True)
    
    bass_file = output_dir / "example1_bass.mid"
    drum_file = output_dir / "example1_drums.mid"
    
    bass_midi.write(str(bass_file))
    drum_midi.write(str(drum_file))
    
    print(f"Files saved: {bass_file}, {drum_file}")


def example_different_styles():
    """Example 2: Different musical styles and tempos."""
    print("\nExample 2: Different Styles")
    print("-" * 40)
    
    generator = MidiGenerator()
    
    # Style 1: Slow ballad
    ballad_chords = [
        {"chord": "C", "start_time": 0.0, "duration": 4.0},
        {"chord": "Am", "start_time": 4.0, "duration": 4.0},
        {"chord": "F", "start_time": 8.0, "duration": 4.0},
        {"chord": "G", "start_time": 12.0, "duration": 4.0},
    ]
    
    bass_ballad = generator.generate_bass_track(ballad_chords, tempo=70)
    
    # Style 2: Fast rock
    rock_chords = [
        {"chord": "Em", "start_time": 0.0, "duration": 1.0},
        {"chord": "C", "start_time": 1.0, "duration": 1.0},
        {"chord": "G", "start_time": 2.0, "duration": 1.0},
        {"chord": "D", "start_time": 3.0, "duration": 1.0},
    ]
    
    bass_rock = generator.generate_bass_track(rock_chords, tempo=140)
    drum_rock = generator.generate_drum_track(rock_chords, tempo=140, duration=4.0)
    
    # Save files
    output_dir = Path("examples_output")
    output_dir.mkdir(exist_ok=True)
    
    bass_ballad.write(str(output_dir / "example2_ballad_bass.mid"))
    bass_rock.write(str(output_dir / "example2_rock_bass.mid"))
    drum_rock.write(str(output_dir / "example2_rock_drums.mid"))
    
    print("Different style examples saved")


def example_combined_track():
    """Example 3: Combining bass and drums into one file."""
    print("\nExample 3: Combined Track")
    print("-" * 40)
    
    generator = MidiGenerator()
    
    # Create a progression
    chords = [
        {"chord": "Am", "start_time": 0.0, "duration": 2.0},
        {"chord": "F", "start_time": 2.0, "duration": 2.0},
        {"chord": "C", "start_time": 4.0, "duration": 2.0},
        {"chord": "G", "start_time": 6.0, "duration": 2.0},
    ]
    
    # Generate individual tracks
    bass_midi = generator.generate_bass_track(chords, tempo=100)
    drum_midi = generator.generate_drum_track(chords, tempo=100, duration=8.0)
    
    # Combine tracks
    combined_midi = generator.combine_tracks(bass_midi, drum_midi)
    
    # Save combined file
    output_dir = Path("examples_output")
    output_dir.mkdir(exist_ok=True)
    
    combined_file = output_dir / "example3_combined.mid"
    combined_midi.write(str(combined_file))
    
    print(f"Combined track saved: {combined_file}")


def example_ai_features():
    """Example 4: AI feature extraction for future model training."""
    print("\nExample 4: AI Features")
    print("-" * 40)
    
    detector = ChordDetector()
    
    # Complex chord progression
    chords = [
        {"chord": "Dm", "start_time": 0.0, "duration": 1.5},
        {"chord": "G", "start_time": 1.5, "duration": 1.5},
        {"chord": "C", "start_time": 3.0, "duration": 1.0},
        {"chord": "Am", "start_time": 4.0, "duration": 2.0},
        {"chord": "F", "start_time": 6.0, "duration": 1.0},
        {"chord": "G", "start_time": 7.0, "duration": 1.0},
    ]
    
    # Extract features for AI
    features = detector.extract_features_for_ai(chords)
    analysis = detector.analyze_chord_progression(chords)
    
    print(f"AI Features: {features}")
    print(f"Musical Analysis: {analysis}")
    
    # Generate with AI-enhanced method (placeholder)
    generator = MidiGenerator()
    ai_bass = generator.generate_ai_bass_track(chords, tempo=analysis["tempo"])
    
    # Save AI-generated track
    output_dir = Path("examples_output")
    output_dir.mkdir(exist_ok=True)
    
    ai_file = output_dir / "example4_ai_bass.mid"
    ai_bass.write(str(ai_file))
    
    print(f"AI-enhanced bass saved: {ai_file}")


def main():
    """Run all examples."""
    print("AI Band Backend - Examples")
    print("=" * 50)
    print("Created by Sergie Code")
    print("These examples show different ways to use the AI Band Backend")
    
    try:
        example_basic_generation()
        example_different_styles()
        example_combined_track()
        example_ai_features()
        
        print("\nAll examples completed successfully!")
        print("Check the 'examples_output' folder for generated MIDI files")
        print("Import these files into your DAW to hear the results!")
        
    except Exception as e:
        print(f"\nError running examples: {e}")
        print("Make sure you've installed all dependencies:")
        print("pip install -r requirements.txt")


if __name__ == "__main__":
    main()
