"""
ASR Service - Servicio de reconocimiento de voz
Incluye mock para testing y interfaz para servicios reales
"""
import asyncio
import threading
import queue
import time
import random
from typing import Optional, List
import logging

logger = logging.getLogger(__name__)

class ASRService:
    def __init__(self, use_mock=True):
        self.use_mock = use_mock
        self.is_recording = False
        self.transcript_queue = queue.Queue()
        self.current_transcript = ""
        self.session_transcript = []

        # Mock data para demo
        self.mock_phrases = [
            "Hola, ¿cómo estás?",
            "Me parece una buena idea",
            "¿Podrías explicar más sobre ese punto?",
            "Estoy de acuerdo con esa propuesta",
            "Necesitamos revisar los números",
            "¿Cuál sería el siguiente paso?",
            "Perfecto, procedamos así",
            "Tengo algunas dudas sobre el presupuesto",
            "¿Qué opinas del timeline?",
            "Creo que deberíamos considerarlo"
        ]

    def start_recording(self):
        """Iniciar grabación de audio"""
        if self.is_recording:
            return

        self.is_recording = True
        logger.info("ASR: Iniciando grabación")

        if self.use_mock:
            self._start_mock_recording()
        else:
            self._start_real_recording()

    def stop_recording(self):
        """Detener grabación"""
        self.is_recording = False
        logger.info("ASR: Deteniendo grabación")

    def _start_mock_recording(self):
        """Simular transcripción para demo"""
        def mock_worker():
            while self.is_recording:
                # Simular delay natural
                time.sleep(random.uniform(3, 8))

                if not self.is_recording:
                    break

                # Generar frase mock
                phrase = random.choice(self.mock_phrases)
                timestamp = time.time()

                # Añadir a transcript
                transcript_entry = {
                    'timestamp': timestamp,
                    'text': phrase,
                    'confidence': random.uniform(0.8, 0.95)
                }

                self.session_transcript.append(transcript_entry)
                self.current_transcript = phrase

                logger.info(f"ASR Mock: '{phrase}'")

        # Ejecutar en thread separado
        thread = threading.Thread(target=mock_worker, daemon=True)
        thread.start()

    def _start_real_recording(self):
        """Iniciar grabación real (requiere configuración)"""
        # TODO: Implementar con Whisper local o API externa
        logger.warning("ASR real no configurado - usando mock")
        self._start_mock_recording()

    def get_recent_transcript(self, seconds=30) -> str:
        """Obtener transcripción reciente"""
        if not self.session_transcript:
            return ""

        current_time = time.time()
        recent_entries = [
            entry for entry in self.session_transcript
            if current_time - entry['timestamp'] <= seconds
        ]

        if not recent_entries:
            return ""

        # Combinar texto reciente
        texts = [entry['text'] for entry in recent_entries]
        return " ".join(texts)

    def get_full_transcript(self) -> List[dict]:
        """Obtener transcripción completa de la sesión"""
        return self.session_transcript.copy()

    def clear_transcript(self):
        """Limpiar transcripción actual"""
        self.session_transcript.clear()
        self.current_transcript = ""
        logger.info("ASR: Transcripción limpiada")
