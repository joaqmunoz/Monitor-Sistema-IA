CLAY_THEME = """
QWidget#MainWindow {
    background-color: #E2E2EC; /* Color principal de fondo apastelado oscuro/azulado suave */
}

/* Las tarjetas principales (Cards) */
QFrame.Card {
    background-color: #FFFFFF;
    border-radius: 30px;
}

QFrame.CardDark {
    background-color: #403889; /* Azul purpura del mockup */
    border-radius: 30px;
}

QLabel {
    font-family: 'Segoe UI', system-ui;
    color: #4A4A68;
}

QLabel.TitleDark {
    color: #FFFFFF;
    font-size: 16px;
    font-weight: bold;
}

QLabel.TitleLight {
    color: #403889;
    font-size: 20px;
    font-weight: bold;
}

QLabel.Subtitle {
    color: #8A8BA6;
    font-size: 12px;
}

/* Tablas con Virtual Scrolling para procesos */
QTableView {
    background-color: transparent;
    border: none;
    color: #4A4A68;
    gridline-color: transparent;
    selection-background-color: #DEDDF1;
    selection-color: #403889;
}
QHeaderView::section {
    background-color: transparent;
    color: #8A8BA6;
    font-weight: bold;
    border: none;
    border-bottom: 2px solid #F0F0F7;
    padding: 10px;
}

/* Barras de progreso circulares (QProgressBar custom) */
QProgressBar {
    background-color: #F0F0F7;
    border-radius: 10px;
    text-align: center;
    color: transparent; 
}
QProgressBar::chunk {
    background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                                      stop: 0 #6C5DD3, stop: 1 #A79FF2);
    border-radius: 10px;
}

/* Botones estilo Pill Modernos */
QPushButton {
    background-color: #FFFFFF;
    color: #8A8BA6;
    border: 2px solid transparent;
    border-radius: 20px;
    font-weight: bold;
    font-size: 14px;
    padding: 10px;
}

QPushButton:hover {
    background-color: #DEDDF1;
    color: #403889;
}

QPushButton:checked {
    background-color: #403889;
    color: #FFFFFF;
}

QPushButton.ActionButton {
    background-color: #6C5DD3;
    color: white;
}
QPushButton.ActionButton:hover {
    background-color: #403889;
}
"""
