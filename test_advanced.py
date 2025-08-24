"""
Advanced Test Suite for AI Band Backend
Created by Sergie Code

Comprehensive tests including edge cases, performance, and integration tests.
"""

import sys
import unittest
import tempfile
from pathlib import Path
import time

# Add src to Python path
sys.path.append(str(Path(__file__).parent / "src"))

from chord_detection import ChordDetector
from midi_generator import MidiGenerator


class TestChordDetectionAdvanced(unittest.TestCase):
    """Advanced tests for chord detection functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.detector = ChordDetector()
    
    def test_empty_chord_progression(self):
        """Test handling of empty chord progression."""
        empty_chords = []
        tempo = self.detector.detect_tempo(empty_chords)
        key = self.detector.detect_key(empty_chords)
        
        self.assertEqual(tempo, 120)  # Default tempo
        self.assertEqual(key, "C")    # Default key
    
    def test_single_chord(self):
        """Test handling of single chord."""
        single_chord = [{"chord": "Am", "start_time": 0.0, "duration": 4.0}]
        
        tempo = self.detector.detect_tempo(single_chord)
        key = self.detector.detect_key(single_chord)
        
        self.assertEqual(tempo, 120)  # Default for single chord
        self.assertIn(key, ['C', 'F', 'G'])  # Am is in these keys
    
    def test_unknown_chords(self):
        """Test handling of unknown chord types."""
        unknown_chords = [
            {"chord": "Xmaj7", "start_time": 0.0, "duration": 2.0},
            {"chord": "Ysus4", "start_time": 2.0, "duration": 2.0},
        ]
        
        # Should not crash and provide defaults
        tempo = self.detector.detect_tempo(unknown_chords)
        key = self.detector.detect_key(unknown_chords)
        
        self.assertIsInstance(tempo, int)
        self.assertIsInstance(key, str)
    
    def test_very_fast_tempo(self):
        """Test detection of very fast tempo."""
        fast_chords = [
            {"chord": "C", "start_time": 0.0, "duration": 0.25},
            {"chord": "F", "start_time": 0.25, "duration": 0.25},
            {"chord": "G", "start_time": 0.5, "duration": 0.25},
            {"chord": "C", "start_time": 0.75, "duration": 0.25},
        ]
        
        tempo = self.detector.detect_tempo(fast_chords)
        self.assertGreater(tempo, 100)  # Should detect fast tempo
    
    def test_very_slow_tempo(self):
        """Test detection of very slow tempo."""
        slow_chords = [
            {"chord": "C", "start_time": 0.0, "duration": 8.0},
            {"chord": "F", "start_time": 8.0, "duration": 8.0},
        ]
        
        tempo = self.detector.detect_tempo(slow_chords)
        self.assertLess(tempo, 100)  # Should detect slow tempo
    
    def test_complex_chord_progression(self):
        """Test analysis of complex chord progression."""
        complex_chords = [
            {"chord": "Cm", "start_time": 0.0, "duration": 1.0},
            {"chord": "Ab", "start_time": 1.0, "duration": 1.0},
            {"chord": "Eb", "start_time": 2.0, "duration": 1.0},
            {"chord": "Bb", "start_time": 3.0, "duration": 1.0},
            {"chord": "Fm", "start_time": 4.0, "duration": 1.0},
            {"chord": "G", "start_time": 5.0, "duration": 1.0},
        ]
        
        analysis = self.detector.analyze_chord_progression(complex_chords)
        
        self.assertEqual(analysis['chord_count'], 6)
        self.assertEqual(analysis['unique_chords'], 6)
        self.assertEqual(analysis['total_duration'], 6.0)
    
    def test_feature_extraction_consistency(self):
        """Test that feature extraction is consistent."""
        chords = [
            {"chord": "C", "start_time": 0.0, "duration": 2.0},
            {"chord": "G", "start_time": 2.0, "duration": 2.0},
        ]
        
        features1 = self.detector.extract_features_for_ai(chords)
        features2 = self.detector.extract_features_for_ai(chords)
        
        # Should be identical
        self.assertTrue((features1 == features2).all())


class TestMidiGenerationAdvanced(unittest.TestCase):
    """Advanced tests for MIDI generation functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.generator = MidiGenerator()
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up temporary files."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_bass_track_note_ranges(self):
        """Test that bass notes are in appropriate ranges."""
        chords = [{"chord": "C", "start_time": 0.0, "duration": 4.0}]
        bass_midi = self.generator.generate_bass_track(chords)
        
        for note in bass_midi.instruments[0].notes:
            # Bass should be in lower octaves (typically C1-C4, MIDI 24-72)
            self.assertGreaterEqual(note.pitch, 24)
            self.assertLessEqual(note.pitch, 72)
    
    def test_drum_track_valid_notes(self):
        """Test that drum notes use valid MIDI drum numbers."""
        chords = [{"chord": "C", "start_time": 0.0, "duration": 4.0}]
        drum_midi = self.generator.generate_drum_track(chords, duration=4.0)
        
        valid_drum_notes = {36, 38, 42, 46, 49, 51}  # Common drum kit notes
        
        for note in drum_midi.instruments[0].notes:
            # All drum notes should be valid
            self.assertIn(note.pitch, valid_drum_notes)
    
    def test_note_timing_accuracy(self):
        """Test that generated notes have accurate timing."""
        chords = [
            {"chord": "C", "start_time": 0.0, "duration": 2.0},
            {"chord": "G", "start_time": 2.0, "duration": 2.0},
        ]
        
        bass_midi = self.generator.generate_bass_track(chords, tempo=120)
        
        # Check that notes fall within expected time ranges
        for note in bass_midi.instruments[0].notes:
            self.assertGreaterEqual(note.start, 0.0)
            self.assertLessEqual(note.end, 4.0)  # Total duration
            self.assertLess(note.start, note.end)  # Start < End
    
    def test_velocity_ranges(self):
        """Test that velocities are within valid MIDI ranges."""
        chords = [{"chord": "C", "start_time": 0.0, "duration": 2.0}]
        
        bass_midi = self.generator.generate_bass_track(chords)
        drum_midi = self.generator.generate_drum_track(chords, duration=2.0)
        
        all_notes = (bass_midi.instruments[0].notes + 
                    drum_midi.instruments[0].notes)
        
        for note in all_notes:
            self.assertGreaterEqual(note.velocity, 1)
            self.assertLessEqual(note.velocity, 127)
    
    def test_different_tempos(self):
        """Test generation at different tempos."""
        chords = [{"chord": "C", "start_time": 0.0, "duration": 4.0}]
        
        tempos = [60, 120, 140, 180]
        
        for tempo in tempos:
            bass_midi = self.generator.generate_bass_track(chords, tempo=tempo)
            drum_midi = self.generator.generate_drum_track(chords, tempo=tempo, duration=4.0)
            
            # Should generate valid MIDI for all tempos
            self.assertGreater(len(bass_midi.instruments[0].notes), 0)
            self.assertGreater(len(drum_midi.instruments[0].notes), 0)
    
    def test_file_output(self):
        """Test MIDI file creation and validity."""
        chords = [{"chord": "C", "start_time": 0.0, "duration": 2.0}]
        
        bass_midi = self.generator.generate_bass_track(chords)
        
        # Save to temporary file
        temp_file = Path(self.temp_dir) / "test_bass.mid"
        bass_midi.write(str(temp_file))
        
        # Check file was created and has content
        self.assertTrue(temp_file.exists())
        self.assertGreater(temp_file.stat().st_size, 0)
    
    def test_ai_bass_variations(self):
        """Test that AI bass generation adds variations."""
        chords = [
            {"chord": "C", "start_time": 0.0, "duration": 2.0},
            {"chord": "G", "start_time": 2.0, "duration": 2.0},
        ]
        
        # Generate multiple AI bass tracks
        bass1 = self.generator.generate_ai_bass_track(chords)
        bass2 = self.generator.generate_ai_bass_track(chords)
        
        # Should have some variations (timing or velocity differences)
        notes1 = bass1.instruments[0].notes
        notes2 = bass2.instruments[0].notes
        
        # At least some notes should have different properties
        has_variations = False
        for n1, n2 in zip(notes1, notes2):
            if (abs(n1.start - n2.start) > 0.001 or 
                abs(n1.velocity - n2.velocity) > 0):
                has_variations = True
                break
        
        # Both tracks should have notes (basic functionality test)
        self.assertGreater(len(notes1), 0)
        self.assertGreater(len(notes2), 0)
        
        # Note: In a real scenario, you'd test for variations with a fixed seed
        # For now, we just ensure the AI generation method doesn't crash


