import PyInstaller.__main__
import os
import shutil

print("=== Iniciando Build Automatizado ===")

# Rutas
base_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(base_dir, 'src')
main_script = os.path.join(src_dir, 'main.py')
icon_path = os.path.join(src_dir, 'resources', 'icon.ico') # Opcional si existe

# 1. Asegurar recurso base
os.makedirs(os.path.join(src_dir, 'resources'), exist_ok=True)

# 2. Configuración PyInstaller 
# Nota: --onedir se mantiene como mejor práctica para inicio rápido. 
# Si el usuario quiere un .exe único, se puede cambiar `--onedir` a `--onefile`.
pyinstaller_cmd = [
    main_script,
    '--name=MonitorSistema',
    '--windowed',                 # Ocultar consola DOS en PC
    '--icon=' + icon_path,        # ICONO OFICIAL DE LA APP
    '--noconfirm',                # Sobrescribir sin preguntar
    '--clean',                    # Limpiar caches
    '--log-level=WARN',
    '--add-data=%s;resources' % os.path.dirname(icon_path),
    '--onedir',                   # Extra rápido al iniciar (recomendado para producción instalable)
    # '--onefile',                # <- Usar esto si deseas un único .exe portable a costa de 3s de lag
]

# Agregar hooks/hidden imports
pyinstaller_cmd.extend([
    '--hidden-import=pyqtgraph',
    '--hidden-import=psutil',
    '--hidden-import=wmi',
    '--hidden-import=keyboard',
    '--collect-all=pandas'       # Req: Exportación a CSV avanzada
])

# Ejecutar
print(f"Comando PyInstaller: {' '.join(pyinstaller_cmd)}")
PyInstaller.__main__.run(pyinstaller_cmd)

print("\n✅ Compilación Exitosa.")
print("El ejecutable está en la carpeta 'dist/MonitorSistema'")
print("Ahora puedes ejecutar el script de Inno Setup (installer/setup.iss) para empaquetarlo.")
