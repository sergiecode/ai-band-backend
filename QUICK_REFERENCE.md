# AI Band Backend - Referencia Rápida de Integración

**Para Agentes de IA desarrollando ai-band-plugin y ai-band-orchestrator**

## 🚀 Puntos de Integración Esenciales

### 1. Importación del Backend (Python)
```python
# En proyecto orchestrator
import sys
sys.path.append('../ai-band-backend/src')
from chord_detection import ChordDetector
from midi_generator import MidiGenerator
```

### 2. Estructuras de Datos Principales

#### Formato de Progresión de Acordes
```json
{
  "chord": "C",
  "start_time": 0.0,
  "duration": 2.0
}
```

#### Respuesta de Generación
```json
{
  "bass_file": "path/to/bass.mid",
  "drum_file": "path/to/drums.mid", 
  "metadata": {"tempo": 120, "key": "C"}
}
```

### 3. Uso de Clases del Backend

#### ChordDetector
```python
detector = ChordDetector()
tempo = detector.detect_tempo(chord_progression)
key = detector.detect_key(chord_progression)
analysis = detector.analyze_chord_progression(chord_progression)
```

#### MidiGenerator  
```python
generator = MidiGenerator()
bass_midi = generator.generate_bass_track(chords, tempo=120, key="C")
drum_midi = generator.generate_drum_track(chords, tempo=120, duration=8.0)
combined = generator.combine_tracks(bass_midi, drum_midi)
```

### 4. Operaciones de Archivos
```python
# Guardar archivos MIDI
bass_midi.write("output/bass.mid")
drum_midi.write("output/drums.mid")

# Cargar en plugin (C++ JUCE)
MidiFile midiFile;
FileInputStream stream(File("output/bass.mid"));
midiFile.readFrom(stream);
```

### 5. Endpoints de API REST (Orchestrator)
```python
@app.post("/generate")
async def generate_tracks(progression: ChordProgression):
    result = backend.generate_tracks(progression.chords, progression.tempo, progression.key)
    return result

@app.get("/files/{filename}")
async def get_midi_file(filename: str):
    return FileResponse(f"generated/{filename}")
```

### 6. Comunicación de Plugin (C++ JUCE)
```cpp
// Enviar datos de acordes al orchestrator
json request = {
    {"chords", chordsToJson(chords)},
    {"tempo", 120},
    {"key", "C"}
};
auto response = httpPost("http://localhost:8080/generate", request);

// Cargar MIDI generado
plugin.loadMIDIFile(response["bass_file"]);
plugin.loadMIDIFile(response["drum_file"]);
```

## 🎯 Requisitos Clave

### Plugin (C++ JUCE)
- Importación/exportación de archivos MIDI
- Cliente HTTP para orchestrator
- Procesamiento de audio en tiempo real
- Integración con DAW (VST/AU)
- Captura de entrada de acordes

### Orchestrator (Python)
- Servidor FastAPI/Flask
- Módulo de integración backend
- Sistema de gestión de archivos
- Soporte WebSocket
- Manejo de errores

## 📁 Dependencias Requeridas

### Backend (ya instaladas)
```
pretty_midi==0.2.10
mido==1.3.2
numpy==1.24.3
```

### Orchestrator (a agregar)
```
fastapi==0.68.0
uvicorn==0.15.0
python-multipart==0.0.5
websockets==10.0
```

### Plugin (C++ JUCE)
```
JUCE Framework 7.0+
Librería cliente HTTP (cpp-httplib)
Parser JSON (nlohmann/json)
```

## ⚡ Objetivos de Rendimiento
- Análisis de acordes: <50ms
- Generación MIDI: <200ms
- E/S de archivos: <20ms
- Latencia total: <300ms

## 🔗 Estructura del Repositorio
```
ai-band-ecosystem/
├── ai-band-backend/     # ✅ Completo (núcleo Python)
├── ai-band-plugin/      # 🔄 A crear (C++ JUCE)
└── ai-band-orchestrator/ # 🔄 A crear (servidor Python)
```

---
**Usa INTEGRATION_GUIDE.md para especificaciones completas**
