import os
import sys
from PyQt5.QtWidgets import QApplication, QStackedWidget
from PyQt5.QtGui import QIcon
from LOGIC.navigation import Navigation

def resource_path(relative_path):
    """ Obtener la ruta absoluta al recurso, funciona para desarrollo y para PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def load_stylesheet():
    qss_path = resource_path("styles/style.qss")
    with open(qss_path, "r") as file:
        stylesheet = file.read()

    stylesheet = stylesheet.replace("{unchecked_icon}", resource_path("icons/checkbox_unchecked.svg").replace("\\", "/"))
    stylesheet = stylesheet.replace("{checked_icon}", resource_path("icons/checkbox_checked.svg").replace("\\", "/"))
    return stylesheet

if __name__ == '__main__':
    app = QApplication(sys.argv)

    icon_path = resource_path("RIFT.ico")
    app.setWindowIcon(QIcon(icon_path))

    stacked_widget = QStackedWidget()
    navigator = Navigation(stacked_widget)  

    navigator.show_login()  

    stacked_widget.show()

    sys.exit(app.exec_())