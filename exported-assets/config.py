"""
Configuración de la aplicación
"""
import os
import json
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class Config:
    def __init__(self):
        self.config_file = 'config.json'
        self.load_config()

    def load_config(self):
        """Cargar configuración desde archivo"""
        default_config = {
            'app': {
                'name': 'Cluely Clone',
                'version': '1.0.0',
                'debug': True
            },
            'ui': {
                'overlay_position': 'top-right',
                'overlay_opacity': 0.9,
                'always_on_top': True,
                'hotkeys': {
                    'toggle_recording': 'ctrl+shift+c',
                    'request_suggestion': 'ctrl+shift+s',
                    'toggle_overlay': 'ctrl+shift+h'
                }
            },
            'services': {
                'asr': {
                    'use_mock': True,
                    'provider': 'whisper',
                    'language': 'es-ES'
                },
                'ocr': {
                    'use_mock': True,
                    'provider': 'tesseract',
                    'capture_interval': 2
                },
                'claude': {
                    'use_mock': True,
                    'model': 'claude-3-sonnet',
                    'api_key': None
                }
            },
            'privacy': {
                'store_transcripts': False,
                'encrypt_data': True,
                'auto_delete_after_hours': 24
            }
        }

        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                # Merge con default config
                self.config = self._merge_configs(default_config, loaded_config)
            else:
                self.config = default_config
                self.save_config()

        except Exception as e:
            logger.error(f"Error cargando configuración: {e}")
            self.config = default_config

    def _merge_configs(self, default: Dict, loaded: Dict) -> Dict:
        """Merge configuraciones recursivamente"""
        result = default.copy()
        for key, value in loaded.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_configs(result[key], value)
            else:
                result[key] = value
        return result

    def save_config(self):
        """Guardar configuración actual"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            logger.info("Configuración guardada")
        except Exception as e:
            logger.error(f"Error guardando configuración: {e}")

    def get(self, key_path: str, default=None):
        """Obtener valor de configuración usando dot notation"""
        keys = key_path.split('.')
        value = self.config

        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default

        return value

    def set(self, key_path: str, value: Any):
        """Establecer valor de configuración usando dot notation"""
        keys = key_path.split('.')
        config_ref = self.config

        for key in keys[:-1]:
            if key not in config_ref:
                config_ref[key] = {}
            config_ref = config_ref[key]

        config_ref[keys[-1]] = value
        self.save_config()

    def is_debug_mode(self) -> bool:
        """Verificar si está en modo debug"""
        return self.get('app.debug', False)

    def get_hotkey(self, action: str) -> str:
        """Obtener hotkey para una acción"""
        return self.get(f'ui.hotkeys.{action}', '')

    def is_mock_mode(self, service: str) -> bool:
        """Verificar si un servicio está en modo mock"""
        return self.get(f'services.{service}.use_mock', True)
