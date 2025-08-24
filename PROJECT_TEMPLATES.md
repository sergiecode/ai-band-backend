# AI Band Ecosystem - Project Structure Templates

## 🎸 ai-band-plugin (C++ JUCE)

```
ai-band-plugin/
├── Source/
│   ├── PluginProcessor.cpp      # Main audio processor
│   ├── PluginProcessor.h        # Audio processor header
│   ├── PluginEditor.cpp         # GUI implementation
│   ├── PluginEditor.h           # GUI header
│   ├── MidiManager.cpp          # MIDI file handling
│   ├── MidiManager.h            # MIDI manager header
│   ├── OrchestratorClient.cpp   # HTTP communication
│   ├── OrchestratorClient.h     # HTTP client header
│   ├── ChordAnalyzer.cpp        # Real-time chord detection
│   └── ChordAnalyzer.h          # Chord analyzer header
├── JuceLibraryCode/             # JUCE framework files
├── Builds/                      # Platform-specific builds
│   ├── VisualStudio2022/        # Windows (VS)
│   ├── Xcode/                   # macOS
│   └── LinuxMakefile/           # Linux
├── Resources/                   # UI assets, presets
├── Tests/                       # Unit tests
├── README.md                    # Plugin documentation
├── CMakeLists.txt              # CMake build config
└── ai-band-plugin.jucer        # JUCE project file
```

### Key Plugin Classes
```cpp
class AIBandProcessor : public AudioProcessor {
    // Audio processing and MIDI handling
    void processBlock(AudioBuffer<float>&, MidiBuffer&);
    void handleMIDI(const MidiBuffer&);
};

class MidiManager {
    // MIDI file import/export
    bool loadMIDIFile(const String& path);
    void saveMIDIFile(const MidiFile&, const String& path);
};

class OrchestratorClient {
    // Communication with orchestrator
    Result generateTracks(const ChordProgression&);
    Result getGeneratedFiles();
};
```

## 🎛️ ai-band-orchestrator (Python FastAPI)

```
ai-band-orchestrator/
├── app/
│   ├── __init__.py
│   ├── main.py                  # FastAPI application
│   ├── config.py                # Configuration settings
│   ├── models/
│   │   ├── __init__.py
│   │   ├── requests.py          # Pydantic request models
│   │   └── responses.py         # Pydantic response models
│   ├── api/
│   │   ├── __init__.py
│   │   ├── endpoints/
│   │   │   ├── __init__.py
│   │   │   ├── generation.py    # Track generation endpoints
│   │   │   ├── analysis.py      # Chord analysis endpoints
│   │   │   └── files.py         # File serving endpoints
│   │   └── websocket.py         # WebSocket handlers
│   ├── services/
│   │   ├── __init__.py
│   │   ├── backend_client.py    # AI Band Backend integration
│   │   ├── file_manager.py      # MIDI file management
│   │   └── cache_manager.py     # Caching system
│   └── utils/
│       ├── __init__.py
│       ├── logging.py           # Logging configuration
│       └── validators.py        # Input validation
├── tests/
│   ├── __init__.py
│   ├── test_generation.py       # Generation endpoint tests
│   ├── test_websocket.py        # WebSocket tests
│   └── test_integration.py      # Backend integration tests
├── generated/                   # Generated MIDI files directory
├── logs/                        # Application logs
├── requirements.txt             # Python dependencies
├── docker-compose.yml           # Docker deployment
├── Dockerfile                   # Docker image
├── README.md                    # Server documentation
└── run.py                       # Application entry point
```

### Key Server Modules
```python
# app/services/backend_client.py
class BackendClient:
    def generate_tracks(self, chords, tempo, key):
        # Use ai-band-backend
        
# app/api/endpoints/generation.py
@router.post("/generate")
async def generate_tracks(request: GenerationRequest):
    # Handle track generation

# app/api/websocket.py
@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # Real-time communication
```

## 🔗 Integration Dependencies

### ai-band-plugin Dependencies
```cmake
# CMakeLists.txt additions
find_package(CURL REQUIRED)      # HTTP client
find_package(nlohmann_json REQUIRED)  # JSON parsing

target_link_libraries(ai-band-plugin 
    PRIVATE
    juce::juce_audio_plugin_client
    juce::juce_audio_utils
    CURL::libcurl
    nlohmann_json::nlohmann_json
)
```

### ai-band-orchestrator Dependencies
```python
# Backend integration setup
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'ai-band-backend', 'src'))

from chord_detection import ChordDetector
from midi_generator import MidiGenerator
```

## 🚀 Development Workflow

### 1. Setup Order
```bash
# 1. Verify backend is working
cd ai-band-backend
python run_all_tests.py

# 2. Create orchestrator
cd ../ai-band-orchestrator  
python -m venv venv
pip install -r requirements.txt
python run.py

# 3. Create plugin
cd ../ai-band-plugin
# Setup JUCE project
# Build and test
```

### 2. Testing Integration
```bash
# Terminal 1: Start orchestrator
cd ai-band-orchestrator
python run.py

# Terminal 2: Test REST API
curl -X POST http://localhost:8080/generate \
  -H "Content-Type: application/json" \
  -d '{"chords": [{"chord": "C", "start_time": 0, "duration": 2}], "tempo": 120}'

# Terminal 3: Test with plugin
# Load plugin in DAW
# Send chord progression
# Verify MIDI playback
```

### 3. File Sharing Strategy
```
shared_output/
├── midi_files/
│   ├── bass_<timestamp>.mid
│   ├── drum_<timestamp>.mid
│   └── combined_<timestamp>.mid
├── metadata/
│   └── generation_<timestamp>.json
└── cache/
    └── chord_analysis_cache.json
```

## 📊 Communication Flow

```
Guitar Input → Plugin → Orchestrator → Backend → Generation
     ↓             ↓         ↓           ↓         ↓
  MIDI Data → Chord Data → REST API → Analysis → MIDI Files
     ↓             ↓         ↓           ↓         ↓
  DAW Audio ←  Plugin  ←  WebSocket ←  Server  ←  Files
```

## 🎯 Success Criteria

### Plugin (C++ JUCE)
- [ ] Loads as VST/AU in major DAWs
- [ ] Captures real-time MIDI input
- [ ] Communicates with orchestrator via HTTP
- [ ] Plays generated MIDI tracks
- [ ] Provides intuitive user interface

### Orchestrator (Python)
- [ ] Integrates seamlessly with ai-band-backend
- [ ] Provides REST API for track generation
- [ ] Handles WebSocket connections
- [ ] Manages file serving and cleanup
- [ ] Includes proper error handling and logging

### Integration
- [ ] End-to-end latency < 500ms
- [ ] Handles concurrent requests
- [ ] Graceful error recovery
- [ ] Compatible with major DAWs
- [ ] Professional audio quality

---

**Use this structure as a foundation for creating the companion projects. The ai-band-backend provides the core AI functionality, while these projects handle user interaction and real-time processing.**
