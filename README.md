# 🎸 AI Band Backend

**Creado por Sergie Code - Herramientas de IA para Músicos**

Un backend de Python para generar pistas de bajo y batería automáticamente desde entrada de guitarra usando modelos de IA como Magenta y Riffusion. El backend genera archivos MIDI que luego pueden usarse en un DAW o plugin de audio.

## 🎵 Descripción del Proyecto

El AI Band Backend es el motor central de un sistema inteligente de creación musical que:

- **Analiza entrada de guitarra** para detectar acordes, tempo y tonalidad musical
- **Genera líneas de bajo complementarias** que siguen la progresión de acordes
- **Crea patrones de batería dinámicos** que coinciden con el estilo musical
- **Genera archivos MIDI profesionales** listos para integración con DAW
- **Proporciona una base** para generación musical en tiempo real y desarrollo de plugins

### Cómo Funciona

```
Entrada de Guitarra → Detección de Acordes → Generación IA → Salida MIDI
     ↓                    ↓                    ↓            ↓
Audio/MIDI → Acordes + Tempo → Bajo + Batería → archivos .mid
```

El pipeline consiste en:

1. **Detección de Acordes**: Analiza entrada musical para extraer progresiones de acordes y timing
2. **Generación IA**: Usa modelos de aprendizaje automático para generar partes de bajo y batería
3. **Exportación MIDI**: Crea archivos MIDI de alta calidad para integración con DAW

## 🚀 Características

- ✅ **Análisis de progresiones de acordes** con detección de tempo y tonalidad
- ✅ **Generación inteligente de líneas de bajo** siguiendo teoría musical
- ✅ **Creación dinámica de patrones de batería** con velocidad y timing realistas
- ✅ **Salida MIDI profesional** compatible con todos los DAWs
- 🔄 **Arquitectura extensible** para agregar más instrumentos
- 🎯 **Base lista para IA** para integración con Magenta y modelos personalizados
- 🔌 **Diseño amigable para plugins** para procesamiento en tiempo real

## 🛠️ Instalación

### Prerrequisitos

- Python 3.8 o superior
- Gestor de paquetes pip
- Entorno virtual (recomendado)

### Instrucciones de Configuración

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/sergiecode/ai-band-backend.git
   cd ai-band-backend
   ```

2. **Crear y activar un entorno virtual**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verificar instalación**
   ```bash
   cd src
   python main.py
   ```

## 🎮 Uso

### Ejemplo Básico

Ejecuta el script principal para generar pistas de bajo y batería de muestra:

```bash
cd src
python main.py
```

Esto:
- Analizará una progresión de acordes de muestra (C - Am - F - G)
- Generará una pista de bajo que sigue los acordes
- Creará un patrón de batería que complementa la progresión
- Guardará archivos MIDI en el directorio `output/`

### Salida de Ejemplo

```
🎸 AI Band Backend - Generando Música con IA
==================================================
🎵 Analizando progresión de acordes...
🎼 Tempo detectado: 120 BPM
🎹 Tonalidad detectada: C
🎸 Generando pista de bajo...
🥁 Generando pista de batería...
✅ Pista de bajo guardada: output/bass_track.mid
✅ Pista de batería guardada: output/drum_track.mid

🎉 ¡Generación del AI Band Backend completa!
📁 Revisa la carpeta 'output' para tus archivos MIDI
🎵 ¡Importa estos archivos a tu DAW para escuchar la magia!
```

### Usando en Tu Código

```python
from chord_detection import ChordDetector
from midi_generator import MidiGenerator

# Inicializar componentes
detector = ChordDetector()
generator = MidiGenerator()

# Definir progresión de acordes
chords = [
    {"chord": "C", "start_time": 0.0, "duration": 2.0},
    {"chord": "Am", "start_time": 2.0, "duration": 2.0},
    {"chord": "F", "start_time": 4.0, "duration": 2.0},
    {"chord": "G", "start_time": 6.0, "duration": 2.0},
]

# Generar pistas
bass_midi = generator.generate_bass_track(chords, tempo=120)
drum_midi = generator.generate_drum_track(chords, tempo=120)

