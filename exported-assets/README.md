# 🤖 Cluely Clone - AI Meeting Assistant

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
