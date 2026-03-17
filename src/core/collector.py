import time
import psutil
from PySide6.QtCore import QThread, Signal
import traceback
try:
    from utils.hardware_detection import HardwareDetector
except ImportError:
    pass

class SystemMonitorWorker(QThread):
    """
    Hilo de recolección en background. 
    Evita que el hilo principal (GUI) se bloquee mientras se obtienen métricas.
    """
    metrics_updated = Signal(dict)
    
    def __init__(self, interval=2):
        super().__init__()
        self.interval = interval
        self.running = True

        self.last_net_io = psutil.net_io_counters()
        self.last_disk_io = psutil.disk_io_counters()
        self.boot_time = psutil.boot_time()
        
        try:
            self.hw_detector = HardwareDetector()
        except:
            self.hw_detector = None

    def run(self):
        while self.running:
            try:
                metrics = self.collect_all_metrics()
                self.metrics_updated.emit(metrics)
            except Exception as e:
                print(f"Error recolectando métricas: {e}")
                traceback.print_exc()
            
            time.sleep(self.interval)

    def collect_all_metrics(self):
        # CPU
        cpu_percent = psutil.cpu_percent(interval=None) 
        cpu_per_core = psutil.cpu_percent(interval=None, percpu=True)
        cpu_freq = psutil.cpu_freq()
        
        # RAM
        mem = psutil.virtual_memory()
        swap = psutil.swap_memory()

        # Network I/O
        net_io = psutil.net_io_counters()
        net_sent = (net_io.bytes_sent - self.last_net_io.bytes_sent) / self.interval
        net_recv = (net_io.bytes_recv - self.last_net_io.bytes_recv) / self.interval
        self.last_net_io = net_io

        # Disk I/O
        disk_io = psutil.disk_io_counters()
        disk_read = (disk_io.read_bytes - self.last_disk_io.read_bytes) / self.interval if disk_io else 0
        disk_write = (disk_io.write_bytes - self.last_disk_io.write_bytes) / self.interval if disk_io else 0
        self.last_disk_io = disk_io
        
        disks_usage = []
        for p in psutil.disk_partitions():
            if 'cdrom' in p.opts or p.fstype == '':
                continue
            try:
                usage = psutil.disk_usage(p.mountpoint)
                disks_usage.append({
                    'device': p.device,
                    'total': usage.total,
                    'used': usage.used,
                    'free': usage.free,
                    'percent': usage.percent
                })
            except:
                continue

        # Batería
        battery = psutil.sensors_battery()

        # Hardware y GPU
        gpu_metrics = {'name': 'Integrada', 'usage': 0, 'temperature': 0}
        temps = [0]
        fans = []
        if self.hw_detector:
            gpu_metrics = self.hw_detector.get_gpu_metrics()
            temps = self.hw_detector.get_cpu_temperatures()
            fans = self.hw_detector.get_fan_speeds()

        # Empaquetamos todo
        data = {
            'cpu': {
                'percent': cpu_percent,
                'per_core': cpu_per_core,
                'freq': cpu_freq.current if cpu_freq else 0,
                'temperature': temps[0] if temps else 0
            },
            'memory': {
                'used': mem.used,
                'total': mem.total,
                'percent': mem.percent,
                'swap_percent': swap.percent
            },
            'network': {
                'sent_speed': net_sent,
                'recv_speed': net_recv,
                'connections': len(psutil.net_connections(kind='inet'))
            },
            'disk': {
                'read_speed': disk_read,
                'write_speed': disk_write,
                'partitions': disks_usage
            },
            'gpu': gpu_metrics,
            'battery': {
                'percent': battery.percent if battery else 100,
                'power_plugged': battery.power_plugged if battery else True
            },
            'uptime': time.time() - self.boot_time
        }
        return data

    def stop(self):
        self.running = False
        self.wait()
