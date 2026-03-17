<p align="center">
  <img src="https://raw.githubusercontent.com/joaqmunoz/Monitor-Sistema-IA/main/src/resources/icon.ico" width="120" alt="Monitor Logic Logo">
  <h1 align="center">Monitor de Sistema IA</h1>
  <p align="center">
    Un monitor de recursos de escritorio <b>moderno, local y de alto rendimiento</b>.
    <br>
    <i>Hecho en Python, Qt y C++ (PySide6)</i>
  </p>
</p>

---

##  Características Principales

Este proyecto fue estructurado bajo un stack profesional diseñado para ofrecer monitoreo **offline, privado y veloz** a un nivel competitivo con aplicaciones integradas de Windows 11.

-  **Diseño Claymorphism / Glassmorphism:** Interfaz ultra-moderna (QSS personalizado), tarjetas flotantes y sombras elegantes a 60 FPS aceleradas por hardware.
-  **Rendimiento <3% de CPU:** A diferencia de apps basadas en Electron o WebViews (como Flet/Tauri), está programado con `QThreads` asíncronos y OpenGL nativo, consumiendo menos de 100 MB RAM y evitando el *freeze* de la UI.
-  **Motor de Base de Datos (SQLite WAL):** Sistema de guardado y *Batch Inserts* en ráfaga para mantener el histórico de tu consumo por días, preservando la vida útil operativa del cristal SSD.
-  **Game Overlay Inyectado:** Contiene una ventana global inteligente transparente (`Ctrl+Shift+M`) que flota sobre tus juegos de pantalla completa (DirectX/Vulkan) informando temperaturas sin robar el mouse ni lag.
-  **Sistema Inteligente Offline:** Módulo de alerta (ej. *Matar tareas si CPU > 95%*) y Sistema Experto que analiza las métricas de tu semana reportando tips para agilizar tu Windows sin enviar datos a la nube.
-  **Exportación Avanzada:** Exporta tablas completas de datos hacia .CSV, tableros dinámicos en HTML y completos reportes ejecutivos en .PDF.

---

##  Tecnologías Utilizadas

- **Framework Gráfico:** PySide6 (`Qt for Python`)
- **Renderizado de Charts:** PyQtGraph
- **Interactividad OS y Sensores:** PSUtil, WMI (Windows Native Subsystem)
- **Persistencia y Base de Datos:** SQLite3 Asíncrono
- **Exportación:** Pandas, CSV, ReportLab
- **Empaquetado:** PyInstaller, Inno Setup 6

---

##  Cómo Empezar (Modo Desarrollador)

Para ejecutar el monitor tú mismo desde el código fuente o realizar modificaciones:

### 1. Requisitos
Necesitas tener instalado **Python 3.9+** en Windows 10 u 11.

### 2. Clonar el repositorio
```bash
git clone https://github.com/joaqmunoz/Monitor-Sistema-IA.git
cd Monitor-Sistema-IA
```

### 3. Crear entorno virtual e instalar módulos
Crea tu entorno aislado y prepáralo:
```bash
python -m venv .venv

# Activar en CMD/Powershell
.venv\Scripts\activate

# Instalar los requerimientos C++ y librerías
pip install -r requirements.txt
```

### 4. Ejecutar
```bash
python src/main.py
```

---

##  Compilación y Distribución (Modo Producción)

Si quieres entregar la aplicación como un solo instalador sin requerir instalar Python nunca más:

### Paso 1: Generar código máquina
Dentro de tu entorno virtual, corre el script automatizado:
```bash
python build.py
```
> Esto generará una versión independiente de ultra alta velocidad (Flag: `--onedir`) en la carpeta `/dist/MonitorSistema` con el ícono empaquetado.

### Paso 2: Generar el instalador .EXE
1. Descarga e instala [Inno Setup 6](https://jrsoftware.org/isdl.php).
2. Abre el archivo localizado en `installer\setup.iss`.
3. Presiona el botón verde de **"Compile"**.
4. ¡Lista! Tu instalador final, `MonitorSistema-Setup-v2.exe` estará esperándote en la carpeta local `/installer/Output/`. Ya puedes repartirlo; instala accesos al Menú Win como cualquier otra app.

---

##  ROADMAP (Funcionalidades en desarrollo)

- [x] Motor Multi-Hilo con WMI y Base de Datos Asíncrona  
- [x] Dashboard Moderno Estilo "Claymorphism"  
- [x] Overlay Flotante Transparente y Exportadores (PDF/CSV) 
- [ ] Sistema de control de Luces RGB desde el propio monitor
- [ ] Plugin opcional: Transmisor Flask (para ver consumos en un teléfono en la misma red Wi-Fi).

---
<p align="center">Hecho por JoaqMuñoz. <br> </p>
