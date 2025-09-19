# Crear config.py y archivos de configuración
with open('config.py', 'w', encoding='utf-8') as f:
    f.write('''"""
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
''')

# Crear requirements.txt
with open('requirements.txt', 'w', encoding='utf-8') as f:
    f.write('''# Cluely Clone Requirements
PyQt5==5.15.9
keyboard==0.13.5
asyncio
threading
logging
json
time
random
typing
platform

# Opcional para servicios reales (descomentar cuando necesites)
# openai-whisper  # Para ASR real
# pytesseract     # Para OCR real  
# anthropic       # Para Claude API real
# Pillow          # Para manejo de imágenes
# pyautogui       # Para captura de pantalla avanzada
''')

# Crear archivo de configuración de ejemplo
with open('config.env.example', 'w', encoding='utf-8') as f:
    f.write('''# Configuración de APIs - Renombrar a config.env
CLAUDE_API_KEY=tu_clave_de_claude_aqui
OPENAI_API_KEY=tu_clave_de_openai_aqui
GOOGLE_VISION_API_KEY=tu_clave_de_google_vision_aqui

# Configuración de servicios
USE_REAL_ASR=false
USE_REAL_OCR=false
USE_REAL_CLAUDE=false

# Configuración de logging
LOG_LEVEL=INFO
DEBUG_MODE=true
''')

# Crear run_demo.py
with open('run_demo.py', 'w', encoding='utf-8') as f:
    f.write('''#!/usr/bin/env python3
"""
Script para ejecutar Cluely Clone en modo demo
"""
import sys
import os

def check_requirements():
    """Verificar que las dependencias estén instaladas"""
    try:
        import PyQt5
        import keyboard
        print("✅ Dependencias verificadas")
        return True
    except ImportError as e:
        print(f"❌ Falta dependencia: {e}")
        print("Instala con: pip install -r requirements.txt")
        return False

def main():
    print("🚀 Iniciando Cluely Clone en modo DEMO")
    print("=" * 50)
    
    if not check_requirements():
        sys.exit(1)
    
    print("📋 Hotkeys disponibles:")
    print("  Ctrl+Shift+C: Activar/desactivar grabación")
    print("  Ctrl+Shift+S: Solicitar sugerencia")
    print("  Ctrl+Shift+H: Mostrar/ocultar overlay")
    print()
    print("🎯 Modo DEMO activo - Usando datos sintéticos")
    print("💡 Para activar servicios reales, configura APIs en config.env")
    print()
    
    # Importar y ejecutar app principal
    from app import main as app_main
    app_main()

if __name__ == "__main__":
    main()
''')

# Crear README.md
with open('README.md', 'w', encoding='utf-8') as f:
    f.write('''# 🤖 Cluely Clone - AI Meeting Assistant

Asistente de IA en tiempo real para reuniones, entrevistas y presentaciones. Réplica completa de Cluely con overlay invisible, transcripción en vivo y sugerencias contextuales.

## ✨ Características

- **Overlay Invisible**: Ventana flotante que no aparece en screen-share
- **Hotkeys Globales**: Control total mediante atajos de teclado
- **Transcripción en Tiempo Real**: ASR con mocks inteligentes y soporte para Whisper
- **OCR de Pantalla**: Lee texto de aplicaciones (Zoom, Gmail, PowerPoint, etc.)
- **Sugerencias Contextuales**: IA que analiza audio + pantalla para coaching en vivo
- **Playbooks Personalizables**: Plantillas para entrevistas, ventas, demos y pitches
- **Modo Demo**: Funciona inmediatamente sin configuración

## 🚀 Instalación Rápida

```bash
# 1. Clonar o descargar archivos
# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Ejecutar en modo demo
python run_demo.py
```

## 🎮 Uso

### Hotkeys
- **Ctrl+Shift+C**: Activar/desactivar grabación
- **Ctrl+Shift+S**: Solicitar sugerencia inmediata  
- **Ctrl+Shift+H**: Mostrar/ocultar overlay

### Playbooks Incluidos
- **Entrevistas**: Preguntas técnicas y respuestas STAR
- **Ventas**: Manejo de objeciones y técnicas de cierre
- **Demos**: Scripts de presentación y Q&A
- **VC Pitch**: Estructura para presentar a inversores

## ⚙️ Configuración Avanzada

### APIs Reales
1. Copiar `config.env.example` a `config.env`
2. Añadir claves de API:
   ```env
   CLAUDE_API_KEY=tu_clave_aqui
   USE_REAL_CLAUDE=true
   ```

### Servicios Soportados
- **Claude**: Sugerencias contextuales y análisis
- **Whisper**: Transcripción local de alta calidad
- **Google Vision**: OCR preciso para lectura de pantalla
- **Zoom/Meet/Teams**: Integraciones nativas (roadmap)

## 📁 Estructura del Proyecto

```
cluely-clone/
├── app.py              # Aplicación principal
├── overlay.py          # Ventana flotante invisible
├── asr_service.py      # Servicio de transcripción
├── ocr_service.py      # Servicio de OCR
├── claude_service.py   # Servicio de IA
├── playbook_manager.py # Gestor de plantillas
├── config.py          # Sistema de configuración
├── run_demo.py        # Script de demostración
└── requirements.txt   # Dependencias
```

## 🔒 Privacidad

- **Procesamiento Local**: ASR y OCR pueden ejecutarse offline
- **Datos Cifrados**: Transcripciones almacenadas de forma segura
- **Auto-eliminación**: Limpieza automática después de 24h
- **Modo Ético**: Banner opcional para transparencia en reuniones

## 🛣️ Roadmap

- [x] MVP funcional con overlay invisible
- [x] Playbooks inteligentes por contexto
- [x] Sistema de configuración flexible
- [ ] Integración con APIs reales (Claude, Whisper, Google Vision)
- [ ] Plugins para Zoom/Meet/Teams
- [ ] Analytics post-llamada
- [ ] Modo Enterprise con SSO

## 📞 Soporte

El software incluye:
- Documentación completa en código
- Logs detallados para debugging  
- Modo demo sin dependencias externas
- Configuración modular por servicios

## 📄 Licencia

Código abierto para uso personal y comercial.

---

**¡Listo para usar!** Ejecuta `python run_demo.py` y comienza a recibir coaching de IA en tiempo real.
''')

print("✅ Todos los archivos creados exitosamente!")
print("\n📁 Archivos del proyecto:")
print("- app.py (aplicación principal)")
print("- overlay.py (ventana flotante)")
print("- asr_service.py (transcripción)")
print("- ocr_service.py (lectura de pantalla)")
print("- claude_service.py (IA sugerencias)")
print("- playbook_manager.py (plantillas)")
print("- config.py (configuración)")
print("- requirements.txt (dependencias)")
print("- run_demo.py (script de inicio)")
print("- README.md (documentación)")
print("- config.env.example (configuración de ejemplo)")

print("\n🚀 Para ejecutar:")
print("1. pip install -r requirements.txt")
print("2. python run_demo.py")