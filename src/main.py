"""
AI Band Backend - Punto de Entrada Principal
Creado por Sergie Code - Herramientas de IA para Músicos

Este es el punto de entrada principal para el AI Band Backend que genera
pistas de bajo y batería desde entrada de guitarra usando modelos de IA.
"""

import sys
from pathlib import Path

# Add src to Python path
sys.path.append(str(Path(__file__).parent))

from chord_detection import ChordDetector
from midi_generator import MidiGenerator


def main():
    """
    Función principal que demuestra el pipeline del AI Band Backend:
    1. Detectar acordes desde entrada de guitarra (simulada)
    2. Generar pistas MIDI de bajo y batería
    3. Guardar archivos de salida
    """
    print("🎸 AI Band Backend - Generando Música con IA")
    print("=" * 50)
    
    # Inicializar componentes
    chord_detector = ChordDetector()
    midi_generator = MidiGenerator()
    
    # Progresión de acordes de ejemplo (entrada de guitarra simulada)
    print("🎵 Analizando progresión de acordes...")
    sample_chords = [
        {"chord": "C", "start_time": 0.0, "duration": 2.0},
        {"chord": "Am", "start_time": 2.0, "duration": 2.0},
        {"chord": "F", "start_time": 4.0, "duration": 2.0},
        {"chord": "G", "start_time": 6.0, "duration": 2.0},
    ]
    
    # Detectar información de tempo y tonalidad
    tempo = chord_detector.detect_tempo(sample_chords)
    key = chord_detector.detect_key(sample_chords)
    
    print(f"🎼 Tempo detectado: {tempo} BPM")
    print(f"🎹 Tonalidad detectada: {key}")
    
    # Generar pista de bajo
    print("🎸 Generando pista de bajo...")
    bass_midi = midi_generator.generate_bass_track(
        chord_progression=sample_chords,
        tempo=tempo,
        key=key
    )
    
    # Generar pista de batería
    print("🥁 Generando pista de batería...")
    drum_midi = midi_generator.generate_drum_track(
        chord_progression=sample_chords,
        tempo=tempo,
        duration=8.0  # Duración total en segundos
    )
    
    # Crear directorio de salida
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    # Guardar archivos MIDI
    bass_file = output_dir / "bass_track.mid"
    drum_file = output_dir / "drum_track.mid"
    
    bass_midi.write(str(bass_file))
    drum_midi.write(str(drum_file))
    
    print(f"✅ Pista de bajo guardada: {bass_file}")
    print(f"✅ Pista de batería guardada: {drum_file}")
    print("\n🎉 ¡Generación del AI Band Backend completa!")
    print("📁 Revisa la carpeta 'output' para tus archivos MIDI")
    print("🎵 ¡Importa estos archivos a tu DAW para escuchar la magia!")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Asegúrate de que todas las dependencias estén instaladas:")
        print("pip install -r requirements.txt")
        sys.exit(1)
