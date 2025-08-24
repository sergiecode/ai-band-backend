# AI Band Backend Integration Guide

**For AI Band Plugin (C++ JUCE) and AI Band Orchestrator (Python Server)**

This document provides comprehensive integration instructions for using the AI Band Backend with the companion projects: `ai-band-plugin` (JUCE-based audio plugin) and `ai-band-orchestrator` (Python coordination server).

## 📋 Table of Contents

1. [AI Band Backend Overview](#ai-band-backend-overview)
2. [Integration Architecture](#integration-architecture)
3. [AI Band Plugin Integration](#ai-band-plugin-integration)
4. [AI Band Orchestrator Integration](#ai-band-orchestrator-integration)
5. [Communication Protocols](#communication-protocols)
6. [File Formats and Data Structures](#file-formats-and-data-structures)
7. [API Reference](#api-reference)
8. [Error Handling](#error-handling)
9. [Performance Considerations](#performance-considerations)
10. [Development Workflow](#development-workflow)

---

## 🎯 AI Band Backend Overview

### Core Functionality
The AI Band Backend (`ai-band-backend`) provides:
- **Chord progression analysis** from guitar input
- **Intelligent bass line generation** following musical theory
- **Dynamic drum pattern creation** with realistic timing
- **Professional MIDI file output** compatible with all DAWs
- **Real-time generation capabilities** for live performance

### Key Components
```
src/
├── main.py              # Entry point and example usage
├── chord_detection.py   # ChordDetector class
├── midi_generator.py    # MidiGenerator class
└── models/              # AI models directory
```

### Dependencies
```python
# Core dependencies (see requirements.txt)
pretty_midi==0.2.10
mido==1.3.2
numpy==1.24.3
```

---

## 🏗️ Integration Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   AI Band       │    │   AI Band       │    │   AI Band       │
│   Backend       │◄──►│  Orchestrator   │◄──►│    Plugin       │
│   (Python)      │    │   (Python)      │    │   (C++ JUCE)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
        │                        │                        │
        ▼                        ▼                        ▼
   MIDI Files              REST API              VST/AU Plugin
   Chord Analysis         WebSocket              DAW Integration
   AI Generation          File Management        Real-time Playback
```

### Communication Flow
1. **Input**: Guitar/MIDI → Plugin → Orchestrator
2. **Processing**: Orchestrator → Backend (chord analysis + generation)
3. **Output**: Backend → Orchestrator → Plugin → DAW

---

## 🎸 AI Band Plugin Integration

### Plugin Requirements (C++ JUCE)

#### 1. MIDI File Import/Export
```cpp
// Example JUCE integration
class AIBandPlugin : public AudioProcessor {
public:
    // Load MIDI from AI Band Backend
    void loadAIGeneratedMIDI(const String& filePath) {
        File midiFile(filePath);
        if (midiFile.existsAsFile()) {
            FileInputStream stream(midiFile);
            MidiFile midi;
            midi.readFrom(stream);
            // Process MIDI data...
        }
    }
    
    // Send chord progression to orchestrator
    void sendChordProgression(const ChordProgression& chords) {
        // HTTP POST to orchestrator
        // Format: JSON chord data
    }
};
```

#### 2. Expected Input Format from Backend
```json
{
  "bass_track": {
    "file_path": "output/bass_track.mid",
    "instrument": "Electric Bass",
    "note_range": [24, 72],
    "duration": 8.0
  },
  "drum_track": {
    "file_path": "output/drum_track.mid", 
    "instrument": "Drum Kit",
    "duration": 8.0
  },
  "metadata": {
    "tempo": 120,
    "key": "C",
    "time_signature": "4/4"
  }
}
```

#### 3. Required Plugin Features
- **MIDI Import**: Read `.mid` files from backend
- **Real-time Playback**: Stream MIDI data to DAW
- **Chord Input**: Capture guitar/MIDI input for analysis
- **Parameter Control**: Tempo, key, style adjustments
- **File Management**: Handle temporary MIDI files

#### 4. Communication with Orchestrator
```cpp
// HTTP client for orchestrator communication
class OrchestratorClient {
public:
    // Generate tracks from chord progression
    bool generateTracks(const ChordProgression& chords, 
                       int tempo, const String& key) {
        json request = {
            {"chords", chordsToJson(chords)},
            {"tempo", tempo},
            {"key", key}
        };
        
        auto response = httpPost("http://localhost:8080/generate", request);
        return response.status == 200;
    }
    
    // Get generated MIDI files
    MidiFiles getGeneratedFiles() {
        auto response = httpGet("http://localhost:8080/files/latest");
        return parseMidiFiles(response.body);
    }
};
```

---

## 🎛️ AI Band Orchestrator Integration

### Server Requirements (Python FastAPI/Flask)

#### 1. Backend Integration Module
```python
# orchestrator/backend_client.py
import sys
sys.path.append('../ai-band-backend/src')

from chord_detection import ChordDetector
from midi_generator import MidiGenerator
import json
import os
from pathlib import Path

class BackendClient:
    def __init__(self):
        self.detector = ChordDetector()
        self.generator = MidiGenerator()
        self.output_dir = Path("generated_midi")
        self.output_dir.mkdir(exist_ok=True)
    
    def generate_tracks(self, chord_data, tempo=120, key="C"):
        """Generate bass and drum tracks from chord progression."""
        # Convert input to backend format
        chords = self._parse_chord_data(chord_data)
        
        # Generate tracks
        bass_midi = self.generator.generate_bass_track(chords, tempo, key)
        drum_midi = self.generator.generate_drum_track(chords, tempo, duration=8.0)
        
        # Save files with unique names
        timestamp = int(time.time())
        bass_file = self.output_dir / f"bass_{timestamp}.mid"
        drum_file = self.output_dir / f"drum_{timestamp}.mid"
        
        bass_midi.write(str(bass_file))
        drum_midi.write(str(drum_file))
        
        return {
            "bass_file": str(bass_file),
            "drum_file": str(drum_file),
            "metadata": {
                "tempo": tempo,
                "key": key,
                "timestamp": timestamp
            }
        }
    
    def analyze_chords(self, chord_progression):
        """Analyze chord progression and return musical info."""
        return self.detector.analyze_chord_progression(chord_progression)
```

#### 2. REST API Endpoints
```python
# orchestrator/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from backend_client import BackendClient
import json

app = FastAPI(title="AI Band Orchestrator")
backend = BackendClient()

class ChordProgression(BaseModel):
    chords: list
    tempo: int = 120
    key: str = "C"

class GenerationResponse(BaseModel):
    bass_file: str
    drum_file: str
    metadata: dict

@app.post("/generate", response_model=GenerationResponse)
async def generate_tracks(progression: ChordProgression):
    """Generate bass and drum tracks from chord progression."""
    try:
        result = backend.generate_tracks(
            progression.chords, 
            progression.tempo, 
            progression.key
        )
        return GenerationResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze")
async def analyze_chords(progression: ChordProgression):
    """Analyze chord progression and return musical information."""
    try:
        analysis = backend.analyze_chords(progression.chords)
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/files/{filename}")
async def get_midi_file(filename: str):
    """Serve generated MIDI files."""
    file_path = backend.output_dir / filename
    if file_path.exists():
        return FileResponse(str(file_path))
    raise HTTPException(status_code=404, detail="File not found")
```

#### 3. WebSocket for Real-time Communication
```python
# orchestrator/websocket_handler.py
from fastapi import WebSocket
import json
import asyncio

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Receive chord data from plugin
            data = await websocket.receive_text()
            chord_data = json.loads(data)
            
            # Generate tracks
            result = backend.generate_tracks(chord_data["chords"])
            
            # Send back file paths
            await websocket.send_text(json.dumps(result))
            
    except Exception as e:
        await websocket.send_text(json.dumps({"error": str(e)}))
```

---

## 📡 Communication Protocols

### 1. Chord Progression Format
```json
{
  "chords": [
    {
      "chord": "C",
      "start_time": 0.0,
      "duration": 2.0,
      "confidence": 0.95
    },
    {
      "chord": "Am", 
      "start_time": 2.0,
      "duration": 2.0,
      "confidence": 0.90
    }
  ],
  "tempo": 120,
  "key": "C",
  "time_signature": "4/4"
}
```

### 2. Generation Response Format
```json
{
  "success": true,
  "files": {
    "bass": {
      "path": "/generated/bass_1692875432.mid",
      "url": "http://localhost:8080/files/bass_1692875432.mid",
      "size_bytes": 1024
    },
    "drums": {
      "path": "/generated/drum_1692875432.mid", 
      "url": "http://localhost:8080/files/drum_1692875432.mid",
      "size_bytes": 2048
    }
  },
  "metadata": {
    "generation_time_ms": 150,
    "tempo": 120,
    "key": "C",
    "total_duration": 8.0
  }
}
```

### 3. Error Response Format
```json
{
  "success": false,
  "error": {
    "code": "GENERATION_FAILED",
    "message": "Invalid chord progression format",
    "details": "Missing required field: start_time"
  }
}
```

---

## 📄 File Formats and Data Structures

### 1. MIDI File Specifications
- **Format**: Standard MIDI Format 1
- **Resolution**: 480 ticks per quarter note
- **Tracks**: Separate tracks for bass and drums
- **Instruments**: 
  - Bass: Program 33 (Electric Bass - pick)
  - Drums: Channel 10 (Standard drum kit)

### 2. Bass Track Structure
```python
# MIDI note ranges and patterns
BASS_NOTE_RANGE = (24, 72)  # C1 to C4
BASS_PATTERNS = {
    "whole_notes": [(0, 4.0)],           # Root on beat 1
    "half_notes": [(0, 2.0), (2.0, 2.0)], # Root on beats 1,3
    "quarter_notes": [(0, 1.0), (1.0, 1.0), (2.0, 1.0), (3.0, 1.0)]
}
```

### 3. Drum Track Structure
```python
# Standard drum kit mapping
DRUM_MAP = {
    'kick': 36,         # Bass Drum 1
    'snare': 38,        # Acoustic Snare  
    'hihat_closed': 42, # Closed Hi-Hat
    'hihat_open': 46,   # Open Hi-Hat
    'crash': 49,        # Crash Cymbal 1
    'ride': 51          # Ride Cymbal 1
}
```

---

## 🔌 API Reference

### Backend Classes

#### ChordDetector
```python
class ChordDetector:
    def __init__(self):
        # Initialize chord detection parameters
        
    def detect_tempo(self, chord_progression: List[Dict]) -> int:
        """Detect tempo from chord timing."""
        
    def detect_key(self, chord_progression: List[Dict]) -> str:
        """Detect musical key from chords."""
        
    def analyze_chord_progression(self, chords: List[Dict]) -> Dict:
        """Complete analysis of chord progression."""
        
    def extract_features_for_ai(self, chords: List[Dict]) -> np.ndarray:
        """Extract features for AI model input."""
```

#### MidiGenerator
```python
class MidiGenerator:
    def __init__(self):
        # Initialize MIDI generation parameters
        
    def generate_bass_track(self, chord_progression: List[Dict], 
                          tempo: int = 120, key: str = "C") -> pretty_midi.PrettyMIDI:
        """Generate bass track following chord progression."""
        
    def generate_drum_track(self, chord_progression: List[Dict],
                          tempo: int = 120, duration: float = 8.0) -> pretty_midi.PrettyMIDI:
        """Generate drum track with realistic patterns."""
        
    def combine_tracks(self, bass_midi: pretty_midi.PrettyMIDI,
                      drum_midi: pretty_midi.PrettyMIDI) -> pretty_midi.PrettyMIDI:
        """Combine multiple tracks into single MIDI file."""
```

### Usage Examples

#### Basic Generation
```python
from chord_detection import ChordDetector
from midi_generator import MidiGenerator

# Initialize
detector = ChordDetector()
generator = MidiGenerator()

# Sample chord progression
chords = [
    {"chord": "C", "start_time": 0.0, "duration": 2.0},
    {"chord": "Am", "start_time": 2.0, "duration": 2.0},
    {"chord": "F", "start_time": 4.0, "duration": 2.0},
    {"chord": "G", "start_time": 6.0, "duration": 2.0}
]

# Generate tracks
bass_midi = generator.generate_bass_track(chords, tempo=120)
drum_midi = generator.generate_drum_track(chords, tempo=120, duration=8.0)

# Save files
bass_midi.write("output/bass.mid")
drum_midi.write("output/drums.mid")
```

---

## ⚠️ Error Handling

### Common Error Scenarios

#### 1. Invalid Chord Data
```python
# Handle missing or invalid chord information
try:
    result = generator.generate_bass_track(invalid_chords)
except Exception as e:
    # Backend gracefully handles invalid data with defaults
    print(f"Warning: {e}")
    # Backend will use default chord (C) and continue
```

#### 2. File I/O Errors
```python
# Handle file system issues
try:
    bass_midi.write("output/bass.mid")
except OSError as e:
    # Handle permission/disk space issues
    print(f"File write error: {e}")
```

#### 3. Network Communication
```python
# Handle orchestrator communication failures
try:
    response = requests.post("http://localhost:8080/generate", json=data)
    response.raise_for_status()
except requests.RequestException as e:
    # Fallback to local generation or cached files
    print(f"Network error: {e}")
```

### Error Recovery Strategies
1. **Graceful Degradation**: Use defaults for invalid inputs
2. **Retry Logic**: Automatic retry for network failures
3. **Fallback Modes**: Local generation when server unavailable
4. **Validation**: Input validation before processing

---

## ⚡ Performance Considerations

### Backend Performance
- **Chord Analysis**: ~10ms for typical progressions (4-8 chords)
- **MIDI Generation**: ~100ms for 8-second tracks
- **File I/O**: ~10ms for typical MIDI files
- **Memory Usage**: ~50MB for backend process

### Optimization Tips
1. **Batch Processing**: Generate multiple tracks in single call
2. **Caching**: Cache generated files for repeated requests
3. **Async Processing**: Use async/await for network operations
4. **Resource Pooling**: Reuse backend instances

### Real-time Requirements
- **Latency Target**: <200ms total (input → output)
- **Buffer Size**: 512-1024 samples for audio plugins
- **Threading**: Separate audio and generation threads

---

## 🔄 Development Workflow

### 1. Plugin Development Setup
```bash
# Clone all repositories
git clone https://github.com/sergiecode/ai-band-backend.git
git clone https://github.com/sergiecode/ai-band-plugin.git
git clone https://github.com/sergiecode/ai-band-orchestrator.git

# Setup backend
cd ai-band-backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
python run_all_tests.py  # Verify installation

# Setup orchestrator
cd ../ai-band-orchestrator
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Setup plugin (JUCE/C++)
cd ../ai-band-plugin
# Follow JUCE setup instructions
```

### 2. Development Testing
```bash
# Terminal 1: Start backend (for testing)
cd ai-band-backend/src
python main.py

# Terminal 2: Start orchestrator
cd ai-band-orchestrator
python main.py

# Terminal 3: Test integration
curl -X POST http://localhost:8080/generate \
  -H "Content-Type: application/json" \
  -d '{"chords": [{"chord": "C", "start_time": 0, "duration": 2}]}'
```

### 3. Plugin Integration Testing
```cpp
// Test MIDI file loading in plugin
void testMIDIIntegration() {
    // Generate test files using backend
    AIBandBackend backend;
    auto result = backend.generateTracks(testChords);
    
    // Load files in plugin
    plugin.loadMIDIFile(result.bassFile);
    plugin.loadMIDIFile(result.drumFile);
    
    // Verify playback
    assert(plugin.hasValidMIDIData());
}
```

### 4. Continuous Integration
```yaml
# .github/workflows/integration.yml
name: AI Band Integration Tests
on: [push, pull_request]
jobs:
  test-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Test Backend
        run: |
          cd ai-band-backend
          pip install -r requirements.txt
          python run_all_tests.py
  
  test-orchestrator:
    needs: test-backend
    runs-on: ubuntu-latest
    steps:
      - name: Test Orchestrator Integration
        run: |
          # Start backend and orchestrator
          # Run integration tests
```

---

## 📚 Additional Resources

### Documentation Links
- [AI Band Backend Repository](https://github.com/sergiecode/ai-band-backend)
- [JUCE Framework Documentation](https://juce.com/learn/documentation)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [MIDI File Format Specification](https://www.midi.org/specifications-old/item/the-midi-1-0-specification)

### Example Projects
- **Backend Examples**: `ai-band-backend/examples.py`
- **Test Cases**: `ai-band-backend/test_*.py`
- **Configuration**: `ai-band-backend/config.ini`

### Support and Community
- **Issues**: Report bugs in respective repositories
- **Discussions**: Use GitHub Discussions for questions
- **Contributing**: See CONTRIBUTING.md in each repository

---

## 🎵 Quick Start Checklist

### For Plugin Developers (C++ JUCE)
- [ ] Set up JUCE development environment
- [ ] Clone and test ai-band-backend
- [ ] Implement MIDI file loading/saving
- [ ] Add HTTP client for orchestrator communication
- [ ] Implement chord progression input capture
- [ ] Add real-time MIDI playback
- [ ] Test with DAW integration

### For Orchestrator Developers (Python)
- [ ] Set up Python FastAPI environment
- [ ] Import ai-band-backend modules
- [ ] Implement REST API endpoints
- [ ] Add WebSocket support for real-time
- [ ] Implement file management system
- [ ] Add error handling and logging
- [ ] Test end-to-end integration

### Integration Testing
- [ ] Test chord progression → MIDI generation
- [ ] Verify file formats and compatibility
- [ ] Test real-time performance
- [ ] Validate error handling
- [ ] Test with multiple DAWs
- [ ] Performance benchmarking

---

*This integration guide ensures seamless connectivity between the AI Band Backend and its companion projects. Follow the specifications carefully for optimal compatibility and performance.*

**Created by Sergie Code - AI Tools for Musicians**  
**Last Updated**: August 24, 2025
