import sqlite3
import os
import csv
from datetime import datetime, timedelta

class MetricsDatabase:
    """ CRUD Completo con SQLite y WAL """
    def __init__(self):
        self.appdata_dir = os.path.join(os.getenv('APPDATA'), 'MonitorSistema')
        os.makedirs(self.appdata_dir, exist_ok=True)
        self.db_path = os.path.join(self.appdata_dir, 'metrics.db')
        
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        
        self.cursor.execute("PRAGMA journal_mode = WAL;") 
        self.cursor.execute("PRAGMA synchronous = NORMAL;") 
        self.cursor.execute("PRAGMA temp_store = MEMORY;")
        
        self.init_db()
        self._buffer = []
        self._max_buffer = 15

    def init_db(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS metrics_snapshot (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            cpu_avg REAL,
            ram_used INTEGER,
            ram_total INTEGER,
            disk_read_speed REAL,
            disk_write_speed REAL,
            net_sent_speed REAL,
            net_recv_speed REAL,
            gpu_usage REAL,
            battery_level REAL,
            cpu_temp REAL
        )
        ''')
        # Índices optimizados para consultas por fecha
        self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_timestamp ON metrics_snapshot(timestamp);")
        self.conn.commit()
    
    def insert_snapshot(self, data: dict):
        cpu = data.get('cpu', {})
        mem = data.get('memory', {})
        disk = data.get('disk', {})
        net = data.get('network', {})
        gpu = data.get('gpu', {})
        bat = data.get('battery', {})

        self._buffer.append((
            datetime.now(),
            cpu.get('percent', 0),
            mem.get('used', 0),
            mem.get('total', 0),
            disk.get('read_speed', 0),
            disk.get('write_speed', 0),
            net.get('sent_speed', 0),
            net.get('recv_speed', 0),
            gpu.get('usage', 0),
            bat.get('percent', 0),
            cpu.get('temperature', 0)
        ))
        
        if len(self._buffer) >= self._max_buffer:
            self._flush_buffer()
            
    def _flush_buffer(self):
        if not self._buffer: return
        query = '''
        INSERT INTO metrics_snapshot 
        (timestamp, cpu_avg, ram_used, ram_total, disk_read_speed, disk_write_speed, 
         net_sent_speed, net_recv_speed, gpu_usage, battery_level, cpu_temp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        try:
            self.cursor.executemany(query, self._buffer)
            self.conn.commit()
            self._buffer.clear()
        except Exception as e:
            print(f"Error escribiendo en BD: {e}")

    def get_history(self, hours=24):
        """ Consultar datos históricos """
        self._flush_buffer()
        time_limit = datetime.now() - timedelta(hours=hours)
        self.cursor.execute('''
            SELECT timestamp, cpu_avg, ram_used, ram_total, net_sent_speed, net_recv_speed 
            FROM metrics_snapshot 
            WHERE timestamp >= ? ORDER BY timestamp ASC
        ''', (time_limit,))
        return self.cursor.fetchall()

    def clean_old_records(self, days=7):
        time_limit = datetime.now() - timedelta(days=days)
        self.cursor.execute("DELETE FROM metrics_snapshot WHERE timestamp < ?", (time_limit,))
        self.conn.commit()

    def get_stats(self, period="24h"):
        hours = 24 if period == "24h" else 168
        time_limit = datetime.now() - timedelta(hours=hours)
        self.cursor.execute('''
            SELECT MAX(cpu_avg), AVG(cpu_avg), MAX(ram_used), AVG(ram_used)
            FROM metrics_snapshot WHERE timestamp >= ?
        ''', (time_limit,))
        return self.cursor.fetchone()

    def export_to_csv(self, path):
        self._flush_buffer()
        self.cursor.execute("SELECT * FROM metrics_snapshot")
        rows = self.cursor.fetchall()
        cols = [desc[0] for desc in self.cursor.description]
        with open(path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(cols)
            writer.writerows(rows)

    def close(self):
        self._flush_buffer()
        self.conn.close()

db = MetricsDatabase()
