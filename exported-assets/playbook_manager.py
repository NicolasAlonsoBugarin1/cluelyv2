"""
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
