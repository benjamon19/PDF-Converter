from PyQt5.QtWidgets import QStackedWidget
from gestionar import Gestionar
from documento import GestionarDocumento

class Navigation:
    def __init__(self, stacked_widget):
        self.stacked_widget = stacked_widget

    def show_login(self):
        from GUI.login_front import LoginWindow 
        login_window = LoginWindow(self.stacked_widget)
        self.stacked_widget.addWidget(login_window)
        self.stacked_widget.setCurrentWidget(login_window)

    def show_menu(self):
        from menu import MainWindow  
        main_window = MainWindow(self.stacked_widget)
        self.stacked_widget.addWidget(main_window)
        self.stacked_widget.setCurrentWidget(main_window)

    def show_gestionar(self):
        gestionar_window = Gestionar(self.stacked_widget)
        self.stacked_widget.addWidget(gestionar_window)
        self.stacked_widget.setCurrentWidget(gestionar_window)

    def show_documento(self):
        documento_window = GestionarDocumento(self.stacked_widget)
        self.stacked_widget.addWidget(documento_window)
        self.stacked_widget.setCurrentWidget(documento_window)