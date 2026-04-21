# Monitor de Sistema IA

## Descripción

Monitor de Sistema IA es una aplicación de escritorio desarrollada en Python con Qt (PySide6), diseñada para el monitoreo en tiempo real de recursos del sistema con alto rendimiento, bajo consumo y procesamiento completamente local.

El sistema permite visualizar métricas críticas como uso de CPU, memoria y procesos activos, incorporando mecanismos de análisis, almacenamiento histórico y generación de reportes. Está orientado a entornos donde se requiere monitoreo eficiente sin dependencia de servicios en la nube.

---

## Características Principales

- Interfaz gráfica moderna desarrollada con Qt (PySide6), optimizada para rendimiento y fluidez
- Consumo eficiente de recursos: menor a 3% de CPU y menos de 100 MB de memoria RAM
- Monitoreo en tiempo real de CPU, memoria y procesos
- Sistema de almacenamiento con SQLite en modo WAL para registro histórico eficiente
- Procesamiento concurrente mediante QThreads para evitar bloqueos de interfaz
- Sistema de alertas configurable (ej: terminación automática de procesos con alto consumo)
- Análisis local de métricas para sugerencias de optimización del sistema
- Exportación de datos a formatos CSV, HTML y PDF
- Overlay flotante compatible con aplicaciones en pantalla completa (DirectX/Vulkan)

---

## Tecnologías Utilizadas

- Python 3.9+
- PySide6 (Qt for Python)
- PyQtGraph
- SQLite3 (modo WAL)
- PSUtil
- WMI (Windows Management Instrumentation)
- Pandas
- ReportLab
- PyInstaller
- Inno Setup

---

## Arquitectura

El sistema está diseñado bajo un enfoque modular con separación de responsabilidades:

- Captura de datos del sistema mediante PSUtil y WMI
- Procesamiento concurrente utilizando QThreads
- Persistencia en base de datos SQLite optimizada para escritura continua
- Capa de visualización basada en Qt con renderizado eficiente
- Módulo de exportación para generación de reportes

---

## Instalación (Modo Desarrollo)

### Requisitos

- Python 3.9 o superior
- Sistema operativo Windows 10 o 11

### Clonar repositorio

```bash
git clone https://github.com/joaqmunoz/Monitor-Sistema-IA.git
cd Monitor-Sistema-IA
Crear entorno virtual e instalar dependencias
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
Ejecutar aplicación
python src/main.py
Compilación y Distribución
Generar ejecutable
python build.py

Esto generará una versión empaquetada en la carpeta:

/dist/MonitorSistema
Crear instalador
Instalar Inno Setup
Abrir el archivo installer/setup.iss
Compilar el instalador

El ejecutable final se generará en:

/installer/Output/MonitorSistema-Setup-v2.exe
Casos de Uso
Monitoreo de rendimiento en estaciones de trabajo
Diagnóstico de consumo excesivo de recursos
Supervisión de procesos en segundo plano
Generación de reportes para análisis técnico
Uso en entornos donde se requiere privacidad (sin envío de datos externos)
Roadmap
Control de iluminación RGB desde la aplicación
Módulo de transmisión de datos vía red local (Flask)
Mejoras en análisis predictivo de rendimiento
Optimización adicional del sistema de alertas
Notas
La aplicación funciona completamente offline
No transmite datos a servicios externos
Diseñada para entornos de uso personal y técnico
Autor

Joaquín Muñoz
