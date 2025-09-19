"""
Overlay Window - Ventana flotante invisible para sugerencias
"""
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTextEdit, QFrame, QApplication
from PyQt5.QtCore import Qt, pyqtSignal, QTimer, QPropertyAnimation, QRect
from PyQt5.QtGui import QFont, QPalette, QColor
import platform

class OverlayWindow(QWidget):
    suggestion_requested = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setup_window()
        self.setup_ui()
        self.setup_animations()
        self.is_minimized = False

    def setup_window(self):
        """Configurar ventana para ser overlay invisible"""
        # Configuración básica de ventana
        self.setWindowTitle("Cluely Assistant")
        self.setFixedSize(350, 500)

        # Flags para hacer la ventana flotante e invisible en screen share
        flags = (Qt.WindowStaysOnTopHint | 
                Qt.FramelessWindowHint | 
                Qt.Tool)

        if platform.system() == "Darwin":  # macOS
            flags |= Qt.WindowDoesNotAcceptFocus
        elif platform.system() == "Windows":
            flags |= Qt.WindowTransparentForInput

        self.setWindowFlags(flags)

        # Posicionar en esquina superior derecha
        from PyQt5.QtWidgets import QDesktopWidget
        desktop = QDesktopWidget()
        screen = desktop.screenGeometry()
        self.move(screen.width() - self.width() - 20, 20)

        # Estilo transparente
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(30, 30, 30, 240);
                border-radius: 10px;
                color: white;
            }
            QLabel {
                background-color: transparent;
                padding: 5px;
            }
            QPushButton {
                background-color: rgba(70, 130, 180, 200);
                border: none;
                padding: 8px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(100, 160, 210, 255);
            }
            QPushButton:pressed {
                background-color: rgba(50, 100, 150, 255);
            }
            QTextEdit {
                background-color: rgba(50, 50, 50, 200);
                border: 1px solid rgba(100, 100, 100, 100);
                border-radius: 5px;
                padding: 10px;
                font-size: 12px;
            }
        """)

    def setup_ui(self):
        """Configurar interfaz de usuario"""
        layout = QVBoxLayout()

        # Header con status
        header_layout = QHBoxLayout()

        self.status_label = QLabel("Inactivo")
        self.status_label.setFont(QFont("Arial", 10, QFont.Bold))

        # Botón minimizar/expandir
        self.minimize_btn = QPushButton("−")
        self.minimize_btn.setFixedSize(25, 25)
        self.minimize_btn.clicked.connect(self.toggle_minimize)

        # Botón cerrar
        close_btn = QPushButton("×")
        close_btn.setFixedSize(25, 25)
        close_btn.clicked.connect(self.hide)

        header_layout.addWidget(QLabel("🤖 Cluely"))
        header_layout.addWidget(self.status_label)
        header_layout.addStretch()
        header_layout.addWidget(self.minimize_btn)
        header_layout.addWidget(close_btn)

        layout.addLayout(header_layout)

        # Separador
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("color: rgba(100, 100, 100, 100);")
        layout.addWidget(line)

        # Área de sugerencias
        self.suggestion_area = QTextEdit()
        self.suggestion_area.setPlaceholderText("Las sugerencias aparecerán aquí...")
        self.suggestion_area.setMaximumHeight(200)
        layout.addWidget(self.suggestion_area)

        # Botones de acción
        button_layout = QHBoxLayout()

        self.new_suggestion_btn = QPushButton("Nueva Sugerencia")
        self.new_suggestion_btn.clicked.connect(lambda: self.suggestion_requested.emit("new_suggestion"))

        self.copy_btn = QPushButton("Copiar")
        self.copy_btn.clicked.connect(self.copy_suggestion)

        button_layout.addWidget(self.new_suggestion_btn)
        button_layout.addWidget(self.copy_btn)

        layout.addLayout(button_layout)

        # Área de notas rápidas
        layout.addWidget(QLabel("Notas Rápidas:"))
        self.notes_area = QTextEdit()
        self.notes_area.setPlaceholderText("Escribe notas rápidas aquí...")
        self.notes_area.setMaximumHeight(100)
        layout.addWidget(self.notes_area)

        # Botón guardar notas
        save_btn = QPushButton("Guardar Notas")
        save_btn.clicked.connect(lambda: self.suggestion_requested.emit("save_note"))
        layout.addWidget(save_btn)

        self.setLayout(layout)

    def setup_animations(self):
        """Configurar animaciones"""
        self.fade_animation = QPropertyAnimation(self, b"windowOpacity")
        self.fade_animation.setDuration(300)

        self.slide_animation = QPropertyAnimation(self, b"geometry")
        self.slide_animation.setDuration(300)

    def show_suggestion(self, suggestion):
        """Mostrar nueva sugerencia con animación"""
        self.suggestion_area.setText(suggestion)

        # Animación de resaltado
        self.flash_overlay()

        # Auto-scroll al final
        cursor = self.suggestion_area.textCursor()
        cursor.movePosition(cursor.End)
        self.suggestion_area.setTextCursor(cursor)

    def flash_overlay(self):
        """Efecto de flash para nueva sugerencia"""
        original_style = self.styleSheet()
        flash_style = original_style.replace(
            "background-color: rgba(30, 30, 30, 240)",
            "background-color: rgba(70, 130, 180, 240)"
        )

        self.setStyleSheet(flash_style)

        # Volver al estilo original después de 200ms
        QTimer.singleShot(200, lambda: self.setStyleSheet(original_style))

    def copy_suggestion(self):
        """Copiar sugerencia al clipboard"""
        text = self.suggestion_area.toPlainText()
        if text:
            clipboard = QApplication.clipboard()
            clipboard.setText(text)

            # Feedback visual
            original_text = self.copy_btn.text()
            self.copy_btn.setText("¡Copiado!")
            QTimer.singleShot(1000, lambda: self.copy_btn.setText(original_text))

    def toggle_minimize(self):
        """Minimizar/expandir overlay"""
        if self.is_minimized:
            self.expand_overlay()
        else:
            self.minimize_overlay()

    def minimize_overlay(self):
        """Minimizar overlay"""
        self.slide_animation.setStartValue(self.geometry())
        self.slide_animation.setEndValue(QRect(
            self.x(), self.y(), self.width(), 40
        ))
        self.slide_animation.start()

        self.minimize_btn.setText("+")
        self.is_minimized = True

        # Ocultar contenido excepto header
        for i in range(1, self.layout().count()):
            item = self.layout().itemAt(i)
            if item.widget():
                item.widget().hide()

    def expand_overlay(self):
        """Expandir overlay"""
        self.slide_animation.setStartValue(self.geometry())
        self.slide_animation.setEndValue(QRect(
            self.x(), self.y(), self.width(), 500
        ))
        self.slide_animation.start()

        self.minimize_btn.setText("−")
        self.is_minimized = False

        # Mostrar contenido
        for i in range(1, self.layout().count()):
            item = self.layout().itemAt(i)
            if item.widget():
                item.widget().show()

    def set_status(self, status):
        """Actualizar status del overlay"""
        self.status_label.setText(status)

        # Cambiar color según status
        if status == "Grabando...":
            self.status_label.setStyleSheet("color: #ff6b6b;")
        elif status == "Procesando...":
            self.status_label.setStyleSheet("color: #feca57;")
        elif status == "Listo":
            self.status_label.setStyleSheet("color: #48dbfb;")
        else:
            self.status_label.setStyleSheet("color: white;")

    def mousePressEvent(self, event):
        """Permitir arrastrar ventana"""
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        """Mover ventana al arrastrar"""
        if event.buttons() == Qt.LeftButton and hasattr(self, 'drag_position'):
            self.move(event.globalPos() - self.drag_position)
            event.accept()

    def enterEvent(self, event):
        """Mostrar overlay al pasar mouse"""
        self.fade_animation.setStartValue(self.windowOpacity())
        self.fade_animation.setEndValue(1.0)
        self.fade_animation.start()

    def leaveEvent(self, event):
        """Atenuar overlay al quitar mouse"""
        if not self.is_minimized:
            self.fade_animation.setStartValue(self.windowOpacity())
            self.fade_animation.setEndValue(0.7)
            self.fade_animation.start()
