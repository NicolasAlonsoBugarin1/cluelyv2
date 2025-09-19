#!/usr/bin/env python3
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
