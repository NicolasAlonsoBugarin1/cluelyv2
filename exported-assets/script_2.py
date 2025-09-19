# Crear los servicios restantes
# asr_service.py
with open('asr_service.py', 'w', encoding='utf-8') as f:
    f.write('''"""
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
''')

# ocr_service.py
with open('ocr_service.py', 'w', encoding='utf-8') as f:
    f.write('''"""
OCR Service - Servicio de reconocimiento óptico de caracteres
Captura y lee texto de la pantalla en tiempo real
"""
import time
import random
import logging
from typing import Optional, Dict, List

logger = logging.getLogger(__name__)

class OCRService:
    def __init__(self, use_mock=True):
        self.use_mock = use_mock
        self.last_capture_time = 0
        self.capture_interval = 2  # segundos
        self.last_screen_text = ""
        
        # Mock data simulando diferentes tipos de pantallas
        self.mock_screen_scenarios = {
            'zoom_meeting': [
                "Participantes: Juan, María, Carlos, Ana",
                "Reunión: Revisión Proyecto Q3",
                "Agenda: 1. Status 2. Presupuesto 3. Timeline",
                "Chat: ¿Pueden activar cámara?",
                "Compartiendo pantalla: Presentación.pptx"
            ],
            'email': [
                "De: cliente@empresa.com",
                "Asunto: Propuesta comercial",
                "Hola, queremos agendar una reunión",
                "Adjunto: RFP_2025.pdf",
                "Necesitamos respuesta antes del viernes"
            ]
        }
        
        self.current_scenario = 'zoom_meeting'
        self.scenario_rotation = 0
        
    def capture_screen_text(self) -> str:
        """Capturar texto de la pantalla actual"""
        current_time = time.time()
        
        # Rate limiting
        if current_time - self.last_capture_time < self.capture_interval:
            return self.last_screen_text
            
        self.last_capture_time = current_time
        
        if self.use_mock:
            text = self._mock_screen_capture()
        else:
            text = self._real_screen_capture()
            
        self.last_screen_text = text
        return text
    
    def _mock_screen_capture(self) -> str:
        """Simular captura de pantalla para demo"""
        # Rotar entre escenarios
        scenarios = list(self.mock_screen_scenarios.keys())
        scenario = scenarios[self.scenario_rotation % len(scenarios)]
        
        # Obtener texto del escenario
        scenario_texts = self.mock_screen_scenarios[scenario]
        
        # Simular cambios graduales en la pantalla
        num_lines = random.randint(2, len(scenario_texts))
        selected_lines = scenario_texts[:num_lines]
        
        screen_text = "\\n".join(selected_lines)
        
        # Ocasionalmente cambiar escenario
        if random.random() < 0.1:  # 10% probabilidad
            self.scenario_rotation += 1
            logger.info(f"OCR Mock: Cambiando a escenario '{scenarios[self.scenario_rotation % len(scenarios)]}'")
        
        logger.debug(f"OCR Mock [{scenario}]: {len(screen_text)} caracteres capturados")
        return screen_text
    
    def _real_screen_capture(self) -> str:
        """Captura real de pantalla (requiere configuración)"""
        try:
            # TODO: Implementar con pytesseract o API externa
            logger.warning("OCR real no configurado - usando mock")
            return self._mock_screen_capture()
            
        except Exception as e:
            logger.error(f"Error en OCR real: {e}")
            return ""
''')

print("✅ asr_service.py y ocr_service.py creados")