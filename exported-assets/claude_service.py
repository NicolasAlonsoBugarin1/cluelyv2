"""
Claude Service - Servicio de IA para generar sugerencias
"""
import random
import time
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)

class ClaudeService:
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.use_mock = api_key is None

        # Sugerencias mock por contexto
        self.mock_suggestions = {
            'meeting': [
                "Podrías preguntar: '¿Cuáles son los próximos pasos concretos?'",
                "Sugiere hacer un recap de los puntos clave antes de continuar",
                "Es buen momento para confirmar el timeline y responsables",
                "Considera proponer una fecha para la próxima revisión"
            ],
            'sales': [
                "Enfócate en el ROI: '¿Cómo medirían el éxito de esta solución?'",
                "Pregunta por el proceso de decisión: '¿Quién más participa en esta decisión?'",
                "Aborda objeciones: 'Entiendo la preocupación por el precio, veamos el valor...'",
                "Cierra con siguiente paso: '¿Te parece si preparamos una propuesta formal?'"
            ],
            'interview': [
                "Da ejemplos específicos con método STAR (Situación, Tarea, Acción, Resultado)",
                "Conecta tu experiencia con los requisitos del puesto",
                "Prepara preguntas sobre cultura de empresa y crecimiento",
                "Muestra interés genuino: '¿Cuáles son los mayores desafíos del equipo?'"
            ],
            'presentation': [
                "Haz una pausa y pregunta: '¿Alguna duda hasta aquí?'",
                "Conecta con la audiencia: '¿Alguien ha vivido una situación similar?'",
                "Resume los puntos clave antes de pasar al siguiente tema",
                "Usa storytelling para hacer más memorable el mensaje"
            ]
        }

    def generate_suggestion(self, context: str, playbook: Dict = None) -> str:
        """Generar sugerencia basada en contexto"""
        if self.use_mock:
            return self._generate_mock_suggestion(context, playbook)
        else:
            return self._generate_real_suggestion(context, playbook)

    def _generate_mock_suggestion(self, context: str, playbook: Dict = None) -> str:
        """Generar sugerencia mock inteligente"""
        # Detectar tipo de contexto
        context_lower = context.lower()

        if 'zoom' in context_lower or 'reunión' in context_lower:
            suggestion_type = 'meeting'
        elif 'precio' in context_lower or 'propuesta' in context_lower:
            suggestion_type = 'sales'
        elif 'experiencia' in context_lower or 'fortalezas' in context_lower:
            suggestion_type = 'interview'
        elif 'slide' in context_lower or 'presentación' in context_lower:
            suggestion_type = 'presentation'
        else:
            suggestion_type = random.choice(['meeting', 'sales', 'interview', 'presentation'])

        # Obtener sugerencia del tipo detectado
        suggestions = self.mock_suggestions.get(suggestion_type, self.mock_suggestions['meeting'])
        base_suggestion = random.choice(suggestions)

        # Personalizar según playbook si existe
        if playbook and 'context' in playbook:
            playbook_context = playbook['context']
            base_suggestion = f"[{playbook_context}] {base_suggestion}"

        # Añadir contexto específico
        if 'presupuesto' in context_lower:
            base_suggestion += "\n\n💡 Tip: Pregunta por el presupuesto aprobado para entender el alcance real."
        elif 'timeline' in context_lower:
            base_suggestion += "\n\n⏰ Sugerencia: Confirma fechas críticas y dependencias."

        logger.info(f"Claude Mock: Generando sugerencia tipo '{suggestion_type}'")
        return base_suggestion

    def _generate_real_suggestion(self, context: str, playbook: Dict = None) -> str:
        """Generar sugerencia real con Claude API"""
        try:
            # TODO: Implementar llamada real a Claude API
            logger.warning("Claude API no configurada - usando mock")
            return self._generate_mock_suggestion(context, playbook)

        except Exception as e:
            logger.error(f"Error llamando Claude API: {e}")
            return "Error generando sugerencia. Revisa la configuración de la API."

    def analyze_sentiment(self, text: str) -> Dict:
        """Analizar sentimiento del texto"""
        if self.use_mock:
            return {
                'sentiment': random.choice(['positive', 'neutral', 'negative']),
                'confidence': random.uniform(0.7, 0.95),
                'emotions': random.choice([
                    ['curious', 'engaged'],
                    ['concerned', 'cautious'],
                    ['excited', 'optimistic']
                ])
            }
        else:
            # TODO: Implementar análisis real
            return {'sentiment': 'neutral', 'confidence': 0.5}

    def extract_action_items(self, text: str) -> list:
        """Extraer elementos de acción del texto"""
        if self.use_mock:
            mock_actions = [
                "Enviar propuesta antes del viernes",
                "Agendar reunión de seguimiento",
                "Revisar presupuesto con el equipo",
                "Preparar demo personalizado",
                "Contactar referencias"
            ]
            return random.sample(mock_actions, random.randint(1, 3))
        else:
            # TODO: Implementar extracción real
            return []

    def generate_meeting_summary(self, transcript: list) -> str:
        """Generar resumen de reunión"""
        if self.use_mock:
            return """
📋 **Resumen de Reunión**

**Participantes:** Juan, María, Carlos, Ana
**Temas principales:**
• Revisión del proyecto Q3
• Análisis de presupuesto
• Definición de próximos pasos

**Decisiones:**
• Proceder con la propuesta original
• Aumentar presupuesto en 15%
• Fecha límite: 30 de septiembre

**Acciones:**
• Juan: Revisar contratos (viernes)
• María: Coordinar con legal (lunes)
• Carlos: Preparar presentación final (miércoles)
            """
        else:
            # TODO: Implementar resumen real
            return "Resumen no disponible - configurar Claude API"

    def configure_api(self, api_key: str):
        """Configurar API de Claude"""
        self.api_key = api_key
        self.use_mock = False
        logger.info("Claude API configurada correctamente")
