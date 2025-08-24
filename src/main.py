"""
AI Band Backend - Punto de Entrada Principal
Creado por Sergie Code - Herramientas de IA para Músicos

Este es el punto de entrada principal para el AI Band Backend que genera
pistas de bajo y batería desde entrada de guitarra usando modelos de IA.

PROPÓSITO DEL ARCHIVO:
- Demostrar cómo usar el sistema completo
- Mostrar el flujo de trabajo típico del AI Band Backend
- Generar archivos MIDI de ejemplo para pruebas
- Servir como punto de entrada para nuevos usuarios

FLUJO DEL PROGRAMA:
1. Inicializar los componentes (detector de acordes y generador MIDI)
2. Definir una progresión de acordes de ejemplo
3. Analizar la progresión para obtener tempo y tonalidad
4. Generar pistas de bajo y batería
5. Guardar los archivos MIDI resultantes
"""

import sys
from pathlib import Path

# Agregar el directorio src al path de Python para poder importar nuestros módulos
# Esto es necesario para que Python encuentre nuestros archivos chord_detection.py y midi_generator.py
sys.path.append(str(Path(__file__).parent))

# Importar nuestras clases principales del proyecto
from chord_detection import ChordDetector  # Para analizar acordes y detectar tempo/tonalidad
from midi_generator import MidiGenerator    # Para generar archivos MIDI de bajo y batería


def main():
    """
    Función principal que demuestra el pipeline del AI Band Backend:
    1. Detectar acordes desde entrada de guitarra (simulada)
    2. Generar pistas MIDI de bajo y batería
    3. Guardar archivos de salida
    
    EXPLICACIÓN DETALLADA:
    Esta función es el corazón del programa. Muestra cómo usar todas las
    funcionalidades del AI Band Backend de manera práctica.
    
    ¿POR QUÉ ESTA FUNCIÓN ES IMPORTANTE?
    - Demuestra el uso completo del sistema
    - Proporciona un ejemplo funcional para desarrolladores
    - Genera archivos de prueba para validar que todo funciona
    """
    # Mostrar mensaje de bienvenida al usuario
    print("🎸 AI Band Backend - Generando Música con IA")
    print("=" * 50)
    
    # PASO 1: Inicializar los componentes principales del sistema
    # ChordDetector: Se encarga de analizar progresiones de acordes
    # MidiGenerator: Se encarga de crear archivos MIDI
    chord_detector = ChordDetector()
    midi_generator = MidiGenerator()
    
    # PASO 2: Definir una progresión de acordes de ejemplo
    # En un escenario real, estos acordes vendrían de una guitarra real
    # Por ahora usamos datos simulados para demostrar el funcionamiento
    print("🎵 Analizando progresión de acordes...")
    sample_chords = [
        # Cada acorde tiene: nombre del acorde, tiempo de inicio, duración
        {"chord": "C", "start_time": 0.0, "duration": 2.0},   # Do mayor por 2 segundos
        {"chord": "Am", "start_time": 2.0, "duration": 2.0},  # La menor por 2 segundos  
        {"chord": "F", "start_time": 4.0, "duration": 2.0},   # Fa mayor por 2 segundos
        {"chord": "G", "start_time": 6.0, "duration": 2.0},   # Sol mayor por 2 segundos
    ]
    
    # PASO 3: Analizar la progresión para extraer información musical
    # El detector analiza los acordes y extrae características importantes
    tempo = chord_detector.detect_tempo(sample_chords)  # Velocidad de la música (BPM)
    key = chord_detector.detect_key(sample_chords)      # Tonalidad musical (Do, Sol, etc.)
    
    # Mostrar al usuario lo que hemos detectado
    print(f"🎼 Tempo detectado: {tempo} BPM")
    print(f"🎹 Tonalidad detectada: {key}")
    
    # PASO 4: Generar la pista de bajo
    # La pista de bajo sigue la progresión de acordes y proporciona la base armónica
    print("🎸 Generando pista de bajo...")
    bass_midi = midi_generator.generate_bass_track(
        chord_progression=sample_chords,  # Los acordes que debe seguir el bajo
        tempo=tempo,                      # La velocidad detectada
        key=key                          # La tonalidad detectada
    )
    
    # PASO 5: Generar la pista de batería
    # La batería proporciona el ritmo y la base rítmica de la canción
    print("🥁 Generando pista de batería...")
    drum_midi = midi_generator.generate_drum_track(
        chord_progression=sample_chords,  # Los acordes para sincronizar el ritmo
        tempo=tempo,                      # La velocidad para el patrón rítmico
        duration=8.0                      # Duración total en segundos
    )
    
    # PASO 6: Preparar el directorio de salida
    # Crear el directorio donde guardaremos los archivos MIDI generados
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)  # exist_ok=True evita error si ya existe
    
    # PASO 7: Guardar los archivos MIDI
    # Definir las rutas donde guardaremos cada archivo
    bass_file = output_dir / "bass_track.mid"  # Archivo para la pista de bajo
    drum_file = output_dir / "drum_track.mid"  # Archivo para la pista de batería
    
    # Escribir los datos MIDI a archivos físicos
    # El método .write() convierte los datos MIDI en archivos .mid estándar
    bass_midi.write(str(bass_file))  # Guardar bajo
    drum_midi.write(str(drum_file))  # Guardar batería
    
    # PASO 8: Informar al usuario sobre el éxito de la operación
    print(f"✅ Pista de bajo guardada: {bass_file}")
    print(f"✅ Pista de batería guardada: {drum_file}")
    print("\n🎉 ¡Generación del AI Band Backend completa!")
    print("📁 Revisa la carpeta 'output' para tus archivos MIDI")
    print("🎵 ¡Importa estos archivos a tu DAW para escuchar la magia!")


# BLOQUE PRINCIPAL DE EJECUCIÓN
# Este bloque se ejecuta solo cuando el archivo se ejecuta directamente
# (no cuando se importa como módulo)
if __name__ == "__main__":
    try:
        # Intentar ejecutar la función principal
        main()
    except Exception as e:
        # Si algo sale mal, mostrar un mensaje de error útil
        print(f"❌ Error: {e}")
        print("Asegúrate de que todas las dependencias estén instaladas:")
        print("pip install -r requirements.txt")
        sys.exit(1)  # Salir con código de error
