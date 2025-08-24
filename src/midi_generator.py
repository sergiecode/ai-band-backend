"""
Módulo Generador MIDI
Parte del AI Band Backend por Sergie Code

Este módulo maneja la generación MIDI para pistas de bajo y batería usando modelos de IA.
Se integra con Magenta y otros frameworks de IA para generación musical inteligente.
"""

import pretty_midi
from typing import List, Dict, Any
import random


class MidiGenerator:
    """
    Genera pistas MIDI para bajo y batería basándose en progresiones de acordes.
    
    Esta clase proporciona métodos para:
    - Generar líneas de bajo que siguen progresiones de acordes
    - Crear patrones de batería que complementan el estilo musical
    - Usar modelos de IA para generación musical inteligente
    - Exportar archivos MIDI de alta calidad
    """
    
    def __init__(self):
        """
        Inicializar el generador MIDI con configuraciones por defecto.
        
        EXPLICACIÓN PEDAGÓGICA:
        El constructor prepara todas las herramientas y mapeos necesarios
        para generar música MIDI profesional. Configuramos:
        
        1. TEMPO: Velocidad por defecto (120 BPM = moderado)
        2. RESOLUCIÓN: Precisión temporal del MIDI (480 ticks = alta calidad)
        3. MAPEOS DE NOTAS: Traduce acordes a notas MIDI específicas
        4. INSTRUMENTOS: Define qué sonidos usar para bajo y batería
        
        NOTAS MIDI EXPLICADAS:
        - Los números representan teclas de piano (0-127)
        - C4 = 60 (Do central), cada octava suma/resta 12
        - Bajo usa octavas bajas (notas 20-50)
        - Batería usa canal 9 con números fijos por instrumento
        """
        # CONFIGURACIÓN TEMPORAL
        self.default_tempo = 120      # BPM por defecto (beats por minuto)
        self.ticks_per_beat = 480     # Resolución MIDI (más alto = más preciso)
        
        # MAPEOS DE NOTAS DE BAJO PARA ACORDES COMUNES
        # Cada acorde mapea a su nota fundamental en diferentes octavas
        self.chord_bass_notes = {
            'C': [36, 48],      # Do2, Do3 - Acorde de Do Mayor
            'Am': [33, 45],     # La1, La2 - Acorde de La menor  
            'F': [29, 41],      # Fa1, Fa2 - Acorde de Fa Mayor
            'G': [31, 43],      # Sol1, Sol2 - Acorde de Sol Mayor
            'Dm': [38, 50],     # Re2, Re3 - Acorde de Re menor
            'Em': [28, 40],     # Mi1, Mi2 - Acorde de Mi menor
        }
        
        # MAPEOS DE NOTAS MIDI ESTÁNDAR DE BATERÍA (General MIDI)
        # Canal 9 (índice 9) reservado para percusión en MIDI estándar
        self.drum_map = {
            'kick': 36,         # Bombo 1 (C2) - golpe grave principal
            'snare': 38,        # Caja Acústica (D2) - golpe agudo en tiempos 2 y 4
            'hihat_closed': 42, # Hi-Hat Cerrado (F#2) - ritmo constante
            'hihat_open': 46,   # Hi-Hat Abierto (A#2) - acentos especiales
            'crash': 49,        # Platillo Crash 1 (C#3) - acentos dramáticos
            'ride': 51,         # Platillo Ride 1 (D#3) - ritmo alternativo
        }
    
    def generate_bass_track(self, chord_progression: List[Dict[str, Any]], 
                          tempo: int = 120, key: str = "C") -> pretty_midi.PrettyMIDI:
        """
        Generar una pista de bajo que sigue la progresión de acordes.
        
        Args:
            chord_progression: Lista de diccionarios de acordes con timing
            tempo: Tempo en BPM (beats por minuto)
            key: Tonalidad musical (ej: "C", "Am", "G")
            
        Returns:
            Objeto PrettyMIDI conteniendo la pista de bajo generada
            
        EXPLICACIÓN PEDAGÓGICA:
        El bajo es la base armónica de cualquier canción. Esta función:
        
        1. CONFIGURACIÓN: Crea un archivo MIDI con el tempo especificado
        2. INSTRUMENTO: Selecciona el sonido de bajo eléctrico
        3. MAPEO: Convierte cada acorde a su nota fundamental
        4. TIMING: Coloca las notas en el tiempo correcto según la progresión
        5. EXPORT: Genera un archivo MIDI que cualquier DAW puede leer
        
        TEORÍA MUSICAL DEL BAJO:
        - El bajo toca principalmente la nota fundamental del acorde
        - Octavas bajas (notas MIDI 20-50) dan profundidad y peso
        - Patrones rítmicos simples mantienen la estabilidad harmónica
        - La velocidad (volume) se ajusta para naturalidad
        
        EJEMPLO:
        Acorde C durante 2 segundos → Nota MIDI 36 (C2) durante 2 segundos
        """
        # PASO 1: Crear archivo MIDI base con tempo especificado
        midi = pretty_midi.PrettyMIDI(initial_tempo=tempo)
        
        # PASO 2: Configurar instrumento de bajo
        # Usar programa 34 = Bajo Eléctrico (pick) según General MIDI
        bass_program = pretty_midi.instrument_name_to_program('Electric Bass (pick)')
        bass = pretty_midi.Instrument(program=bass_program, is_drum=False, name='Bass')
        
        # PASO 3: Procesar cada acorde de la progresión
        for chord_info in chord_progression:
            # Extraer información del acorde con valores por defecto seguros
            chord_name = chord_info.get("chord", "C")     # Nombre del acorde
            start_time = chord_info.get("start_time", 0.0) # Cuándo empezar
            duration = chord_info.get("duration", 2.0)    # Cuánto durar
            
            # VALIDACIÓN: Manejar datos inválidos o faltantes
            if not chord_name or not isinstance(chord_name, str):
                chord_name = "C"  # Usar Do Mayor como respaldo seguro
            
            # PASO 4: Mapear acorde a notas de bajo apropiadas
            if chord_name in self.chord_bass_notes:
                bass_notes = self.chord_bass_notes[chord_name]
            else:
                # Respaldo: usar Do Mayor si el acorde no está mapeado
                bass_notes = self.chord_bass_notes['C']
            
            # PASO 5: Generar patrón rítmico de bajo para este acorde
            self._add_bass_pattern(bass, bass_notes, start_time, duration, tempo)
        
        # PASO 6: Agregar el instrumento de bajo al archivo MIDI
        midi.instruments.append(bass)
        return midi
    
    def _add_bass_pattern(self, instrument: pretty_midi.Instrument, 
                         bass_notes: List[int], start_time: float, 
                         duration: float, tempo: int):
        """
        Agregar un patrón rítmico de bajo para la duración de un acorde.
        
        Args:
            instrument: Instrumento MIDI donde agregar las notas
            bass_notes: Lista de números MIDI de notas de bajo disponibles
            start_time: Tiempo de inicio en segundos
            duration: Duración total del patrón en segundos
            tempo: Tempo en BPM para calcular timing de beats
            
        EXPLICACIÓN PEDAGÓGICA:
        Los patrones de bajo en música popular siguen estructuras rítmicas
        específicas que proporcionan estabilidad y groove:
        
        1. TIEMPOS FUERTES: Nota fundamental en beats 1 y 3 (típico en 4/4)
        2. VARIACIÓN: Octavas o quintas para evitar monotonía
        3. VELOCITY: Volumen natural que simula interpretación humana
        4. DURACIÓN: Notas sostenidas vs. staccato según el estilo
        
        PATRÓN IMPLEMENTADO:
        - Beat 1: Nota fundamental (más grave y fuerte)
        - Beat 3: Octava superior o misma nota (variación tonal)
        - Velocity: 80-100 (dinámico pero controlado)
        - Duración: Notas ligeramente separadas para claridad
        """
        # Calcular duración de un beat en segundos
        beat_duration = 60.0 / tempo  # BPM a segundos por beat
        
        # PATRÓN RÍTMICO: Nota fundamental en tiempos 1 y 3 (compás 4/4)
        # Elegir entre diferentes patrones para variedad musical
        patterns = [
            # PATRÓN 1: Notas enteras - nota sostenida durante todo el acorde
            [(0, bass_notes[0], duration * 0.9)],  # 90% para evitar superposición
            
            # PATRÓN 2: Blancas - dos notas por acorde
            [(0, bass_notes[0], beat_duration * 2 * 0.9),
             (beat_duration * 2, bass_notes[0], beat_duration * 2 * 0.9)],
            
            # PATRÓN 3: Fundamental + Octava - patrón clásico de bajo
            [(0, bass_notes[0], beat_duration * 0.9),                    # Beat 1: Fundamental
             (beat_duration * 2, bass_notes[-1], beat_duration * 0.9)],  # Beat 3: Octava superior
        ]
        
        # SELECCIÓN DE PATRÓN: Elegir patrón basado en duración del acorde
        if duration >= 4 * beat_duration:
            # Acordes largos: usar patrón 3 (más activo)
            pattern = patterns[2]
        elif duration >= 2 * beat_duration:
            # Acordes medianos: usar patrón 2 (moderado)
            pattern = patterns[1]
        else:
            # Acordes cortos: usar patrón 1 (simple)
            pattern = patterns[0]
        
        # GENERACIÓN DE NOTAS: Crear objetos Note de PrettyMIDI
        for note_offset, note_pitch, note_duration in pattern:
            # Calcular tiempo absoluto de la nota
            note_start = start_time + note_offset
            note_end = note_start + note_duration
            
            # Asegurar que no excedemos la duración del acorde
            if note_start >= start_time + duration:
                break  # No agregar notas que exceden el tiempo del acorde
            
            # Ajustar final de nota si excede duración del acorde
            if note_end > start_time + duration:
                note_end = start_time + duration
            
            # VELOCITY (Volumen): Agregar variación natural
            velocity = random.randint(80, 100)  # Rango dinámico natural
            
            # Crear y agregar la nota MIDI
            note = pretty_midi.Note(
                velocity=velocity,      # Intensidad del golpe
                pitch=note_pitch,       # Altura de la nota (número MIDI)
                start=note_start,       # Inicio en segundos
                end=note_end           # Final en segundos
            )
            instrument.notes.append(note)
    
    def generate_drum_track(self, chord_progression: List[Dict[str, Any]], 
                          tempo: int = 120, duration: float = 8.0) -> pretty_midi.PrettyMIDI:
        """
        Generar una pista de batería que complementa la progresión de acordes.
        
        Args:
            chord_progression: Lista de diccionarios de acordes con información temporal
            tempo: Tempo en BPM (beats por minuto)
            duration: Duración total de la pista en segundos
            
        Returns:
            Objeto PrettyMIDI conteniendo la pista de batería completa
            
        EXPLICACIÓN PEDAGÓGICA:
        La batería es el corazón rítmico de la música. Esta función genera
        patrones de percusión que:
        
        1. ESTRUCTURA: Proporcionan la base rítmica fundamental
        2. GROOVE: Crean el "feel" o sensación de la canción
        3. ACENTOS: Marcan divisiones musicales y secciones
        4. COMPLEMENTO: Se adaptan al tempo y estilo de los acordes
        
        INSTRUMENTOS DE BATERÍA UTILIZADOS:
        - BOMBO (Kick): Beat principal, marca tiempos 1 y 3
        - CAJA (Snare): Acento en tiempos 2 y 4, da fuerza al groove
        - HI-HAT: Subdivisiones, mantiene el pulse constante
        - CRASH: Acentos dramáticos en inicios de sección
        
        PATRÓN ESTÁNDAR (4/4):
        1 + 2 + 3 + 4 +
        K   S   K   S    (K=Kick, S=Snare, +=Hi-hat)
        """
        # PASO 1: Crear archivo MIDI base
        midi = pretty_midi.PrettyMIDI(initial_tempo=tempo)
        
        # PASO 2: Configurar instrumento de batería
        # Canal 9 (is_drum=True) indica percusión en MIDI estándar
        drums = pretty_midi.Instrument(program=0, is_drum=True, name='Drums')
        
        # PASO 3: Generar patrón de batería profesional
        self._add_drum_pattern(drums, tempo, duration)
        
        # PASO 4: Agregar batería al archivo MIDI
        midi.instruments.append(drums)
        return midi
    
    def _add_drum_pattern(self, instrument: pretty_midi.Instrument, 
                         tempo: int, duration: float):
        """
        Agregar un patrón básico de batería con groove profesional.
        
        Args:
            instrument: Instrumento MIDI de batería donde agregar notas
            tempo: Tempo en BPM para calcular timing
            duration: Duración total del patrón en segundos
            
        EXPLICACIÓN PEDAGÓGICA:
        Este método crea el patrón rítmico fundamental de la batería:
        
        1. COMPÁS 4/4: División en 4 beats por compás
        2. BOMBO: Beats 1 y 3 (groove de rock/pop básico)
        3. CAJA: Beats 2 y 4 (backbeat clásico)
        4. HI-HAT: Todos los beats + subdivisiones (pulse constante)
        
        MATEMÁTICA RÍTMICA:
        - Beat = 60/BPM segundos
        - Compás = 4 beats
        - Loop continuo hasta completar duración total
        
        VELOCITY (Intensidad):
        - Bombo: 90-100 (fuerte, fundamental)
        - Caja: 95 (precisa, cortante)
        - Hi-Hat: 60-70 (constante, sutil)
        """
        # Calcular duración temporal básica
        beat_duration = 60.0 / tempo  # Segundos por beat
        current_time = 0.0            # Tiempo actual en la generación
        
        # LOOP PRINCIPAL: Generar compases hasta completar duración
        while current_time < duration:
            measure_duration = beat_duration * 4  # Duración de un compás 4/4
            
            # Verificar que no excedamos la duración total
            if current_time + measure_duration > duration:
                break
            
            # BOMBO: Beats 1 y 3 (groove fundamental)
            kick_note1 = pretty_midi.Note(
                velocity=100,                           # Fuerte y claro
                pitch=self.drum_map['kick'],           # Nota MIDI 36
                start=current_time,                    # Beat 1
                end=current_time + 0.1                 # Duración corta (staccato)
            )
            kick_note2 = pretty_midi.Note(
                velocity=90,                           # Ligeramente más suave
                pitch=self.drum_map['kick'],           # Nota MIDI 36
                start=current_time + beat_duration * 2, # Beat 3
                end=current_time + beat_duration * 2 + 0.1
            )
            instrument.notes.extend([kick_note1, kick_note2])
            
            # CAJA: Beats 2 y 4 (backbeat clásico)
            snare_note1 = pretty_midi.Note(
                velocity=95,                           # Precisa y cortante
                pitch=self.drum_map['snare'],          # Nota MIDI 38
                start=current_time + beat_duration,    # Beat 2
                end=current_time + beat_duration + 0.1
            )
            snare_note2 = pretty_midi.Note(
                velocity=95,                           # Consistente
                pitch=self.drum_map['snare'],          # Nota MIDI 38
                start=current_time + beat_duration * 3, # Beat 4
                end=current_time + beat_duration * 3 + 0.1
            )
            instrument.notes.extend([snare_note1, snare_note2])
            
            # HI-HAT: Pulse constante en cada beat (1, 2, 3, 4)
            for beat in range(4):
                hihat_note = pretty_midi.Note(
                    velocity=70,                                      # Sutil pero presente
                    pitch=self.drum_map['hihat_closed'],             # Nota MIDI 42
                    start=current_time + beat * beat_duration,       # En cada beat
                    end=current_time + beat * beat_duration + 0.05   # Muy corto (staccato)
                )
                instrument.notes.append(hihat_note)
            
            # AVANZAR al siguiente compás
            current_time += measure_duration
    
    def generate_ai_bass_track(self, chord_progression: List[Dict[str, Any]], 
                              tempo: int = 120) -> pretty_midi.PrettyMIDI:
        """
        Generar pista de bajo usando modelos de IA avanzados.
        
        Args:
            chord_progression: Lista de diccionarios de acordes con información temporal
            tempo: Tempo en BPM para la generación
            
        Returns:
            Objeto PrettyMIDI conteniendo pista de bajo generada por IA
            
        EXPLICACIÓN PEDAGÓGICA:
        Esta función representa el futuro de la generación musical automatizada.
        Los modelos de IA como Magenta de Google pueden:
        
        1. APRENDER: Entrenar con miles de canciones reales
        2. CONTEXTUALIZAR: Entender progresiones armónicas complejas
        3. CREAR: Generar líneas de bajo musicalmente coherentes
        4. ESTILIZAR: Adaptar a diferentes géneros y estilos
        
        INTEGRACIÓN CON MAGENTA:
        - MelodyRNN: Para líneas melódicas de bajo
        - PerformanceRNN: Para timing y expresión realista
        - MusicVAE: Para interpolación entre estilos
        - Piano Transformer: Para estructuras armónicas complejas
        
        IMPLEMENTACIÓN ACTUAL:
        Por ahora usamos el generador básico como respaldo,
        pero esta función está preparada para integración futura
        con modelos de IA más sofisticados.
        """
        # PLACEHOLDER: Implementación futura con modelos de IA
        # TODO: Integrar Magenta MelodyRNN o similar
        # TODO: Cargar modelo pre-entrenado
        # TODO: Convertir chord_progression a formato de entrada del modelo
        # TODO: Generar secuencia musical usando el modelo
        # TODO: Post-procesar salida del modelo a formato MIDI
        
        print("🤖 IA Bass Generation: Usando generador básico como respaldo...")
        print("💡 Tip: Integra Magenta para generación IA avanzada")
        
        # Por ahora, usar el generador básico como respaldo
        return self.generate_bass_track(chord_progression, tempo)
    
    def combine_tracks(self, bass_midi: pretty_midi.PrettyMIDI, 
                      drum_midi: pretty_midi.PrettyMIDI) -> pretty_midi.PrettyMIDI:
        """
        Combinar pistas de bajo y batería en un solo archivo MIDI.
        
        Args:
            bass_midi: MIDI de pista de bajo
            drum_midi: MIDI de pista de batería
            
        Returns:
            Archivo MIDI combinado con ambas pistas
            
        EXPLICACIÓN PEDAGÓGICA:
        Combinar múltiples pistas MIDI es esencial para crear 
        arreglos musicales completos. Esta función:
        
        1. PRESERVA: Mantiene el tempo y configuración temporal
        2. CANALES: Asigna diferentes canales MIDI a cada instrumento
        3. SINCRONIZACIÓN: Asegura que ambas pistas estén alineadas temporalmente
        4. METADATA: Conserva información de instrumentos y programa
        
        ESTRUCTURA MIDI RESULTANTE:
        - Canal 0: Bajo eléctrico (melódico)
        - Canal 9: Batería (percusión) - estándar MIDI
        - Tempo: Heredado de la pista de bajo
        - Formato: Tipo 1 MIDI (múltiples pistas sincronizadas)
        """
        # PASO 1: Crear archivo MIDI base con tempo del bajo
        if bass_midi.get_tempo_changes()[1].size > 0:
            initial_tempo = bass_midi.get_tempo_changes()[1][0]
        else:
            initial_tempo = 120  # Tempo por defecto
        
        combined = pretty_midi.PrettyMIDI(initial_tempo=initial_tempo)
        
        # PASO 2: Agregar pista de bajo (si existe)
        if bass_midi.instruments:
            bass_track = bass_midi.instruments[0]
            bass_track.name = "Bajo Eléctrico"  # Nombre descriptivo en español
            combined.instruments.append(bass_track)
        
        # PASO 3: Agregar pista de batería (si existe)
        if drum_midi.instruments:
            drum_track = drum_midi.instruments[0]
            drum_track.name = "Batería"  # Nombre descriptivo en español
            combined.instruments.append(drum_track)
        
        return combined
