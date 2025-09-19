# Crear todos los archivos del proyecto Cluely Clone
import os

# Crear el archivo principal - app.py
with open('app.py', 'w', encoding='utf-8') as f:
    f.write('''"""
Cluely Clone - AI Meeting Assistant
Aplicación de escritorio que proporciona asistencia de IA en tiempo real durante reuniones
"""
import sys
import asyncio
import threading
import logging
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtCore import QTimer, pyqtSignal, QObject
from PyQt5.QtGui import QIcon
import keyboard
from config import Config
from overlay import OverlayWindow
from asr_service import ASRService
from ocr_service import OCRService
from claude_service import ClaudeService
from playbook_manager import PlaybookManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CluelyApp(QObject):
    def __init__(self):
        super().__init__()
        self.config = Config()
        self.overlay = None
        self.asr_service = ASRService()
        self.ocr_service = OCRService()
        self.claude_service = ClaudeService()
        self.playbook_manager = PlaybookManager()
        
        # Estado de la aplicación
        self.is_recording = False
        self.current_context = ""
        self.session_notes = []
        
        # Timer para actualizaciones periódicas
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_context)
        self.update_timer.start(2000)  # Actualizar cada 2 segundos
        
    def initialize(self):
        """Inicializar todos los componentes"""
        try:
            # Crear overlay invisible
            self.overlay = OverlayWindow()
            self.overlay.suggestion_requested.connect(self.handle_suggestion_request)
            
            # Configurar hotkeys
            self.setup_hotkeys()
            
            # Configurar system tray
            self.setup_system_tray()
            
            logger.info("Aplicación inicializada correctamente")
            return True
            
        except Exception as e:
            logger.error(f"Error inicializando aplicación: {e}")
            return False
    
    def setup_hotkeys(self):
        """Configurar atajos de teclado globales"""
        try:
            # Ctrl+Shift+C: Activar/desactivar grabación
            keyboard.add_hotkey('ctrl+shift+c', self.toggle_recording)
            
            # Ctrl+Shift+S: Solicitar sugerencia inmediata
            keyboard.add_hotkey('ctrl+shift+s', self.request_suggestion)
            
            # Ctrl+Shift+H: Mostrar/ocultar overlay
            keyboard.add_hotkey('ctrl+shift+h', self.toggle_overlay)
            
            logger.info("Hotkeys configurados")
            
        except Exception as e:
            logger.error(f"Error configurando hotkeys: {e}")
    
    def setup_system_tray(self):
        """Configurar icono en system tray"""
        if not QSystemTrayIcon.isSystemTrayAvailable():
            logger.warning("System tray no disponible")
            return
            
        # Crear menú
        menu = QMenu()
        
        toggle_action = QAction("Activar/Desactivar", None)
        toggle_action.triggered.connect(self.toggle_recording)
        menu.addAction(toggle_action)
        
        settings_action = QAction("Configuración", None)
        settings_action.triggered.connect(self.show_settings)
        menu.addAction(settings_action)
        
        quit_action = QAction("Salir", None)
        quit_action.triggered.connect(self.quit_app)
        menu.addAction(quit_action)
        
        # Crear system tray icon
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setContextMenu(menu)
        self.tray_icon.show()
    
    def toggle_recording(self):
        """Activar/desactivar grabación de audio"""
        if self.is_recording:
            self.stop_recording()
        else:
            self.start_recording()
    
    def start_recording(self):
        """Iniciar grabación y procesamiento"""
        try:
            self.asr_service.start_recording()
            self.is_recording = True
            self.overlay.set_status("Grabando...")
            logger.info("Grabación iniciada")
            
        except Exception as e:
            logger.error(f"Error iniciando grabación: {e}")
    
    def stop_recording(self):
        """Detener grabación"""
        try:
            self.asr_service.stop_recording()
            self.is_recording = False
            self.overlay.set_status("Inactivo")
            logger.info("Grabación detenida")
            
        except Exception as e:
            logger.error(f"Error deteniendo grabación: {e}")
    
    def update_context(self):
        """Actualizar contexto de pantalla periódicamente"""
        if not self.is_recording:
            return
            
        try:
            # Capturar texto de pantalla
            screen_text = self.ocr_service.capture_screen_text()
            
            # Obtener transcripción de audio reciente
            audio_text = self.asr_service.get_recent_transcript()
            
            # Combinar contextos
            self.current_context = f"Pantalla: {screen_text}\\nAudio: {audio_text}"
            
            # Generar sugerencia automática si hay cambios significativos
            if self.should_generate_suggestion():
                self.generate_suggestion()
                
        except Exception as e:
            logger.error(f"Error actualizando contexto: {e}")
    
    def should_generate_suggestion(self):
        """Determinar si se debe generar una nueva sugerencia"""
        # Lógica simple: si hay nueva transcripción o cambios en pantalla
        return len(self.current_context.strip()) > 50
    
    def request_suggestion(self):
        """Solicitar sugerencia inmediata"""
        self.generate_suggestion()
    
    def generate_suggestion(self):
        """Generar sugerencia basada en el contexto actual"""
        try:
            if not self.current_context:
                return
                
            # Obtener playbook activo
            active_playbook = self.playbook_manager.get_active_playbook()
            
            # Generar sugerencia con Claude
            suggestion = self.claude_service.generate_suggestion(
                context=self.current_context,
                playbook=active_playbook
            )
            
            if suggestion:
                self.overlay.show_suggestion(suggestion)
                self.session_notes.append({
                    'timestamp': self.get_timestamp(),
                    'context': self.current_context,
                    'suggestion': suggestion
                })
                
        except Exception as e:
            logger.error(f"Error generando sugerencia: {e}")
    
    def handle_suggestion_request(self, request_type):
        """Manejar solicitudes del overlay"""
        if request_type == "new_suggestion":
            self.generate_suggestion()
        elif request_type == "save_note":
            self.save_current_note()
    
    def toggle_overlay(self):
        """Mostrar/ocultar overlay"""
        if self.overlay:
            if self.overlay.isVisible():
                self.overlay.hide()
            else:
                self.overlay.show()
    
    def show_settings(self):
        """Mostrar ventana de configuración"""
        # TODO: Implementar ventana de configuración
        logger.info("Mostrando configuración...")
    
    def save_current_note(self):
        """Guardar nota actual"""
        try:
            # TODO: Implementar guardado de notas
            logger.info("Nota guardada")
        except Exception as e:
            logger.error(f"Error guardando nota: {e}")
    
    def get_timestamp(self):
        """Obtener timestamp actual"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def quit_app(self):
        """Cerrar aplicación"""
        self.stop_recording()
        QApplication.quit()

def main():
    """Función principal"""
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)  # No cerrar al cerrar ventanas
    
    # Crear e inicializar aplicación
    cluely_app = CluelyApp()
    
    if not cluely_app.initialize():
        logger.error("Error inicializando aplicación")
        sys.exit(1)
    
    logger.info("Cluely Clone iniciado exitosamente")
    logger.info("Hotkeys disponibles:")
    logger.info("  Ctrl+Shift+C: Activar/desactivar grabación")
    logger.info("  Ctrl+Shift+S: Solicitar sugerencia")
    logger.info("  Ctrl+Shift+H: Mostrar/ocultar overlay")
    
    # Ejecutar aplicación
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
''')

print("✅ app.py creado")