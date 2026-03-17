# Documentación y Análisis del Sistema Monitor de Recursos v2.0

## 1. Análisis y Selección Tecnológica

**Selección: PySide6 (Qt for Python) + `pyqtgraph`**

### Justificación:
Para cumplir con los estrictos requisitos de una aplicación profesional instalable, de alto rendimiento y capaz de proveer gráficos a más de 30 FPS en tiempo real:

- **Rendimiento UI y Gráficos (30+ FPS):** Flet consume más recursos por instanciar un motor web/Flutter, lo cual es prohibitivo para un monitor de recursos con cientos de barras e históricos. Dear PyGui es el más rápido pero su interfaz técnica dificulta recrear diseños *Glassmorphism/Clay*. PySide6 utiliza aceleración nativa C++ mediante `pyqtgraph` para gráficos ultrarrápidos, logrando los 60 FPS sin saturar la CPU.
- **Aspecto Profesional y Mockups:** Mediante Qt Style Sheets (QSS) y `QGraphicsDropShadowEffect`, PySide6 puede recrear exactamente el estilo "Clay" (esquinas suaves, colores pastel, elevaciones de tarjeta) de forma nativa en Windows.
- **Empaquetado y Distribución:** Históricamente es la solución más confiable para generar `.exe` (usando PyInstaller `--onedir` para un arranque menor a 3 segundos) y permite engancharse fácilmente con Inno Setup y APIs nativas de Windows (`ctypes`) para Overlays.

### Resolviendo el "Framework GUI en 2026":
En 2026, si bien las interfaces web son estándar, PySide6 provee el **mejor** balance para una aplicación de Monitor de Recursos por su acceso de ultra bajo nivel (procesos de SO y hardware) sin la barrera de comunicación asíncrona IPC requerida por apps web/Electron. La UI puede lucir como el mockup "ClayPhone" empleando QWidgets personalizados sin borde y con sombras integradas.

### Respuestas Técnicas Clave:
- **Arquitectura de Hilos:** Un `QThread` principal para UI. Múltiples `QRunnable` (Pool de Hilos) para recolectar datos bloqueantes (WMI, sensores I/O) y usando `Signal/Slot` de Qt para no bloquear nunca el rendering del frontend 30-60FPS. Los datos pesados se comunican por colas bloqueantes o señales directas cada 1000ms, pero la UI anima barras gradualmente a 60fps localmente.
- **Base de Datos Local (SQLite 2s escrituras):** Usar el journal mode WAL (`PRAGMA journal_mode=WAL`) reduce los bloqueos. Además, agregamos ráfagas (*Batching*) en RAM, guardando cada 5-10 recolectas en un solo `COMMIT` a disco en hilo separado (evita degradación del SSD).
- **Overlay en Tiempo Real (Juego):** PySide6 ofrece las flags  `Qt.WindowStaysOnTopHint | Qt.WindowTransparentForInput | Qt.FramelessWindowHint` asociadas y opacidades variables. Combinado con la librería `keyboard` para un global hotkey imperceptible, el overlay se superpone incluso sobre juegos sin bordes en Windows (borderless window o fullscreen optimization en W10/11).
- **Detección de Hardware Avanzado:** LibreHardwareMonitorLib.dll inyectada vía `pythonnet`. WMI nativo no siempre expone hardware reciente (ej. Ryzen/Intel Core). Para este ejemplo utilizaremos psutil y mock de WMI con fallback para asegurar *Zero dependencias externas*.
- **Empaquetado (PyInstaller):** PyInstaller usando entorno `--onedir` es vital. Si agrupamos todo en un `--onefile`, crear un `.exe` tarda hasta 7 segundos en desempaquetar las librerías QT en %TEMP% localmente cada vez que el usuario lo abre. `--onedir` compreso con Inno Setup resulta en inicio de 1 a 2 segundos garantizado.

## Roadmap de Desarrollo
Fase 1: Motor local y Capa de Datos SQLite WAL (Día 1)
Fase 2: Arquitectura QThread y Workers WMI/psutil (Día 2)
Fase 3: Desarrollo GUI PySide6 y Theme "Clay" (Día 3-4)
Fase 4: Motor de Reglas (Alertas) y Optimización (Día 5)
Fase 5: Overlay Juego y Settings (Día 6)
Fase 6: Empaquetado PyInstaller + Inno Setup (Día 7)
