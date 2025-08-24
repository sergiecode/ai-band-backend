"""
Módulo de Detección de Acordes
Parte del AI Band Backend por Sergie Code

Este módulo maneja la detección de acordes y tempo desde entrada de guitarra.
Actualmente implementa análisis básico de acordes, con placeholders para
procesamiento de audio en tiempo real y reconocimiento de acordes basado en IA.

PROPÓSITO DEL ARCHIVO:
- Analizar progresiones de acordes musicales
- Detectar tempo (velocidad) de la música
- Determinar la tonalidad musical
- Extraer características para modelos de IA
- Preparar datos musicales para generación de acompañamiento

COMPONENTES PRINCIPALES:
- ChordDetector: Clase principal que maneja todo el análisis musical
- Algoritmos de detección de tempo basados en duración de acordes
- Sistema de detección de tonalidad usando mapeo de acordes
- Extractor de características para futuros modelos de IA

FUTURAS EXPANSIONES:
- Integración con librosa para análisis de audio real
- Modelos de IA (TensorFlow/Magenta) para reconocimiento avanzado
- Procesamiento en tiempo real de señales de guitarra
"""

import numpy as np
from typing import List, Dict, Any  # Para tipado de datos - mejora legibilidad del código


class ChordDetector:
    """
    Maneja la detección de acordes y análisis musical desde entrada de guitarra.
    
    Esta clase proporciona métodos para:
    - Detectar acordes desde entrada de audio (placeholder para implementación real)
    - Analizar tempo desde progresiones de acordes
    - Determinar tonalidad musical desde secuencias de acordes
    - Extraer características musicales para entrada de modelo de IA
    
    EXPLICACIÓN PEDAGÓGICA:
    Un detector de acordes es como un "oído musical artificial" que puede:
    1. Escuchar música y identificar qué acordes se están tocando
    2. Determinar qué tan rápida es la música (tempo)
    3. Identificar en qué tonalidad está la canción
    4. Preparar esta información para que una IA genere acompañamiento
    """
    
    def __init__(self):
        """
        Inicializar el detector de acordes con configuraciones por defecto.
        
        CONFIGURACIONES DE AUDIO:
        - sample_rate: Frecuencia de muestreo (44100 Hz es estándar CD)
        - hop_length: Tamaño del salto entre análisis (512 samples)
        - frame_length: Tamaño de ventana para análisis (2048 samples)
        
        MAPEO MUSICAL:
        - chord_key_map: Diccionario que relaciona acordes con posibles tonalidades
        
        ¿POR QUÉ ESTOS VALORES?
        - 44100 Hz captura todo el rango audible humano
        - 512/2048 samples dan buena resolución temporal y frecuencial
        - El mapeo acorde-tonalidad se basa en teoría musical occidental
        """
        # Configuraciones de procesamiento de audio
        self.sample_rate = 44100    # Muestras por segundo (calidad CD)
        self.hop_length = 512       # Salto entre ventanas de análisis
        self.frame_length = 2048    # Tamaño de ventana de análisis
        
        # Mapeos comunes de acorde-a-tonalidad basados en teoría musical
        # Cada acorde puede pertenecer a múltiples tonalidades
        self.chord_key_map = {
            'C': ['C', 'F', 'G'],      # Do mayor puede estar en Do, Fa o Sol mayor
            'Am': ['C', 'F', 'G'],     # La menor también puede estar en estas tonalidades
            'F': ['F', 'Bb', 'C'],     # Fa mayor puede estar en Fa, Si bemol o Do mayor
            'G': ['C', 'G', 'D'],      # Sol mayor puede estar en Do, Sol o Re mayor
            'Dm': ['F', 'Bb', 'C'],    # Re menor puede estar en Fa, Si bemol o Do mayor
            'Em': ['C', 'G', 'D'],     # Mi menor puede estar en Do, Sol o Re mayor
        }
    
    def detect_chords_from_audio(self, audio_file_path: str) -> List[Dict[str, Any]]:
        """
        Detectar acordes desde un archivo de audio.
        
        Args:
            audio_file_path: Ruta al archivo de audio
            
        Returns:
            Lista de diccionarios de acordes con información de timing
            
        Note:
            Esta es una implementación placeholder. En un escenario real,
            usarías librosa + modelos de aprendizaje automático o
            integración con el reconocimiento de acordes de Magenta.
            
        EXPLICACIÓN PEDAGÓGICA:
        Esta función representa el "santo grial" del análisis musical automático.
        En la versión completa:
        1. Cargaría un archivo de audio (.wav, .mp3, etc.)
        2. Analizaría las frecuencias presentes
        3. Identificaría patrones que corresponden a acordes específicos
        4. Determinaría cuándo empieza y termina cada acorde
        5. Devolvería una lista cronológica de todos los acordes detectados
        
        TECNOLOGÍAS NECESARIAS:
        - librosa: Para análisis espectral de audio
        - tensorflow/magenta: Para modelos de IA pre-entrenados
        - chromagram: Para análisis de contenido harmónico
        """
        # TODO: Implementar detección real de acordes usando:
        # - librosa para análisis de audio
        # - tensorflow/magenta para reconocimiento de acordes basado en IA
        # - análisis de cromograma para detección de acordes
        
        # Placeholder: devolver progresión de acordes de muestra
        # En la implementación real, esto vendría del análisis del archivo de audio
        return [
            {"chord": "C", "start_time": 0.0, "duration": 2.0, "confidence": 0.95},
            {"chord": "Am", "start_time": 2.0, "duration": 2.0, "confidence": 0.90},
            {"chord": "F", "start_time": 4.0, "duration": 2.0, "confidence": 0.88},
            {"chord": "G", "start_time": 6.0, "duration": 2.0, "confidence": 0.92},
        ]
    
    def detect_tempo(self, chord_progression: List[Dict[str, Any]]) -> int:
        """
        Detectar tempo desde timing de progresión de acordes.
        
        Args:
            chord_progression: Lista de diccionarios de acordes con timing
            
        Returns:
            Tempo detectado en BPM (beats per minute - latidos por minuto)
            
        EXPLICACIÓN PEDAGÓGICA:
        El tempo es la velocidad de la música, medida en BPM.
        Esta función funciona de la siguiente manera:
        
        1. ANÁLISIS DE DURACIÓN: Examina cuánto dura cada acorde
        2. CÁLCULO DE PROMEDIO: Obtiene la duración promedio de los acordes
        3. CONVERSIÓN A BPM: Usa matemáticas para convertir duración a velocidad
        4. NORMALIZACIÓN: Ajusta a valores de BPM comunes en música
        
        LÓGICA MATEMÁTICA:
        - Si los acordes duran 2 segundos cada uno
        - Y asumimos 4 beats por acorde (compás 4/4)
        - Entonces: 4 beats / 2 segundos = 2 beats por segundo
        - 2 beats/segundo × 60 segundos = 120 BPM
        """
        # Verificar que tenemos suficientes acordes para análisis
        if len(chord_progression) < 2:
            return 120  # Tempo por defecto si no hay suficientes datos
        
        # PASO 1: Extraer duraciones válidas de los acordes
        # Manejamos posibles errores en los datos de entrada
        durations = []
        for chord in chord_progression:
            # Verificar que existe la clave 'duration' y es un número válido
            if "duration" in chord and isinstance(chord["duration"], (int, float)):
                if chord["duration"] > 0:  # Solo duraciones positivas
                    durations.append(chord["duration"])
        
        # Si no encontramos duraciones válidas, usar tempo por defecto
        if not durations:
            return 120  # Valor seguro por defecto
        
        # PASO 2: Calcular duración promedio de acordes
        avg_duration = sum(durations) / len(durations)
        
        # PASO 3: Estimar BPM basado en cambios de acordes
        # TEORÍA MUSICAL: Asumimos que cada acorde representa un compás o medio compás
        beats_per_chord = 4  # Asumir compás de 4/4 (muy común en música popular)
        chord_duration_minutes = avg_duration / 60  # Convertir segundos a minutos
        bpm = beats_per_chord / chord_duration_minutes  # Calcular BPM
        
        # PASO 4: Redondear a valores comunes de BPM en música
        # Lista de tempos comunes en diferentes géneros musicales
        common_bpms = [60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160]
        # Encontrar el BPM más cercano a nuestro cálculo
        return min(common_bpms, key=lambda x: abs(x - bpm))
    
    def detect_key(self, chord_progression: List[Dict[str, Any]]) -> str:
        """
        Detectar tonalidad musical desde progresión de acordes.
        
        Args:
            chord_progression: Lista de diccionarios de acordes
            
        Returns:
            Tonalidad musical detectada (ej: "C", "G", "Am")
            
        EXPLICACIÓN PEDAGÓGICA:
        La tonalidad es el "centro tonal" de una canción - la nota que se siente
        como "casa" o punto de resolución. Esta función:
        
        1. EXTRACCIÓN: Obtiene los nombres de todos los acordes
        2. MAPEO: Usa nuestro diccionario para ver qué tonalidades usan esos acordes
        3. PUNTUACIÓN: Cuenta votos para cada tonalidad posible
        4. DECISIÓN: Elige la tonalidad con más votos
        
        EJEMPLO:
        Si tenemos acordes [C, Am, F, G]:
        - C puede estar en tonalidades: C, F, G
        - Am puede estar en tonalidades: C, F, G  
        - F puede estar en tonalidades: F, Bb, C
        - G puede estar en tonalidades: C, G, D
        
        Puntuación: C=4 votos, F=3 votos, G=3 votos
        Resultado: C mayor (ganador)
        """
        # Verificar que tenemos acordes para analizar
        if not chord_progression:
            return "C"  # Tonalidad por defecto
        
        # PASO 1: Extraer nombres de acordes válidos
        chords = []
        for chord_info in chord_progression:
            # Verificar que existe la clave 'chord' y no está vacía
            if "chord" in chord_info and chord_info["chord"]:
                chords.append(chord_info["chord"])
        
        if not chords:
            return "C"  # Por defecto si no hay acordes válidos
        
        # PASO 2: Sistema de votación para detectar tonalidad
        key_scores = {}  # Diccionario para contar votos por tonalidad
        
        for chord in chords:
            # Si conocemos este acorde en nuestro mapeo
            if chord in self.chord_key_map:
                # Agregar un voto a cada tonalidad posible
                for possible_key in self.chord_key_map[chord]:
                    key_scores[possible_key] = key_scores.get(possible_key, 0) + 1
        
        # Si no pudimos mapear ningún acorde, usar por defecto
        if not key_scores:
            return "C"
        
        # PASO 3: Devolver la tonalidad con mayor puntuación
        return max(key_scores, key=key_scores.get)
    
    def analyze_chord_progression(self, chord_progression: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analizar progresión de acordes para extraer patrones musicales.
        
        Args:
            chord_progression: Lista de acordes detectados
            
        Returns:
            Diccionario con análisis completo de la progresión
            
        EXPLICACIÓN PEDAGÓGICA:
        Una progresión de acordes es la secuencia de acordes que forma la 
        armonía de una canción. Este análisis nos ayuda a entender:
        
        1. PATRONES RÍTMICOS: ¿Cada acorde dura igual tiempo?
        2. TONALIDAD: ¿En qué escala musical estamos?
        3. TEMPO: ¿Qué tan rápida es la canción?
        4. ESTRUCTURA: ¿Qué acordes se repiten más?
        
        APLICACIÓN EN IA MUSICAL:
        Esta información será usada por el generador de MIDI para:
        - Crear líneas de bajo que sigan la progresión armónica
        - Generar patrones de batería apropiados para el tempo
        - Mantener coherencia musical en toda la canción
        
        EJEMPLO DE ANÁLISIS:
        Entrada: [C, Am, F, G] con duración 1 segundo cada uno
        Salida: {
            "tonalidad": "C",
            "tempo": 120,
            "patron": "I-vi-IV-V" (progresión muy común),
            "acordes_unicos": 4,
            "duracion_total": 4.0
        }
        """
        # PASO 1: Calcular duración total de forma segura
        total_duration = 0.0
        valid_chords = []
        
        # Extraer información válida de cada acorde
        for chord in chord_progression:
            # Sumar duración si existe y es válida
            if "duration" in chord and isinstance(chord["duration"], (int, float)):
                if chord["duration"] > 0:
                    total_duration += chord["duration"]
            
            # Agregar nombre del acorde si existe y es válido
            if "chord" in chord and chord["chord"]:
                valid_chords.append(chord["chord"])
        
        # PASO 2: Crear análisis comprensivo usando nuestros métodos
        return {
            "tempo": self.detect_tempo(chord_progression),       # BPM detectado
            "key": self.detect_key(chord_progression),          # Tonalidad detectada
            "total_duration": total_duration,                   # Duración total en segundos
            "chord_count": len(chord_progression),              # Número total de acordes
            "unique_chords": len(set(valid_chords)) if valid_chords else 0,  # Acordes únicos
            "time_signature": "4/4",                            # Compás asumido (muy común)
        }
    
    def extract_features_for_ai(self, chord_progression: List[Dict[str, Any]]) -> np.ndarray:
        """
        Extraer características numéricas desde progresión de acordes para entrada de modelo de IA.
        
        Args:
            chord_progression: Lista de diccionarios de acordes
            
        Returns:
            Array NumPy con características numéricas
            
        EXPLICACIÓN PEDAGÓGICA:
        Los modelos de Inteligencia Artificial necesitan números, no texto.
        Esta función convierte información musical en vectores numéricos
        que pueden ser procesados por algoritmos de machine learning.
        
        CARACTERÍSTICAS QUE EXTRAEMOS:
        1. TEMPO: Velocidad de la canción (BPM)
        2. TONALIDAD NUMÉRICA: Convierte "C", "G", etc. a números
        3. DURACIÓN TOTAL: Longitud total de la progresión
        4. CONTADORES: Número de acordes, acordes únicos, cambios
        5. ESTADÍSTICAS: Promedios, variaciones, patrones
        
        CODIFICACIÓN DE TONALIDADES:
        C=0, C#=1, D=2, D#=3, E=4, F=5, F#=6, G=7, G#=8, A=9, A#=10, B=11
        Am=12, A#m=13, Bm=14, Cm=15, C#m=16, Dm=17, D#m=18, Em=19, Fm=20, F#m=21, Gm=22, G#m=23
        
        APLICACIÓN:
        Estas características pueden alimentar modelos de IA para:
        - Clasificar géneros musicales
        - Predecir acordes siguientes
        - Generar acompañamientos automáticos
        - Analizar complejidad harmónica
        """
        # PASO 1: Obtener análisis básico de la progresión
        analysis = self.analyze_chord_progression(chord_progression)
        
        # PASO 2: Codificar tonalidad como número
        # Mapeo de tonalidades a números para uso en ML
        key_encoding = {
            # Tonalidades mayores (0-11)
            "C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3, "E": 4, 
            "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8, "Ab": 8, "A": 9, 
            "A#": 10, "Bb": 10, "B": 11,
            # Tonalidades menores (12-23)
            "Am": 12, "A#m": 13, "Bbm": 13, "Bm": 14, "Cm": 15, "C#m": 16,
            "Dbm": 16, "Dm": 17, "D#m": 18, "Ebm": 18, "Em": 19, "Fm": 20,
            "F#m": 21, "Gbm": 21, "Gm": 22, "G#m": 23, "Abm": 23
        }
        
        # PASO 3: Extraer características numéricas
        key_num = key_encoding.get(analysis["key"], 0)  # Tonalidad como número
        tempo = analysis["tempo"]                        # BPM
        duration = analysis["total_duration"]            # Duración total
        chord_count = analysis["chord_count"]            # Número de acordes
        unique_chords = analysis["unique_chords"]        # Acordes únicos
        
        # PASO 4: Calcular características adicionales
        # Densidad harmónica: cambios de acorde por minuto
        if duration > 0:
            chord_density = (chord_count / duration) * 60  # cambios por minuto
        else:
            chord_density = 0
        
        # Diversidad harmónica: ratio de acordes únicos vs total
        if chord_count > 0:
            harmonic_diversity = unique_chords / chord_count
        else:
            harmonic_diversity = 0
        
        # PASO 5: Crear vector de características para IA
        features = np.array([
            key_num,            # [0] Tonalidad codificada
            tempo,              # [1] Tempo en BPM
            duration,           # [2] Duración total
            chord_count,        # [3] Número total de acordes
            unique_chords,      # [4] Número de acordes únicos
            chord_density,      # [5] Cambios de acorde por minuto
            harmonic_diversity  # [6] Diversidad harmónica (0-1)
        ])
        
        return features
