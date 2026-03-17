from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QFrame)
from PySide6.QtCore import Qt
import keyboard

class GameOverlay(QWidget):
    """
    Overlay transparente para Modo Juego (Always on Top).
    Atraviesa clics y flota sobre DirectX/Vulkan.
    """
    def __init__(self):
        super().__init__()
        
        # Flags Mágicas para Windows Overlay Intrusivo pero Transparente a Clics
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool |
            Qt.WindowType.WindowTransparentForInput
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        self.setGeometry(10, 10, 250, 80)
        self._init_ui()
        
        # Atajo Global para Mostrar/Ocultar
        try:
            keyboard.add_hotkey('ctrl+shift+m', self.toggle_visibility)
        except:
            pass # Falla si no somos admin

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        
        self.panel = QFrame()
        self.panel.setStyleSheet("""
            QFrame {
                background-color: rgba(20, 20, 30, 180);
                border-radius: 10px;
                border: 1px solid #333344;
            }
            QLabel {
                color: #00FF99;
                font-family: 'Consolas', monospace;
                font-weight: bold;
                font-size: 14px;
            }
        """)
        panel_layout = QVBoxLayout(self.panel)
        panel_layout.setContentsMargins(10, 5, 10, 5)
        
        self.lbl_cpu = QLabel("CPU: 0% | Temp: 0°C")
        self.lbl_gpu = QLabel("GPU: 0% | VRAM: 0GB")
        self.lbl_ram = QLabel("RAM: 0GB")
        
        panel_layout.addWidget(self.lbl_cpu)
        panel_layout.addWidget(self.lbl_gpu)
        panel_layout.addWidget(self.lbl_ram)
        layout.addWidget(self.panel)

    def update_metrics(self, data):
        """ Llama la app principal para refrescar el overlay a bajo lag """
        cpu = data.get('cpu', {}).get('percent', 0)
        temp = data.get('cpu', {}).get('temperature', 0)
        ram_gb = data.get('memory', {}).get('used', 0) / (1024**3)
        gpu = data.get('gpu', {}).get('usage', 0)
        
        self.lbl_cpu.setText(f"CPU: {cpu:.1f}% | {temp}°C")
        self.lbl_gpu.setText(f"GPU: {gpu:.1f}%")
        self.lbl_ram.setText(f"RAM: {ram_gb:.1f} GB")

    def toggle_visibility(self):
        if self.isVisible():
            self.hide()
        else:
            self.show()
