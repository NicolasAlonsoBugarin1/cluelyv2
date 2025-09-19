# Crear claude_service.py
with open('claude_service.py', 'w', encoding='utf-8') as f:
    f.write('''"""
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
            base_suggestion += "\\n\\n💡 Tip: Pregunta por el presupuesto aprobado para entender el alcance real."
        elif 'timeline' in context_lower:
            base_suggestion += "\\n\\n⏰ Sugerencia: Confirma fechas críticas y dependencias."
        
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
''')

# Crear playbook_manager.py
with open('playbook_manager.py', 'w', encoding='utf-8') as f:
    f.write('''"""
Playbook Manager - Gestor de playbooks y plantillas
"""
import json
import os
import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

class PlaybookManager:
    def __init__(self):
        self.playbooks = {}
        self.active_playbook = None
        self.load_default_playbooks()
    
    def load_default_playbooks(self):
        """Cargar playbooks por defecto"""
        self.playbooks = {
            'interview': {
                'name': 'Entrevista de Trabajo',
                'context': 'interview',
                'prompts': {
                    'preparation': [
                        "Investiga la empresa y el puesto específico",
                        "Prepara ejemplos usando metodología STAR",
                        "Ten listos 3-5 preguntas inteligentes para el entrevistador"
                    ],
                    'common_questions': [
                        "Cuéntame sobre ti → Enfócate en experiencia relevante (2-3 min)",
                        "¿Por qué quieres trabajar aquí? → Conecta valores personales con empresa",
                        "¿Cuáles son tus fortalezas? → Da ejemplos específicos",
                        "¿Y tus debilidades? → Muestra autoconocimiento y crecimiento"
                    ],
                    'technical_questions': [
                        "Para preguntas técnicas, piensa en voz alta",
                        "Si no sabes algo, sé honesto pero muestra interés por aprender",
                        "Relaciona teoría con experiencia práctica"
                    ]
                },
                'tips': [
                    "Mantén contacto visual y lenguaje corporal positivo",
                    "Escucha activamente antes de responder",
                    "Haz preguntas sobre cultura y crecimiento",
                    "Envía follow-up email dentro de 24 horas"
                ]
            },
            'sales': {
                'name': 'Llamada de Ventas',
                'context': 'sales',
                'prompts': {
                    'discovery': [
                        "¿Cuál es su situación actual con [problema/área]?",
                        "¿Qué les ha motivado a buscar una solución ahora?",
                        "¿Cómo miden el éxito en este proyecto?",
                        "¿Quién más está involucrado en esta decisión?"
                    ],
                    'objection_handling': [
                        "Precio → 'Entiendo la preocupación. Veamos el ROI...'",
                        "Timing → '¿Qué podría cambiar para adelantar la decisión?'",
                        "Competencia → 'Es una buena opción. ¿Qué te falta de ellos?'",
                        "Autoridad → '¿Qué información necesita el decisor final?'"
                    ],
                    'closing': [
                        "Basado en lo que hemos hablado, ¿ves valor en esta solución?",
                        "¿Qué sería necesario para avanzar?",
                        "¿Te parece si preparamos una propuesta formal?",
                        "¿Cuál sería el timeline ideal para implementación?"
                    ]
                },
                'tips': [
                    "Escucha más de lo que hablas (regla 70/30)",
                    "Haz preguntas abiertas para entender necesidades",
                    "Conecta beneficios con problemas específicos del cliente",
                    "Siempre confirma próximos pasos antes de terminar"
                ]
            },
            'demo': {
                'name': 'Demo de Producto',
                'context': 'presentation',
                'prompts': {
                    'opening': [
                        "Agenda: '¿Les parece si comenzamos con sus prioridades?'",
                        "Contexto: '¿Pueden contarme sobre su proceso actual?'",
                        "Expectativas: '¿Qué les gustaría ver específicamente?'"
                    ],
                    'during_demo': [
                        "Relaciona cada feature con su problema específico",
                        "Pausa cada 5-7 minutos: '¿Preguntas hasta aquí?'",
                        "Usa sus datos/ejemplos cuando sea posible",
                        "Destaca diferenciadores clave vs competencia"
                    ],
                    'closing': [
                        "¿Cómo ven esta solución encajando en su proceso?",
                        "¿Qué otros stakeholders necesitan ver esto?",
                        "¿Cuáles serían los próximos pasos lógicos?",
                        "¿Hay alguna preocupación que debamos abordar?"
                    ]
                },
                'tips': [
                    "Enfócate en beneficios, no solo features",
                    "Cuenta historias de clientes similares",
                    "Maneja interrupciones con gracia",
                    "Siempre ten un backup por si falla la tecnología"
                ]
            }
        }
        
        self.active_playbook = 'interview'  # Por defecto
        logger.info(f"Cargados {len(self.playbooks)} playbooks")
    
    def get_active_playbook(self) -> Dict:
        """Obtener playbook activo"""
        return self.playbooks.get(self.active_playbook, self.playbooks['interview'])
    
    def set_active_playbook(self, playbook_name: str):
        """Establecer playbook activo"""
        if playbook_name in self.playbooks:
            self.active_playbook = playbook_name
            logger.info(f"Playbook activo cambiado a: {playbook_name}")
        else:
            logger.warning(f"Playbook '{playbook_name}' no encontrado")
    
    def get_available_playbooks(self) -> List[str]:
        """Obtener lista de playbooks disponibles"""
        return list(self.playbooks.keys())
    
    def get_playbook_prompt(self, category: str, playbook_name: str = None) -> List[str]:
        """Obtener prompts específicos de un playbook"""
        playbook = self.playbooks.get(playbook_name or self.active_playbook, {})
        return playbook.get('prompts', {}).get(category, [])
    
    def get_playbook_tips(self, playbook_name: str = None) -> List[str]:
        """Obtener tips de un playbook"""
        playbook = self.playbooks.get(playbook_name or self.active_playbook, {})
        return playbook.get('tips', [])
    
    def add_custom_playbook(self, name: str, playbook_data: Dict):
        """Añadir playbook personalizado"""
        self.playbooks[name] = playbook_data
        logger.info(f"Playbook personalizado '{name}' añadido")
    
    def save_playbooks(self, filepath: str):
        """Guardar playbooks en archivo"""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.playbooks, f, indent=2, ensure_ascii=False)
            logger.info(f"Playbooks guardados en {filepath}")
        except Exception as e:
            logger.error(f"Error guardando playbooks: {e}")
    
    def load_playbooks(self, filepath: str):
        """Cargar playbooks desde archivo"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                self.playbooks = json.load(f)
            logger.info(f"Playbooks cargados desde {filepath}")
        except Exception as e:
            logger.error(f"Error cargando playbooks: {e}")
            self.load_default_playbooks()  # Fallback a defaults
''')

print("✅ claude_service.py y playbook_manager.py creados")