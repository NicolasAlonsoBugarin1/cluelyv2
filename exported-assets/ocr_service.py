"""
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

        screen_text = "\n".join(selected_lines)

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
