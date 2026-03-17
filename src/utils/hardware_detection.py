import os
import wmi
import psutil
import platform
import subprocess

class HardwareDetector:
    """
    Detección de Hardware nativa para Windows.
    Utiliza WMI y PSUtil para obtener información de sensores.
    En un entorno de producción estricto puede requerir LibreHardwareMonitor,
    pero esta implementación es 100% nativa sin DLLs externas y con fallbacks seguros.
    """
    def __init__(self):
        self._wmi = wmi.WMI()
        self._wmi_root = wmi.WMI(namespace="root\\wmi")
        
    def get_gpu_metrics(self):
        """Intenta obtener métricas de GPU nativamente"""
        metrics = {'name': 'Unknown GPU', 'usage': 0.0, 'memory_total': 0, 'memory_used': 0, 'temperature': 0}
        try:
            # Detección básica de nombre vía WMI
            for gpu in self._wmi.Win32_VideoController():
                metrics['name'] = gpu.Name
                break
            
            # Nota: Obtener el uso en tiempo real de GPU en Windows nativo sin NVML
            # o librehardwaremonitor es limitado. Usaremos contadores de rendimiento.
            # Aquí pondríamos la lógica de PDH (Performance Data Helper) o pynvml si estuviera.
        except Exception as e:
            pass
        return metrics

    def get_cpu_temperatures(self):
        """Obtiene la temperatura del CPU utilizando WMI ThermalZone"""
        temps = []
        try:
            # Requiere permisos de admin a veces, o soporte específico de placa base
            thermal_zones = self._wmi_root.MSAcpi_ThermalZoneTemperature()
            for zone in thermal_zones:
                # WMI devuelve temperaturas en décimas de grado Kelvin
                celcius = (zone.CurrentTemperature / 10.0) - 273.15
                if celcius > 0:
                    temps.append(round(celcius, 1))
        except Exception:
            pass
        return temps if temps else [0.0]

    def get_fan_speeds(self):
        """Obtiene las RPM de los ventiladores"""
        fans = []
        try:
            for fan in self._wmi.Win32_Fan():
                if hasattr(fan, 'DesiredSpeed'):
                    fans.append({'name': fan.Name or 'Fan', 'rpm': fan.DesiredSpeed})
        except Exception:
            pass
        return fans
