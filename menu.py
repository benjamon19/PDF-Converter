import sys
import os
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout, QSpacerItem, QSizePolicy, QFrame, QPushButton)
from PyQt5.QtCore import Qt, QPoint, QPropertyAnimation, pyqtSignal
from PyQt5.QtGui import QPixmap, QIcon, QPainter, QFont, QTransform, QCursor

def resource_path(relative_path):
    """ Obtener la ruta absoluta al recurso, funciona para desarrollo y para PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class HoverFrame(QFrame):
    clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.default_pos = self.pos()
        self.animation = QPropertyAnimation(self, b"pos")
        self.opacity_animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(200)
        self.opacity_animation.setDuration(200)
        self.setCursor(QCursor(Qt.PointingHandCursor))

    def enterEvent(self, event):
        self.default_pos = self.pos()
        self.animation.stop()
        self.opacity_animation.stop()
        self.animation.setEndValue(self.default_pos + QPoint(10, -10))
        self.opacity_animation.setEndValue(0.9)
        self.animation.start()
        self.opacity_animation.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.animation.stop()
        self.opacity_animation.stop()
        self.animation.setEndValue(self.default_pos)
        self.opacity_animation.setEndValue(1.0)
        self.animation.start()
        self.opacity_animation.start()
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)

def create_icon_label(frame, icon_path):
    label = QLabel(frame)
    if os.path.exists(icon_path):
        pixmap = QPixmap(icon_path)
        if not pixmap.isNull():
            label.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
    label.setAlignment(Qt.AlignCenter)
    return label

class MainWindow(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.setWindowTitle('Gestión de Contratos')
        self.setGeometry(100, 100, 1400, 900)

        try:
            style_path = resource_path("styles/menu.qss")
            with open(style_path, "r") as file:
                stylesheet = file.read()
                self.setStyleSheet(stylesheet)
        except Exception as e:
            print(f"Error al cargar el archivo de estilo: {e}")

        layout = QVBoxLayout(self)

        top_frame = QWidget(self)
        top_layout = QHBoxLayout(top_frame)
        top_layout.setSpacing(10)
        top_layout.setContentsMargins(10, 10, 10, 10)

        self.logo_label = QLabel(self)
        logo_pixmap = QPixmap(resource_path("images/logo.png"))
        self.logo_label.setPixmap(logo_pixmap.scaled(250, 250, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.logo_label.setAlignment(Qt.AlignRight)
        top_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        top_layout.addWidget(self.logo_label)
        layout.addWidget(top_frame)

        layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        grid_layout = QGridLayout()
        grid_layout.setSpacing(10)
        grid_layout.setContentsMargins(0, 0, 0, 0)
        grid_layout.setColumnStretch(0, 1)
        grid_layout.setColumnStretch(1, 1)

        frame_gestionar = HoverFrame(self)
        frame_gestionar.setFixedSize(500, 500)
        frame_gestionar.clicked.connect(self.on_gestionar_clicked)
        gestionar_layout = QGridLayout(frame_gestionar)
        gestionar_layout.setSpacing(5)

        icon_1 = create_icon_label(frame_gestionar, resource_path("images/casco-de-seguridad.png"))
        icon_2 = create_icon_label(frame_gestionar, resource_path("images/herramientas.png"))
        icon_3 = create_icon_label(frame_gestionar, resource_path("images/hombre-empleado.png"))
        icon_4 = create_icon_label(frame_gestionar, resource_path("images/maletin.png"))

        gestionar_layout.addWidget(icon_1, 0, 0, Qt.AlignCenter)
        gestionar_layout.addWidget(icon_2, 0, 1, Qt.AlignCenter)
        gestionar_layout.addWidget(icon_3, 1, 0, Qt.AlignCenter)
        gestionar_layout.addWidget(icon_4, 1, 1, Qt.AlignCenter)

        frame_modificar = HoverFrame(self)
        frame_modificar.setFixedSize(500, 500)
        frame_modificar.clicked.connect(self.on_modificar_clicked)
        modificar_layout = QGridLayout(frame_modificar)
        modificar_layout.setSpacing(5)

        icon_5 = create_icon_label(frame_modificar, resource_path("images/agregar-documento.png"))
        icon_6 = create_icon_label(frame_modificar, resource_path("images/buscar-alt.png"))
        icon_7 = create_icon_label(frame_modificar, resource_path("images/archivo-de-edicion.png"))
        icon_8 = create_icon_label(frame_modificar, resource_path("images/documento-aseptado.png"))

        modificar_layout.addWidget(icon_5, 0, 0, Qt.AlignCenter)
        modificar_layout.addWidget(icon_6, 0, 1, Qt.AlignCenter)
        modificar_layout.addWidget(icon_7, 1, 0, Qt.AlignCenter)
        modificar_layout.addWidget(icon_8, 1, 1, Qt.AlignCenter)

        grid_layout.addWidget(frame_gestionar, 0, 0, Qt.AlignCenter)
        grid_layout.addWidget(frame_modificar, 0, 1, Qt.AlignCenter)

        layout.addLayout(grid_layout)

        gestionar_label = QLabel("Gestión de Trabajador", self)
        gestionar_label.setAlignment(Qt.AlignCenter)
        gestionar_label.setFont(QFont('Arial', 42))
        gestionar_label.setObjectName("gestionarLabel")

        modificar_label = QLabel("Gestión de Documento", self)
        modificar_label.setAlignment(Qt.AlignCenter)
        modificar_label.setFont(QFont('Arial', 42))
        modificar_label.setObjectName("modificarLabel")

        grid_layout.addWidget(gestionar_label, 1, 0, Qt.AlignCenter)
        grid_layout.addWidget(modificar_label, 1, 1, Qt.AlignCenter)

        layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        bottom_frame = QWidget(self)
        bottom_layout = QHBoxLayout(bottom_frame)
        bottom_layout.setSpacing(0)
        bottom_layout.setContentsMargins(10, 10, 10, 10)

        self.back_button = QPushButton("Volver al inicio", self)
        self.back_button.setObjectName("backButton")
        self.back_button.setIcon(QIcon(resource_path("icons/home_white.svg")))
        self.back_button.clicked.connect(self.go_to_login)

        bottom_layout.addWidget(self.back_button)
        bottom_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.copyright_label = QLabel("© 2024 WSS Testing and Certification", self)
        self.copyright_label.setAlignment(Qt.AlignCenter)
        self.copyright_label.setObjectName("copyrightLabel")
        bottom_layout.addWidget(self.copyright_label, alignment=Qt.AlignCenter)

        layout.addWidget(bottom_frame)

        self.setLayout(layout)

    def go_to_login(self):
        from LOGIC.navigation import Navigation
        navigator = Navigation(self.stacked_widget)
        navigator.show_login()

    def on_gestionar_clicked(self):
        from LOGIC.navigation import Navigation
        navigator = Navigation(self.stacked_widget)
        navigator.show_gestionar()

    def on_modificar_clicked(self):
        from LOGIC.navigation import Navigation
        navigator = Navigation(self.stacked_widget)
        navigator.show_documento()

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)
        painter.setOpacity(0.15)
        background_pixmap = QPixmap(resource_path("images/logoGrande.png"))
        size = self.size()
        new_size = size * 1
        scaled_pixmap = background_pixmap.scaled(new_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        transform = QTransform()
        transform.rotate(-15)
        rotated_pixmap = scaled_pixmap.transformed(transform, Qt.SmoothTransformation)

        painter.drawPixmap(self.rect().center() - rotated_pixmap.rect().center(), rotated_pixmap)

if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication, QStackedWidget
    app = QApplication(sys.argv)
    stacked_widget = QStackedWidget()
    from LOGIC.navigation import Navigation
    navigator = Navigation(stacked_widget)
    main_window = MainWindow(stacked_widget)
    stacked_widget.addWidget(main_window)
    stacked_widget.setCurrentWidget(main_window)
    stacked_widget.show()
    sys.exit(app.exec_())
