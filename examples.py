"""
Uso de Ejemplo del AI Band Backend
Creado por Sergie Code

Este script demuestra varias formas de usar el AI Band Backend
para generar pistas de bajo y batería desde progresiones de acordes.
"""

import sys
from pathlib import Path

# Add src to Python path
sys.path.append(str(Path(__file__).parent / "src"))

from chord_detection import ChordDetector
from midi_generator import MidiGenerator


def example_basic_generation():
    """Ejemplo 1: Generación básica de progresión de acordes."""
    print("\nEjemplo 1: Generación Básica")
    print("-" * 40)
    
    # Inicializar componentes
    detector = ChordDetector()
    generator = MidiGenerator()
    
    # Definir una progresión simple de acordes
    chords = [
        {"chord": "C", "start_time": 0.0, "duration": 2.0},
        {"chord": "Am", "start_time": 2.0, "duration": 2.0},
        {"chord": "F", "start_time": 4.0, "duration": 2.0},
        {"chord": "G", "start_time": 6.0, "duration": 2.0},
    ]
    
    # Analizar la progresión
    analysis = detector.analyze_chord_progression(chords)
    print(f"Análisis: {analysis}")
    
    # Generar pistas
    bass_midi = generator.generate_bass_track(chords, tempo=analysis["tempo"])
    drum_midi = generator.generate_drum_track(chords, tempo=analysis["tempo"])
    
    # Guardar archivos
    output_dir = Path("examples_output")
    output_dir.mkdir(exist_ok=True)
    
    bass_file = output_dir / "example1_bass.mid"
    drum_file = output_dir / "example1_drums.mid"
    
    bass_midi.write(str(bass_file))
    drum_midi.write(str(drum_file))
    
    print(f"Archivos guardados: {bass_file}, {drum_file}")


def example_different_styles():
    """Ejemplo 2: Diferentes estilos musicales y tempos."""
    print("\nEjemplo 2: Diferentes Estilos")
    print("-" * 40)
    
    generator = MidiGenerator()
    
    # Estilo 1: Balada lenta
    ballad_chords = [
        {"chord": "C", "start_time": 0.0, "duration": 4.0},
        {"chord": "Am", "start_time": 4.0, "duration": 4.0},
        {"chord": "F", "start_time": 8.0, "duration": 4.0},
        {"chord": "G", "start_time": 12.0, "duration": 4.0},
    ]
    
    bass_ballad = generator.generate_bass_track(ballad_chords, tempo=70)
    
    # Estilo 2: Rock rápido
    rock_chords = [
        {"chord": "Em", "start_time": 0.0, "duration": 1.0},
        {"chord": "C", "start_time": 1.0, "duration": 1.0},
        {"chord": "G", "start_time": 2.0, "duration": 1.0},
        {"chord": "D", "start_time": 3.0, "duration": 1.0},
    ]
    
    bass_rock = generator.generate_bass_track(rock_chords, tempo=140)
    drum_rock = generator.generate_drum_track(rock_chords, tempo=140, duration=4.0)
    
    # Guardar archivos
    output_dir = Path("examples_output")
    output_dir.mkdir(exist_ok=True)
    
    bass_ballad.write(str(output_dir / "example2_ballad_bass.mid"))
    bass_rock.write(str(output_dir / "example2_rock_bass.mid"))
    drum_rock.write(str(output_dir / "example2_rock_drums.mid"))
    
    print("Ejemplos de diferentes estilos guardados")


def example_combined_track():
    """Ejemplo 3: Combinando bajo y batería en un archivo."""
    print("\nEjemplo 3: Pista Combinada")
    print("-" * 40)
    
    generator = MidiGenerator()
    
    # Crear una progresión
    chords = [
        {"chord": "Am", "start_time": 0.0, "duration": 2.0},
        {"chord": "F", "start_time": 2.0, "duration": 2.0},
        {"chord": "C", "start_time": 4.0, "duration": 2.0},
        {"chord": "G", "start_time": 6.0, "duration": 2.0},
    ]
    
    # Generar pistas individuales
    bass_midi = generator.generate_bass_track(chords, tempo=100)
    drum_midi = generator.generate_drum_track(chords, tempo=100, duration=8.0)
    
    # Combinar pistas
    combined_midi = generator.combine_tracks(bass_midi, drum_midi)
    
    # Guardar archivo combinado
    output_dir = Path("examples_output")
    output_dir.mkdir(exist_ok=True)
    
    combined_file = output_dir / "example3_combined.mid"
    combined_midi.write(str(combined_file))
    
    print(f"Pista combinada guardada: {combined_file}")


def example_ai_features():
    """Ejemplo 4: Extracción de características de IA para entrenamiento futuro de modelos."""
    print("\nEjemplo 4: Características de IA")
    print("-" * 40)
    
    detector = ChordDetector()
    
    # Progresión compleja de acordes
    chords = [
        {"chord": "Dm", "start_time": 0.0, "duration": 1.5},
        {"chord": "G", "start_time": 1.5, "duration": 1.5},
        {"chord": "C", "start_time": 3.0, "duration": 1.0},
        {"chord": "Am", "start_time": 4.0, "duration": 2.0},
        {"chord": "F", "start_time": 6.0, "duration": 1.0},
        {"chord": "G", "start_time": 7.0, "duration": 1.0},
    ]
    
    # Extraer características para IA
    features = detector.extract_features_for_ai(chords)
    analysis = detector.analyze_chord_progression(chords)
    
    print(f"Características de IA: {features}")
    print(f"Análisis Musical: {analysis}")
    
    # Generar con método mejorado por IA (placeholder)
    generator = MidiGenerator()
    ai_bass = generator.generate_ai_bass_track(chords, tempo=analysis["tempo"])
    
    # Guardar pista generada por IA
    output_dir = Path("examples_output")
    output_dir.mkdir(exist_ok=True)
    
    ai_file = output_dir / "example4_ai_bass.mid"
    ai_bass.write(str(ai_file))
    
    print(f"Bajo mejorado por IA guardado: {ai_file}")


def main():
    """Ejecutar todos los ejemplos."""
    print("🎸 AI Band Backend - Ejemplos")
    print("=" * 50)
    print("Creado por Sergie Code")
    print("Estos ejemplos muestran diferentes formas de usar el AI Band Backend")
    
    try:
        example_basic_generation()
        example_different_styles()
        example_combined_track()
        example_ai_features()
        
        print("\n🎉 ¡Todos los ejemplos completados exitosamente!")
        print("📁 Revisa la carpeta 'examples_output' para los archivos MIDI generados")
        print("🎵 ¡Importa estos archivos a tu DAW para escuchar los resultados!")
        
    except Exception as e:
        print(f"\n❌ Error ejecutando ejemplos: {e}")
        print("Asegúrate de haber instalado todas las dependencias:")
        print("pip install -r requirements.txt")


if __name__ == "__main__":
    main()