# Guardar archivos
bass_midi.save("my_bass.mid")
drum_midi.save("my_drums.mid")
```

## 📁 Estructura del Proyecto

```
ai-band-backend/
├── src/
│   ├── main.py              # Punto de entrada principal y uso de ejemplo
│   ├── chord_detection.py   # Lógica de detección de acordes y tempo
│   ├── midi_generator.py    # Generación MIDI para bajo y batería
│   └── models/              # Modelos de IA y redes neuronales
│       └── __init__.py      # Placeholder del módulo de modelos
├── requirements.txt         # Dependencias de Python
├── README.md               # Este archivo
└── output/                 # Archivos MIDI generados (creados en la primera ejecución)
```

## 🔧 Componentes Principales

### ChordDetector (`chord_detection.py`)

Maneja análisis musical y detección de acordes:

- **`detect_tempo()`**: Analiza timing para determinar BPM
- **`detect_key()`**: Identifica tonalidad musical desde progresión de acordes
- **`detect_chords_from_audio()`**: Placeholder para análisis de audio en tiempo real
- **`extract_features_for_ai()`**: Prepara datos para entrada de modelo de IA

### MidiGenerator (`midi_generator.py`)

Genera pistas MIDI usando inteligencia musical:

- **`generate_bass_track()`**: Crea líneas de bajo siguiendo progresiones de acordes
- **`generate_drum_track()`**: Genera patrones de batería con dinámicas realistas
- **`combine_tracks()`**: Fusiona múltiples instrumentos en un solo archivo MIDI
- **`generate_ai_bass_track()`**: Placeholder para generación mejorada con IA

## 🚀 Extendiendo el Proyecto

### Agregando Nuevos Instrumentos

1. Crear métodos de generación en `MidiGenerator`
2. Definir mapeos MIDI específicos del instrumento
3. Agregar lógica musical para el nuevo instrumento
4. Actualizar pipeline principal para incluir nuevas pistas

### Integrando Modelos de IA

1. Agregar archivos de modelo a `src/models/`
2. Implementar wrappers de modelo en el módulo models
3. Actualizar generadores para usar predicciones de IA
4. Ajustar modelos con tus datos musicales

### Procesamiento en Tiempo Real

1. Implementar manejo de entrada de audio con PyAudio
2. Agregar detección de acordes en tiempo real con librosa
3. Crear salida MIDI de streaming
4. Optimizar para rendimiento de baja latencia

### Integración con Plugin DAW

1. Usar el proyecto compañero `ai-band-plugin`
2. Implementar wrapper VST/AU alrededor de este backend
3. Agregar control de parámetros en tiempo real
4. Crear interfaz de usuario intuitiva

## 🔗 Proyectos Relacionados

Este backend está diseñado para trabajar con:

- **ai-band-plugin**: Wrapper de plugin VST/AU para integración con DAW
- **ai-band-orchestrator**: Coordinación multi-instrumento y arreglos
- **ai-band-frontend**: Interfaz web para generación musical

## 🎓 Recursos Educativos

Creado por **Sergie Code** con propósitos educativos. Revisa tutoriales relacionados:

- [Canal de YouTube](https://youtube.com/@sergiecode) - Tutoriales de programación
- [Curso de Generación Musical con IA] - Profundización en IA musical
- [Fundamentos de Programación MIDI] - Entendiendo los fundamentos MIDI

## 🛣️ Hoja de Ruta

### Versión 1.0 (Actual)
- ✅ Detección básica de acordes
- ✅ Generación de bajo basada en reglas
- ✅ Patrones simples de batería
- ✅ Salida de archivos MIDI

### Versión 2.0 (Planeada)
- 🔄 Entrada de audio en tiempo real
- 🔄 Integración de modelos Magenta
- 🔄 Reconocimiento avanzado de acordes
- 🔄 Múltiples estilos musicales

### Versión 3.0 (Futuro)
- 🔄 Redes neuronales personalizadas
- 🔄 Integración de plugin en tiempo real
- 🔄 Orquestación multi-instrumento
- 🔄 Procesamiento basado en la nube

## 🤝 Contribuyendo

¡Las contribuciones son bienvenidas! Áreas donde puedes ayudar:

- Mejorar algoritmos de detección de acordes
- Agregar nuevos patrones de batería y estilos de bajo
- Integrar modelos de IA adicionales
- Optimizar rendimiento para uso en tiempo real
- Agregar soporte para más estilos musicales

## 📄 Licencia

Este proyecto es código abierto y está disponible bajo la Licencia MIT.

## 🎸 Acerca de Sergie Code

Ingeniero de software apasionado y entusiasta de la música creando herramientas de IA para músicos. Enseñando programación a través de proyectos prácticos que combinan tecnología con creatividad.

**Conéctate conmigo:**
- 📸 Instagram: https://www.instagram.com/sergiecode

- 🧑🏼‍💻 LinkedIn: https://www.linkedin.com/in/sergiecode/

- 📽️Youtube: https://www.youtube.com/@SergieCode

- 😺 Github: https://github.com/sergiecode

- 👤 Facebook: https://www.facebook.com/sergiecodeok

- 🎞️ Tiktok: https://www.tiktok.com/@sergiecode

- 🕊️Twitter: https://twitter.com/sergiecode

- 🧵Threads: https://www.threads.net/@sergiecode

- 🎵 Construyendo el futuro de la creación musical potenciada por IA

---

*Hecho con ❤️ para la comunidad de música y programación*
