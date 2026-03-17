import sys
import os

# Agregamos src al PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PySide6.QtWidgets import QApplication
from ui.app import ResourceMonitorApp
from core.database import db

def main():
    from PySide6.QtGui import QIcon

    app = QApplication(sys.argv)
    app.setApplicationName("MonitorSistema")
    
    # Agregar y setear el nuevo Icono de App
    icon_path = os.path.join(os.path.dirname(__file__), 'resources', 'icon.ico')
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
    
    # Inicializar Base de Datos SQLite WAL
    # (El guardado ocurrirá al inyectar datos del collector_watcher, 
    # pero aquí está a nivel de bootstrap)
    print(f"Base de datos operando en: {db.db_path}")

    # Mostrar la interfaz principal estilo Clay
    window = ResourceMonitorApp()
    window.show()

    # Iniciar Event Loop principal sin bloqueo
    exit_code = app.exec()
    
    # Limpiar recursos locales al cerrar
    db.close()
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
