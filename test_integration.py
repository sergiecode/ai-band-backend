"""
Integration Test Suite for AI Band Backend
Created by Sergie Code

Tests the complete workflow from chord input to MIDI output,
including real file generation and validation.
"""

import sys
import unittest
import tempfile
import shutil
from pathlib import Path

# Add src to Python path
sys.path.append(str(Path(__file__).parent / "src"))

from chord_detection import ChordDetector
from midi_generator import MidiGenerator
import pretty_midi


class TestCompleteWorkflow(unittest.TestCase):
    """Test the complete AI Band Backend workflow."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.detector = ChordDetector()
        self.generator = MidiGenerator()
        
        # Sample chord progressions for testing
        self.pop_progression = [
            {"chord": "C", "start_time": 0.0, "duration": 2.0},
            {"chord": "Am", "start_time": 2.0, "duration": 2.0},
            {"chord": "F", "start_time": 4.0, "duration": 2.0},
            {"chord": "G", "start_time": 6.0, "duration": 2.0},
        ]
        
        self.jazz_progression = [
            {"chord": "Dm", "start_time": 0.0, "duration": 2.0},
            {"chord": "G", "start_time": 2.0, "duration": 2.0},
            {"chord": "C", "start_time": 4.0, "duration": 2.0},
            {"chord": "Am", "start_time": 6.0, "duration": 2.0},
        ]
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_complete_pop_song_generation(self):
        """Test complete pop song generation workflow."""
        # Step 1: Analyze chord progression
        analysis = self.detector.analyze_chord_progression(self.pop_progression)
        
        self.assertEqual(analysis['key'], 'C')
        self.assertEqual(analysis['chord_count'], 4)
        self.assertEqual(analysis['total_duration'], 8.0)
        
        # Step 2: Generate bass track
        bass_midi = self.generator.generate_bass_track(
            self.pop_progression, 
            tempo=analysis['tempo'], 
            key=analysis['key']
        )
        
        # Step 3: Generate drum track
        drum_midi = self.generator.generate_drum_track(
            self.pop_progression,
            tempo=analysis['tempo'],
            duration=analysis['total_duration']
        )
        
        # Step 4: Validate generated tracks
        self.assertIsNotNone(bass_midi)
        self.assertIsNotNone(drum_midi)
        self.assertEqual(len(bass_midi.instruments), 1)
        self.assertEqual(len(drum_midi.instruments), 1)
        
        # Step 5: Save files and validate
        bass_file = self.temp_dir / "pop_bass.mid"
        drum_file = self.temp_dir / "pop_drums.mid"
        
        bass_midi.write(str(bass_file))
        drum_midi.write(str(drum_file))
        
        self.assertTrue(bass_file.exists())
        self.assertTrue(drum_file.exists())
        self.assertGreater(bass_file.stat().st_size, 0)
        self.assertGreater(drum_file.stat().st_size, 0)
        
        # Step 6: Validate MIDI file integrity
        loaded_bass = pretty_midi.PrettyMIDI(str(bass_file))
        loaded_drums = pretty_midi.PrettyMIDI(str(drum_file))
        
        self.assertGreater(len(loaded_bass.instruments[0].notes), 0)
        self.assertGreater(len(loaded_drums.instruments[0].notes), 0)
    
    def test_different_musical_styles(self):
        """Test generation of different musical styles."""
        styles = [
            ("Pop", self.pop_progression, 120),
            ("Jazz", self.jazz_progression, 140),
        ]
        
        for style_name, progression, tempo in styles:
            with self.subTest(style=style_name):
                # Generate tracks
                bass_midi = self.generator.generate_bass_track(progression, tempo=tempo)
                drum_midi = self.generator.generate_drum_track(progression, tempo=tempo, duration=8.0)
                
                # Combine tracks
                combined_midi = self.generator.combine_tracks(bass_midi, drum_midi)
                
                # Validate combined track
                self.assertEqual(len(combined_midi.instruments), 2)
                
                # Check that we have both bass and drums
                has_bass = any(not inst.is_drum for inst in combined_midi.instruments)
                has_drums = any(inst.is_drum for inst in combined_midi.instruments)
                
                self.assertTrue(has_bass, f"{style_name} should have bass")
                self.assertTrue(has_drums, f"{style_name} should have drums")
                
                # Save and validate file
                style_file = self.temp_dir / f"{style_name.lower()}_combined.mid"
                combined_midi.write(str(style_file))
                
                self.assertTrue(style_file.exists())
                self.assertGreater(style_file.stat().st_size, 0)
    
    def test_ai_enhanced_generation(self):
        """Test AI-enhanced generation features."""
        # Test AI bass generation
        ai_bass = self.generator.generate_ai_bass_track(self.pop_progression, tempo=120)
        
        self.assertIsNotNone(ai_bass)
        self.assertEqual(len(ai_bass.instruments), 1)
        self.assertGreater(len(ai_bass.instruments[0].notes), 0)
        
        # Compare with regular bass generation
        regular_bass = self.generator.generate_bass_track(self.pop_progression, tempo=120)
        
        # Both should have the same structure
        self.assertEqual(len(ai_bass.instruments), len(regular_bass.instruments))
        
        # Save AI-generated track
        ai_file = self.temp_dir / "ai_bass.mid"
        ai_bass.write(str(ai_file))
        
        self.assertTrue(ai_file.exists())
        self.assertGreater(ai_file.stat().st_size, 0)
    
    def test_error_recovery_workflow(self):
        """Test that the workflow can handle and recover from errors."""
        # Test with invalid/incomplete chord data
        problematic_chords = [
            {"chord": "C", "start_time": 0.0, "duration": 2.0},
            {"chord": "", "start_time": 2.0, "duration": 2.0},  # Empty chord
            {"start_time": 4.0, "duration": 2.0},  # Missing chord
            {"chord": "UnknownChord", "start_time": 6.0, "duration": 2.0},  # Unknown chord
        ]
        
        # Analysis should still work
        analysis = self.detector.analyze_chord_progression(problematic_chords)
        
        self.assertIsInstance(analysis['tempo'], int)
        self.assertIsInstance(analysis['key'], str)
        self.assertEqual(analysis['chord_count'], 4)  # Still counts all entries
        
        # Generation should still work
        bass_midi = self.generator.generate_bass_track(problematic_chords)
        drum_midi = self.generator.generate_drum_track(problematic_chords, duration=8.0)
        
        self.assertIsNotNone(bass_midi)
        self.assertIsNotNone(drum_midi)
        
        # Should be able to save files
        bass_file = self.temp_dir / "error_recovery_bass.mid"
        drum_file = self.temp_dir / "error_recovery_drums.mid"
        
        bass_midi.write(str(bass_file))
        drum_midi.write(str(drum_file))
        
        self.assertTrue(bass_file.exists())
        self.assertTrue(drum_file.exists())
    
    def test_performance_with_long_progression(self):
        """Test performance with long chord progressions."""
        # Create a long progression (32 chords, typical song length)
        long_progression = []
        chord_names = ["C", "Am", "F", "G", "Dm", "Em"]
        
        for i in range(32):
            chord = {
                "chord": chord_names[i % len(chord_names)],
                "start_time": i * 2.0,
                "duration": 2.0
            }
            long_progression.append(chord)
        
        # Should handle long progressions efficiently
        import time
        
        start_time = time.time()
        analysis = self.detector.analyze_chord_progression(long_progression)
        analysis_time = time.time() - start_time
        
        start_time = time.time()
        bass_midi = self.generator.generate_bass_track(long_progression)
        bass_generation_time = time.time() - start_time
        
        start_time = time.time()
        drum_midi = self.generator.generate_drum_track(long_progression, duration=64.0)
        drum_generation_time = time.time() - start_time
        
        # Performance expectations (should be fast)
        self.assertLess(analysis_time, 0.1)  # Analysis under 100ms
        self.assertLess(bass_generation_time, 1.0)  # Bass generation under 1s
        self.assertLess(drum_generation_time, 1.0)  # Drum generation under 1s
        
        # Validate results
        self.assertEqual(analysis['chord_count'], 32)
        self.assertEqual(analysis['total_duration'], 64.0)
        self.assertGreater(len(bass_midi.instruments[0].notes), 0)
        self.assertGreater(len(drum_midi.instruments[0].notes), 0)


def run_integration_tests():
    """Run all integration tests and return results."""
    print("Running AI Band Backend Integration Tests")
    print("=" * 55)
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add integration tests
    tests = unittest.TestLoader().loadTestsFromTestCase(TestCompleteWorkflow)
    test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print("\n" + "=" * 55)
    if result.wasSuccessful():
        print("All integration tests passed!")
        print(f"Ran {result.testsRun} integration tests successfully")
        print("The AI Band Backend is working perfectly!")
    else:
        print("Some integration tests failed!")
        print(f"Failures: {len(result.failures)}")
        print(f"Errors: {len(result.errors)}")
        
        # Print details of failures
        if result.failures:
            print("\nFailures:")
            for test, traceback in result.failures:
                print(f"- {test}")
                print(f"  {traceback}")
        
        if result.errors:
            print("\nErrors:")
            for test, traceback in result.errors:
                print(f"- {test}")
                print(f"  {traceback}")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    try:
        success = run_integration_tests()
        if not success:
            sys.exit(1)
    except ImportError as e:
        print(f"Import error: {e}")
        print("Make sure all dependencies are installed:")
        print("pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"Test error: {e}")
        sys.exit(1)
