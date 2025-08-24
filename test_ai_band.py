"""
Suite de Pruebas para AI Band Backend
Creado por Sergie Code

Pruebas básicas para asegurar que la funcionalidad principal funciona correctamente.
"""

import sys
import unittest
from pathlib import Path

# Add src to Python path
sys.path.append(str(Path(__file__).parent / "src"))

from chord_detection import ChordDetector
from midi_generator import MidiGenerator


class TestChordDetection(unittest.TestCase):
    """Probar funcionalidad de detección de acordes."""
    
    def setUp(self):
        """Configurar fixtures de prueba."""
        self.detector = ChordDetector()
        self.sample_chords = [
            {"chord": "C", "start_time": 0.0, "duration": 2.0},
            {"chord": "Am", "start_time": 2.0, "duration": 2.0},
            {"chord": "F", "start_time": 4.0, "duration": 2.0},
            {"chord": "G", "start_time": 6.0, "duration": 2.0},
        ]
    
    def test_tempo_detection(self):
        """Probar detección de tempo desde progresión de acordes."""
        tempo = self.detector.detect_tempo(self.sample_chords)
        self.assertIsInstance(tempo, int)
        self.assertGreater(tempo, 0)
        self.assertLess(tempo, 200)
    
    def test_key_detection(self):
        """Probar detección de tonalidad desde progresión de acordes."""
        key = self.detector.detect_key(self.sample_chords)
        self.assertIsInstance(key, str)
        self.assertIn(key, ['C', 'F', 'G', 'Am', 'Dm', 'Em'])
    
    def test_chord_analysis(self):
        """Probar análisis comprensivo de progresión de acordes."""
        analysis = self.detector.analyze_chord_progression(self.sample_chords)
        
        required_keys = ['tempo', 'key', 'total_duration', 'chord_count']
        for key in required_keys:
            self.assertIn(key, analysis)
        
        self.assertEqual(analysis['chord_count'], 4)
        self.assertEqual(analysis['total_duration'], 8.0)
    
    def test_feature_extraction(self):
        """Probar extracción de características de IA."""
        features = self.detector.extract_features_for_ai(self.sample_chords)
        self.assertIsNotNone(features)
        self.assertGreater(len(features), 0)


class TestMidiGeneration(unittest.TestCase):
    """Probar funcionalidad de generación MIDI."""
    
    def setUp(self):
        """Configurar fixtures de prueba."""
        self.generator = MidiGenerator()
        self.sample_chords = [
            {"chord": "C", "start_time": 0.0, "duration": 2.0},
            {"chord": "Am", "start_time": 2.0, "duration": 2.0},
        ]
    
    def test_bass_generation(self):
        """Probar generación de pista de bajo."""
        bass_midi = self.generator.generate_bass_track(
            self.sample_chords, tempo=120
        )
        
        self.assertIsNotNone(bass_midi)
        self.assertGreater(len(bass_midi.instruments), 0)
        
        bass_instrument = bass_midi.instruments[0]
        self.assertFalse(bass_instrument.is_drum)
        self.assertGreater(len(bass_instrument.notes), 0)
    
    def test_drum_generation(self):
        """Probar generación de pista de batería."""
        drum_midi = self.generator.generate_drum_track(
            self.sample_chords, tempo=120, duration=4.0
        )
        
        self.assertIsNotNone(drum_midi)
        self.assertGreater(len(drum_midi.instruments), 0)
        
        drum_instrument = drum_midi.instruments[0]
        self.assertTrue(drum_instrument.is_drum)
        self.assertGreater(len(drum_instrument.notes), 0)
    
    def test_track_combination(self):
        """Probar combinación de pistas de bajo y batería."""
        bass_midi = self.generator.generate_bass_track(self.sample_chords)
        drum_midi = self.generator.generate_drum_track(self.sample_chords, duration=4.0)
        
        combined_midi = self.generator.combine_tracks(bass_midi, drum_midi)
        
        self.assertIsNotNone(combined_midi)
        self.assertEqual(len(combined_midi.instruments), 2)
        
        # Verificar que tenemos tanto bajo como batería
        has_bass = any(not inst.is_drum for inst in combined_midi.instruments)
        has_drums = any(inst.is_drum for inst in combined_midi.instruments)
        
        self.assertTrue(has_bass)
        self.assertTrue(has_drums)


class TestIntegration(unittest.TestCase):
    """Probar integración entre componentes."""
    
    def setUp(self):
        """Configurar fixtures de prueba."""
        self.detector = ChordDetector()
        self.generator = MidiGenerator()
    
    def test_full_pipeline(self):
        """Probar el pipeline completo de generación."""
        # Progresión de acordes de entrada
        chords = [
            {"chord": "C", "start_time": 0.0, "duration": 2.0},
            {"chord": "G", "start_time": 2.0, "duration": 2.0},
        ]
        
        # Analizar acordes
        tempo = self.detector.detect_tempo(chords)
        key = self.detector.detect_key(chords)
        
        # Generar pistas
        bass_midi = self.generator.generate_bass_track(chords, tempo=tempo, key=key)
        drum_midi = self.generator.generate_drum_track(chords, tempo=tempo, duration=4.0)
        
        # Verificar resultados
        self.assertIsNotNone(bass_midi)
        self.assertIsNotNone(drum_midi)
        self.assertGreater(len(bass_midi.instruments[0].notes), 0)
        self.assertGreater(len(drum_midi.instruments[0].notes), 0)


def run_tests():
    """Ejecutar todas las pruebas y devolver resultados."""
    print("🧪 Ejecutando Pruebas del AI Band Backend")
    print("=" * 40)
    
    # Crear suite de pruebas
    test_suite = unittest.TestSuite()
    
    # Agregar clases de prueba
    test_classes = [TestChordDetection, TestMidiGeneration, TestIntegration]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Ejecutar pruebas
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Imprimir resumen
    print("\n" + "=" * 40)
    if result.wasSuccessful():
        print("✅ ¡Todas las pruebas pasaron!")
        print(f"📊 Ejecutó {result.testsRun} pruebas exitosamente")
    else:
        print("❌ ¡Algunas pruebas fallaron!")
        print(f"💥 Fallas: {len(result.failures)}")
        print(f"🚨 Errores: {len(result.errors)}")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    try:
        success = run_tests()
        if not success:
            sys.exit(1)
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        print("Asegúrate de que todas las dependencias estén instaladas:")
        print("pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error de prueba: {e}")
        sys.exit(1)
