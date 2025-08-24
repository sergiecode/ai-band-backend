# AI Band Backend - Quick Integration Reference

**For AI Agents developing ai-band-plugin and ai-band-orchestrator**

## 🚀 Essential Integration Points

### 1. Backend Import (Python)
```python
# In orchestrator project
import sys
sys.path.append('../ai-band-backend/src')
from chord_detection import ChordDetector
from midi_generator import MidiGenerator
```

### 2. Core Data Structures

#### Chord Progression Format
```json
{
  "chord": "C",
  "start_time": 0.0,
  "duration": 2.0
}
```

#### Generation Response
```json
{
  "bass_file": "path/to/bass.mid",
  "drum_file": "path/to/drums.mid", 
  "metadata": {"tempo": 120, "key": "C"}
}
```

### 3. Backend Classes Usage

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

### 4. File Operations
```python
# Save MIDI files
bass_midi.write("output/bass.mid")
drum_midi.write("output/drums.mid")

# Load in plugin (C++ JUCE)
MidiFile midiFile;
FileInputStream stream(File("output/bass.mid"));
midiFile.readFrom(stream);
```

### 5. REST API Endpoints (Orchestrator)
```python
@app.post("/generate")
async def generate_tracks(progression: ChordProgression):
    result = backend.generate_tracks(progression.chords, progression.tempo, progression.key)
    return result

@app.get("/files/{filename}")
async def get_midi_file(filename: str):
    return FileResponse(f"generated/{filename}")
```

### 6. Plugin Communication (C++ JUCE)
```cpp
// Send chord data to orchestrator
json request = {
    {"chords", chordsToJson(chords)},
    {"tempo", 120},
    {"key", "C"}
};
auto response = httpPost("http://localhost:8080/generate", request);

// Load generated MIDI
plugin.loadMIDIFile(response["bass_file"]);
plugin.loadMIDIFile(response["drum_file"]);
```

## 🎯 Key Requirements

### Plugin (C++ JUCE)
- MIDI file import/export
- HTTP client for orchestrator
- Real-time audio processing
- DAW integration (VST/AU)
- Chord input capture

### Orchestrator (Python)
- FastAPI/Flask server
- Backend integration module
- File management system
- WebSocket support
- Error handling

## 📁 Required Dependencies

### Backend (already installed)
```
pretty_midi==0.2.10
mido==1.3.2
numpy==1.24.3
```

### Orchestrator (to be added)
```
fastapi==0.68.0
uvicorn==0.15.0
python-multipart==0.0.5
websockets==10.0
```

### Plugin (C++ JUCE)
```
JUCE Framework 7.0+
HTTP client library (cpp-httplib)
JSON parser (nlohmann/json)
```

## ⚡ Performance Targets
- Chord analysis: <50ms
- MIDI generation: <200ms
- File I/O: <20ms
- Total latency: <300ms

## 🔗 Repository Structure
```
ai-band-ecosystem/
├── ai-band-backend/     # ✅ Complete (Python core)
├── ai-band-plugin/      # 🔄 To be created (C++ JUCE)
└── ai-band-orchestrator/ # 🔄 To be created (Python server)
```

---
**Use INTEGRATION_GUIDE.md for complete specifications**