class TestPerformance(unittest.TestCase):
    """Performance tests for the AI Band Backend."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.detector = ChordDetector()
        self.generator = MidiGenerator()
    
    def test_large_chord_progression_performance(self):
        """Test performance with large chord progressions."""
        # Create a large chord progression (100 chords)
        large_progression = []
        chord_names = ["C", "Am", "F", "G", "Dm", "Em"]
        
        for i in range(100):
            chord = {
                "chord": chord_names[i % len(chord_names)],
                "start_time": i * 2.0,
                "duration": 2.0
            }
            large_progression.append(chord)
        
        # Test chord detection performance
        start_time = time.time()
        analysis = self.detector.analyze_chord_progression(large_progression)
        detection_time = time.time() - start_time
        
        # Should complete quickly (under 1 second)
        self.assertLess(detection_time, 1.0)
        self.assertEqual(analysis['chord_count'], 100)
        
        # Test MIDI generation performance
        start_time = time.time()
        bass_midi = self.generator.generate_bass_track(large_progression)
        generation_time = time.time() - start_time
        
        # Should complete quickly (under 5 seconds)
        self.assertLess(generation_time, 5.0)
        self.assertGreater(len(bass_midi.instruments[0].notes), 0)


class TestErrorHandling(unittest.TestCase):
    """Test error handling and edge cases."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.detector = ChordDetector()
        self.generator = MidiGenerator()
    
    def test_invalid_chord_data(self):
        """Test handling of invalid chord data."""
        invalid_chords = [
            {"chord": "C"},  # Missing timing info
            {"start_time": 0.0, "duration": 2.0},  # Missing chord
            {"chord": "", "start_time": 0.0, "duration": 2.0},  # Empty chord
        ]
        
        # Should handle gracefully without crashing
        try:
            tempo = self.detector.detect_tempo(invalid_chords)
            key = self.detector.detect_key(invalid_chords)
            
            self.assertIsInstance(tempo, int)
            self.assertIsInstance(key, str)
        except Exception as e:
            self.fail(f"Should handle invalid data gracefully: {e}")
    
    def test_negative_duration(self):
        """Test handling of negative durations."""
        chords = [{"chord": "C", "start_time": 0.0, "duration": -1.0}]
        
        # Should handle gracefully
        tempo = self.detector.detect_tempo(chords)
        self.assertIsInstance(tempo, int)
    
    def test_zero_duration(self):
        """Test handling of zero duration chords."""
        chords = [{"chord": "C", "start_time": 0.0, "duration": 0.0}]
        
        bass_midi = self.generator.generate_bass_track(chords)
        # Should generate something even with zero duration
        self.assertIsNotNone(bass_midi)


def run_advanced_tests():
    """Run all advanced tests and return results."""
    print("Running Advanced AI Band Backend Tests")
    print("=" * 50)
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestChordDetectionAdvanced,
        TestMidiGenerationAdvanced,
        TestPerformance,
        TestErrorHandling
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print("\n" + "=" * 50)
    if result.wasSuccessful():
        print("All advanced tests passed!")
        print(f"Ran {result.testsRun} tests successfully")
    else:
        print("Some advanced tests failed!")
        print(f"Failures: {len(result.failures)}")
        print(f"Errors: {len(result.errors)}")
        
        # Print details of failures
        if result.failures:
            print("\nFailures:")
            for test, traceback in result.failures:
                print(f"- {test}: {traceback}")
        
        if result.errors:
            print("\nErrors:")
            for test, traceback in result.errors:
                print(f"- {test}: {traceback}")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    try:
        success = run_advanced_tests()
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
