import os
import psutil
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QProgressBar, QPushButton, QStackedWidget, QTableWidget, 
    QTableWidgetItem, QHeaderView, QFileDialog, QMessageBox
)
from PySide6.QtCore import Qt
import pyqtgraph as pg

from core.collector import SystemMonitorWorker
from core.database import db
from core.alerts import AlertEngine
from core.optimizer import SystemOptimizer
from core.game_overlay import GameOverlay
from ui.styles import CLAY_THEME
from ui.widgets import ClayCard, SmoothChart
from utils.exporters import DataExporter

class ResourceMonitorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Monitor Claymorphism Profesional")
        self.setMinimumSize(480, 850)
        self.setStyleSheet(CLAY_THEME)
        
        # UI Engines
        self.alert_engine = AlertEngine()
        self.optimizer = SystemOptimizer(db)
        self.overlay = GameOverlay()
        
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        self._init_ui()
        self._start_collector()

    def _init_ui(self):
        self.central_widget = QWidget()
        self.central_widget.setObjectName("MainWindow")
        self.setCentralWidget(self.central_widget)
        
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(25, 40, 25, 40)
        self.main_layout.setSpacing(15)

        # ====== HEADER ======
        header = QLabel("ClayMonitor v2")
        header.setAlignment(Qt.AlignCenter)
        header.setProperty("class", "TitleLight")
        self.main_layout.addWidget(header)
        
        # ====== STATE STACK ======
        self.stack = QStackedWidget()
        self.main_layout.addWidget(self.stack)
        
        # Pestañas
        self.page_dashboard = QWidget()
        self.page_processes = QWidget()
        self.page_history = QWidget()
        
        self._build_dashboard(self.page_dashboard)
        self._build_processes(self.page_processes)
        self._build_history(self.page_history)
        
        self.stack.addWidget(self.page_dashboard)
        self.stack.addWidget(self.page_processes)
        self.stack.addWidget(self.page_history)

        # ====== NAVIGATION BAR ======
        nav_layout = QHBoxLayout()
        self.btn_dash = QPushButton("Dashboard")
        self.btn_proc = QPushButton("Procesos")
        self.btn_hist = QPushButton("Ajustes")
        
        self.btn_dash.setCheckable(True)
        self.btn_proc.setCheckable(True)
        self.btn_hist.setCheckable(True)
        self.btn_dash.setChecked(True)
        
        self.btn_dash.clicked.connect(lambda: self._switch_tab(0, self.btn_dash))
        self.btn_proc.clicked.connect(lambda: self._switch_tab(1, self.btn_proc))
        self.btn_hist.clicked.connect(lambda: self._switch_tab(2, self.btn_hist))

        nav_layout.addWidget(self.btn_dash)
        nav_layout.addWidget(self.btn_proc)
        nav_layout.addWidget(self.btn_hist)
        self.main_layout.addLayout(nav_layout)
        
        # ====== FOOTER ======
        self.lbl_status = QLabel("Actualizando: Esperando datos...")
        self.lbl_status.setProperty("class", "Subtitle")
        self.main_layout.addWidget(self.lbl_status)

    def _switch_tab(self, idx, btn):
        for b in [self.btn_dash, self.btn_proc, self.btn_hist]:
            b.setChecked(False)
        btn.setChecked(True)
        self.stack.setCurrentIndex(idx)

    def _build_dashboard(self, parent):
        layout = QVBoxLayout(parent)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # CPU CARD (Dark Purple)
        self.cpu_card = ClayCard(dark=True)
        cpu_layout = QVBoxLayout(self.cpu_card)
        self.lbl_cpu = QLabel("CPU: 0%")
        self.lbl_cpu.setProperty("class", "TitleDark")
        self.chart_cpu = SmoothChart(color="#FFFFFF")
        cpu_layout.addWidget(self.lbl_cpu)
        cpu_layout.addWidget(self.chart_cpu)
        layout.addWidget(self.cpu_card)
        
        # RAM CARD (White)
        self.ram_card = ClayCard()
        ram_layout = QVBoxLayout(self.ram_card)
        self.lbl_ram = QLabel("Memoria RAM")
        self.lbl_ram.setProperty("class", "TitleLight")
        self.ram_bar = QProgressBar()
        self.ram_bar.setRange(0, 100)
        self.ram_bar.setFixedHeight(20)
        self.lbl_ram_det = QLabel("0 GB / 0 GB")
        self.lbl_ram_det.setProperty("class", "Subtitle")
        ram_layout.addWidget(self.lbl_ram)
        ram_layout.addWidget(self.ram_bar)
        ram_layout.addWidget(self.lbl_ram_det)
        layout.addWidget(self.ram_card)
        
        # NETWORK CARD (White)
        self.net_card = ClayCard()
        net_layout = QVBoxLayout(self.net_card)
        self.lbl_net = QLabel("Red: 0 MB/s ▼  0 MB/s ▲")
        self.lbl_net.setProperty("class", "Subtitle")
        self.chart_net = SmoothChart(color="#6C5DD3")
        net_layout.addWidget(self.lbl_net)
        net_layout.addWidget(self.chart_net)
        layout.addWidget(self.net_card)

        # GPU / DISK Basic Stats
        self.gpu_disk_card = ClayCard()
        gd_layout = QVBoxLayout(self.gpu_disk_card)
        self.lbl_gpu = QLabel("GPU Detección... | VRAM...")
        self.lbl_disk = QLabel("Disco C: Uso 0%")
        self.lbl_gpu.setProperty("class", "TitleLight")
        self.lbl_disk.setProperty("class", "Subtitle")
        gd_layout.addWidget(self.lbl_gpu)
        gd_layout.addWidget(self.lbl_disk)
        layout.addWidget(self.gpu_disk_card)
        
        layout.addStretch()

    def _build_processes(self, parent):
        layout = QVBoxLayout(parent)
        
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["PID", "Nombre", "RAM (MB)"])
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        
        btn_kill = QPushButton("Matar Proceso")
        btn_kill.setProperty("class", "ActionButton")
        btn_kill.clicked.connect(self._kill_selected)

        layout.addWidget(QLabel("Top 20 Consumo Memoria"))
        layout.addWidget(self.table)
        layout.addWidget(btn_kill)

    def _build_history(self, parent):
        layout = QVBoxLayout(parent)
        layout.addWidget(QLabel("Herramientas Adicionales"))
        
        btn_overlay = QPushButton("Alternar Game Overlay (Ctrl+Shift+M)")
        btn_overlay.clicked.connect(self.overlay.toggle_visibility)
        
        btn_opt = QPushButton("Ejecutar Sistema Experto")
        btn_opt.clicked.connect(self._run_optimizer)
        
        btn_export = QPushButton("Exportar CSV Historico")
        btn_export.clicked.connect(self._export_csv)

        btn_pdf = QPushButton("Exportar PDF Ejecutivo")
        btn_pdf.clicked.connect(lambda: self._export_pdf())
        
        btn_html = QPushButton("Exportar HTML")
        btn_html.clicked.connect(lambda: self._export_html())
        
        layout.addWidget(btn_overlay)
        layout.addWidget(btn_opt)
        layout.addWidget(btn_export)
        layout.addWidget(btn_pdf)
        layout.addWidget(btn_html)
        layout.addStretch()

    def _start_collector(self):
        self.worker = SystemMonitorWorker(interval=1.5)
        self.worker.metrics_updated.connect(self._on_metrics_updated)
        self.worker.start()

    def _on_metrics_updated(self, data):
        # 1. Update Real-Time Charts & UI
        cpu = data['cpu']['percent']
        temp = data['cpu'].get('temperature', 0)
        self.lbl_cpu.setText(f"CPU Load: {cpu:.1f}% | {temp}°C")
        self.chart_cpu.add_point(cpu)

        ram = data['memory']
        self.ram_bar.setValue(int(ram['percent']))
        u_gb = ram['used'] / (1024**3)
        t_gb = ram['total'] / (1024**3)
        self.lbl_ram_det.setText(f"{u_gb:.1f} / {t_gb:.1f} GB ({ram['percent']}%)")

        net = data['network']
        rx = net['recv_speed'] / (1024**2)
        tx = net['sent_speed'] / (1024**2)
        self.lbl_net.setText(f"Red: {rx:.2f} MB/s ▼ | {tx:.2f} MB/s ▲")
        self.chart_net.add_point(rx + tx)

        gpu = data['gpu']
        self.lbl_gpu.setText(f"GPU: {gpu.get('name', '')} {gpu.get('usage', 0):.1f}%")
        
        # Disco
        disks = data['disk']['partitions']
        if len(disks) > 0:
            c = disks[0]
            self.lbl_disk.setText(f"Disco Principal: En uso {c['percent']}%")

        self.lbl_status.setText(f"Uptime: {int(data['uptime'] // 60)} min")

        # 2. Update Procesos (Aproximación Virtual)
        if self.stack.currentIndex() == 1:
            self._update_processes()

        # 3. Guardar en SQLite (Base de datos Batch/WAL)
        db.insert_snapshot(data)
        
        # 4. Engine Offline Rules
        self.alert_engine.check_rules(data)
        
        # 5. Overlay Si es Visible
        if self.overlay.isVisible():
            self.overlay.update_metrics(data)

    def _update_processes(self):
        try:
            procs = sorted(psutil.process_iter(['pid', 'name', 'memory_info']), 
                           key=lambda x: x.info['memory_info'].rss if x.info.get('memory_info') else 0, 
                           reverse=True)[:20]
                           
            self.table.setRowCount(len(procs))
            for i, p in enumerate(procs):
                self.table.setItem(i, 0, QTableWidgetItem(str(p.info['pid'])))
                self.table.setItem(i, 1, QTableWidgetItem(str(p.info['name'])))
                ram_mb = p.info['memory_info'].rss / (1024**2) if p.info.get('memory_info') else 0
                self.table.setItem(i, 2, QTableWidgetItem(f"{ram_mb:.1f}"))
        except:
            pass

    def _kill_selected(self):
        row = self.table.currentRow()
        if row < 0: return
        pid = int(self.table.item(row, 0).text())
        try:
            psutil.Process(pid).kill()
            QMessageBox.information(self, "Proceso", f"Proceso {pid} eliminado.")
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    def _export_csv(self):
        path, _ = QFileDialog.getSaveFileName(self, "Exportar CSV", "reporte.csv", "CSV Files (*.csv)")
        if path:
            ok = DataExporter.export_csv(db, path)
            QMessageBox.information(self, "Exportación", "Éxito" if ok else "Fallo")

    def _export_html(self):
        path, _ = QFileDialog.getSaveFileName(self, "Exportar HTML", "reporte.html", "HTML Files (*.html)")
        if path:
            ok = DataExporter.export_html(db, path)
            QMessageBox.information(self, "Exportación", "Éxito" if ok else "Fallo")

    def _export_pdf(self):
        path, _ = QFileDialog.getSaveFileName(self, "Exportar PDF", "reporte.pdf", "PDF Files (*.pdf)")
        if path:
            ok = DataExporter.export_pdf(db, path)
            msg = "El modulo reportlab no está instalado." if not ok else "Éxito al exportar."
            QMessageBox.information(self, "Exportación PDF", msg)

    def _run_optimizer(self):
        recs = self.optimizer.analyze()
        msg = "\n\n".join([f"• {r['title']}: {r['desc']}" if type(r)==dict else str(r) for r in recs])
        QMessageBox.information(self, "Sistema Experto (Offline)", msg)

    def closeEvent(self, event):
        self.worker.stop()
        db.close()
        super().closeEvent(event)
