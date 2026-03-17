from PySide6.QtWidgets import QFrame, QGraphicsDropShadowEffect
from PySide6.QtGui import QColor
import pyqtgraph as pg

class ShadowEffect(QGraphicsDropShadowEffect):
    def __init__(self, color_hex="#33000000", radius=25, x=0, y=10):
        super().__init__()
        self.setBlurRadius(radius)
        self.setColor(QColor(color_hex))
        self.setOffset(x, y)

class ClayCard(QFrame):
    def __init__(self, dark=False):
        super().__init__()
        self.setProperty("class", "CardDark" if dark else "Card")
        self.setGraphicsEffect(ShadowEffect("#40000000" if dark else "#18000000"))

class SmoothChart(pg.PlotWidget):
    """ Gráfico base optimizado para alto rendimiento y animación fluida """
    def __init__(self, color='#FFFFFF'):
        super().__init__()
        self.setBackground("transparent")
        self.hideAxis('bottom')
        self.hideAxis('left')
        self.setMouseEnabled(x=False, y=False)
        self.curve = self.plot(pen=pg.mkPen(color=color, width=3))
        
        # Buffer de datos prellenado (ej. ultimos 60 ticks)
        self.data_buffer = [0] * 60
        self.curve.setData(self.data_buffer)

    def add_point(self, value):
        self.data_buffer.pop(0)
        self.data_buffer.append(value)
        self.curve.setData(self.data_buffer)
