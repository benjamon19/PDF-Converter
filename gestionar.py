import sys
import os
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem, 
                             QSpacerItem, QSizePolicy, QFrame, QPushButton, QTabWidget, QLineEdit, QAction, 
                             QDialog, QFormLayout, QMessageBox, QHeaderView, QComboBox, QDateEdit, QInputDialog)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QPixmap, QIcon
from data.database import DatabaseManager

def resource_path(relative_path):
    """ Obtener la ruta absoluta al recurso, funciona para desarrollo y para PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class AddWorkerDialog(QDialog):
    def __init__(self, db_manager, rut=None):
        super().__init__()
        self.db_manager = db_manager
        self.setWindowTitle("Agregar/Modificar Trabajador")
        self.setMinimumWidth(450)
        self.init_ui()
        self.load_styles()
        if rut:
            self.rut_input.setText(rut)
            self.check_existing_worker()
        self.adjustSize()

    def load_styles(self):
        try:
            style_path = resource_path("styles/gestionar.qss")
            with open(style_path, "r") as file:
                self.setStyleSheet(file.read())
        except Exception as e:
            print(f"Error al cargar el archivo de estilo: {e}")

    def init_ui(self):
        layout = QFormLayout(self)

        self.rut_input = QLineEdit(self)
        self.rut_input.setPlaceholderText("Sin puntos y con guion")
        self.rut_input.textChanged.connect(self.check_existing_worker)
        layout.addRow("Rut", self.rut_input)

        self.name_input = QLineEdit(self)
        self.estado_civil_input = QComboBox(self)
        self.estado_civil_input.addItems(["Soltero/a", "Casado/a", "Divorciado/a", "Viudo/a"])
        self.fecha_nacimiento_input = QDateEdit(self)
        self.fecha_nacimiento_input.setDisplayFormat("yyyy-MM-dd")
        self.fecha_nacimiento_input.setCalendarPopup(True)
        self.fonasa_input = QComboBox(self)
        self.fonasa_input.addItems(["Fonasa", "Isapre Banmédica", "Isapre Colmena", "Isapre Consalud", "Isapre Cruz Blanca", "Isapre Masvida", "Isapre Vida Tres"])
        self.afp_input = QComboBox(self)
        self.afp_input.addItems(["AFP Habitat", "AFP Capital", "AFP Cuprum", "AFP PlanVital", "AFP ProVida", "AFP Modelo"])
        self.contact_input = QLineEdit(self)
        self.email_input = QLineEdit(self)
        self.domicilio_input = QLineEdit(self)
        self.ciudad_input = QLineEdit(self)
        self.pais_input = QLineEdit(self)
        self.nacionalidad_input = QLineEdit(self)

        layout.addRow("Nombre", self.name_input)
        layout.addRow("Estado Civil", self.estado_civil_input)
        layout.addRow("Fecha de Nacimiento", self.fecha_nacimiento_input)
        layout.addRow("Fonasa o Isapre", self.fonasa_input)
        layout.addRow("AFP", self.afp_input)
        layout.addRow("Contacto", self.contact_input)
        layout.addRow("Email", self.email_input)
        layout.addRow("Ciudad", self.domicilio_input)
        layout.addRow("País", self.ciudad_input)
        layout.addRow("Nacionalidad", self.pais_input)
        layout.addRow("Domicilio", self.nacionalidad_input)

        self.add_button = QPushButton("Agregar/Modificar", self)
        self.add_button.setObjectName("addButton")
        self.add_button.clicked.connect(self.add_or_modify_worker)
        layout.addRow(self.add_button)

        self.setLayout(layout)

    def check_existing_worker(self):
        rut = self.rut_input.text()
        worker_data = self.db_manager.get_contratista_by_rut(rut)
        if worker_data:
            self.name_input.setText(worker_data[2])
            self.estado_civil_input.setCurrentText(worker_data[3])
            self.fecha_nacimiento_input.setDate(QDate.fromString(worker_data[4], "yyyy-MM-dd"))
            self.fonasa_input.setCurrentText(worker_data[5])
            self.afp_input.setCurrentText(worker_data[6])
            self.contact_input.setText(worker_data[7])
            self.email_input.setText(worker_data[8])
            self.domicilio_input.setText(worker_data[9])
            self.ciudad_input.setText(worker_data[10])
            self.pais_input.setText(worker_data[11])
            self.nacionalidad_input.setText(worker_data[12])
            self.add_button.setText("Modificar")
        else:
            self.name_input.clear()
            self.estado_civil_input.setCurrentIndex(0)
            self.fecha_nacimiento_input.setDate(QDate.currentDate())
            self.fonasa_input.setCurrentIndex(0)
            self.afp_input.setCurrentIndex(0)
            self.contact_input.clear()
            self.email_input.clear()
            self.domicilio_input.clear()
            self.ciudad_input.clear()
            self.pais_input.clear()
            self.nacionalidad_input.clear()
            self.add_button.setText("Agregar")

    def add_or_modify_worker(self):
        fields_data = {
            "RUT": self.rut_input.text(),
            "NOMBRE": self.name_input.text(),
            "ESTADO_CIVIL": self.estado_civil_input.currentText(),
            "FECHA_NACIMIENTO": self.fecha_nacimiento_input.date().toString("yyyy-MM-dd"),
            "FONASA_ISAPRE": self.fonasa_input.currentText(),
            "AFP": self.afp_input.currentText(),
            "CONTACTO": self.contact_input.text(),
            "EMAIL": self.email_input.text(),
            "CIUDAD": self.domicilio_input.text(),
            "PAIS": self.ciudad_input.text(),
            "NACIONALIDAD": self.pais_input.text(),
            "DOMICILIO": self.nacionalidad_input.text(),
        }

        if self.add_button.text() == "Agregar":
            if self.db_manager.save_contratista(fields_data):
                self.show_message("Éxito", "Trabajador agregado exitosamente.")
            else:
                self.show_warning("Error al agregar trabajador.")
        else:
            if self.db_manager.save_contratista(fields_data):
                self.show_message("Éxito", "Trabajador modificado exitosamente.")
            else:
                self.show_warning("Error al modificar trabajador.")

        self.accept()

    def show_message(self, title, message):
        message_box = QMessageBox(self)
        message_box.setWindowTitle(title)
        message_box.setText(message)
        message_box.setIcon(QMessageBox.Information)
        ok_button = message_box.addButton(QMessageBox.Ok)
        ok_button.setMinimumWidth(120)
        message_box.exec_()

    def show_warning(self, message):
        warning_box = QMessageBox(self)
        warning_box.setWindowTitle("Error")
        warning_box.setText(message)
        warning_box.setIcon(QMessageBox.Warning)
        ok_button = warning_box.addButton(QMessageBox.Ok)
        ok_button.setMinimumWidth(120)
        warning_box.exec_()

class Gestionar(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.db_manager = DatabaseManager()
        self.init_ui()
        self.load_styles()

    def load_styles(self):
        try:
            style_path = resource_path("styles/gestionar.qss")
            with open(style_path, "r") as file:
                self.setStyleSheet(file.read())
        except Exception as e:
            print(f"Error al cargar el archivo de estilo: {e}")

    def init_ui(self):
        self.setWindowTitle('Gestionar Trabajador')
        self.setGeometry(100, 100, 1200, 800)

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

        self.database_label = QLabel("Gestión de Trabajadores", self)
        self.database_label.setObjectName("databaseLabel")
        layout.addWidget(self.database_label, alignment=Qt.AlignLeft)

        search_layout = QHBoxLayout()
        self.search_input = QLineEdit(self)
        self.search_input.setObjectName("searchInput")
        self.search_input.setPlaceholderText("Buscar trabajador por Rut...")
        self.search_input.textChanged.connect(self.filter_table)

        search_icon_action = QAction(QIcon(resource_path("icons/search.svg")), "", self.search_input)
        self.search_input.addAction(search_icon_action, QLineEdit.LeadingPosition)
        search_layout.addWidget(self.search_input)
        search_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        
        layout.addLayout(search_layout)

        self.tabs = QTabWidget(self)
        self.tabs.setObjectName("tabs")

        self.worker_table = self.create_table(["ID", "Rut", "Nombre", "Estado Civil", "Cumpleaños", "Fonasa o Isapre", "AFP", "Contacto", "Email", "Ciudad", "País", "Nacionalidad", "Domicilio"], self.db_manager.load_contratista_data)
        self.contract_table = self.create_table(["ID", "Descripción", "Contratante", "Trabajador", "Plantilla", "PDF", "Fecha Contrato", "Inicio Contrato", "Cierre Contrato", "Sueldo Base", "Bono Asistencia", "Colacion", "Tipo Contrato"], self.db_manager.load_contrato_data)

        self.tabs.addTab(self.worker_table, "Trabajadores")
        self.tabs.addTab(self.contract_table, "Contratos")

        layout.addWidget(self.tabs)

        self.placeholder_label = QLabel("De momento está vacío, debe agregar trabajadores mediante el botón Agregar Trabajador", self)
        self.placeholder_label.setAlignment(Qt.AlignCenter)
        self.placeholder_label.setObjectName("placeholderLabel")
        layout.addWidget(self.placeholder_label)

        bottom_frame = QWidget(self)
        bottom_layout = QHBoxLayout(bottom_frame)
        bottom_layout.setSpacing(10)
        bottom_layout.setContentsMargins(10, 10, 10, 10)

        self.back_button = QPushButton("Volver al menú", self)
        self.back_button.setObjectName("backButton")
        self.back_button.setIcon(QIcon(resource_path("icons/home_white.svg")))
        self.back_button.clicked.connect(self.go_to_menu)

        self.add_button = QPushButton("Agregar Trabajador", self)
        self.add_button.setObjectName("addButton")
        self.add_button.clicked.connect(self.show_add_modify_worker_dialog)

        self.modify_button = QPushButton("Modificar Trabajador", self)
        self.modify_button.setObjectName("modifyButton")
        self.modify_button.clicked.connect(self.show_modify_worker_dialog)

        self.delete_button = QPushButton("Eliminar Trabajador", self)
        self.delete_button.setObjectName("deleteButton")
        self.delete_button.clicked.connect(self.delete_worker)

        bottom_layout.addWidget(self.back_button)
        bottom_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        bottom_layout.addWidget(self.add_button)
        bottom_layout.addWidget(self.modify_button)
        bottom_layout.addWidget(self.delete_button)

        layout.addWidget(bottom_frame)

        self.setLayout(layout)

        self.update_placeholder_visibility()

    def create_table(self, headers, load_data_func):
        table = QTableWidget(self)
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)
        table.horizontalHeader().setStretchLastSection(True)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        data = load_data_func()
        for row_data in data:
            row_number = table.rowCount()
            table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        return table

    def update_placeholder_visibility(self):
        if self.worker_table.rowCount() == 0:
            self.placeholder_label.show()
        else:
            self.placeholder_label.hide()

    def filter_table(self):
        query = self.search_input.text().lower()
        current_table = self.tabs.currentWidget()
        for row in range(current_table.rowCount()):
            match = False
            for column in range(current_table.columnCount()):
                item = current_table.item(row, column)
                if item and query in item.text().lower():
                    match = True
                    break
            current_table.setRowHidden(row, not match)

    def go_to_menu(self):
        self.stacked_widget.setCurrentIndex(1)

    def show_add_modify_worker_dialog(self):
        dialog = AddWorkerDialog(self.db_manager)
        if dialog.exec_() == QDialog.Accepted:
            self.refresh_worker_table()

    def show_modify_worker_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Modificar Trabajador")
        dialog.setMinimumWidth(400)  

        layout = QVBoxLayout(dialog)

        label = QLabel("Ingrese el Rut del trabajador:")
        layout.addWidget(label)

        rut_input = QLineEdit(dialog)
        layout.addWidget(rut_input)

        button_layout = QHBoxLayout()
        ok_button = QPushButton("OK")
        ok_button.setMinimumWidth(120) 
        cancel_button = QPushButton("Cancel")
        cancel_button.setMinimumWidth(120) 

        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)

        ok_button.clicked.connect(dialog.accept)
        cancel_button.clicked.connect(dialog.reject)

        if dialog.exec_() == QDialog.Accepted:
            rut = rut_input.text()
            if rut:
                worker_dialog = AddWorkerDialog(self.db_manager, rut=rut)
                if worker_dialog.exec_() == QDialog.Accepted:
                    self.refresh_worker_table()

    def refresh_worker_table(self):
        self.worker_table.setRowCount(0)
        data = self.db_manager.load_contratista_data()
        for row_data in data:
            row_number = self.worker_table.rowCount()
            self.worker_table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.worker_table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        self.update_placeholder_visibility()

    def delete_worker(self):
        selected_items = self.worker_table.selectedItems()
        if not selected_items:
            self.show_warning("Seleccione un trabajador para eliminar.")
            return

        selected_row = selected_items[0].row()
        worker_id = self.worker_table.item(selected_row, 0).text()
        worker_name = self.worker_table.item(selected_row, 2).text()
        worker_rut = self.worker_table.item(selected_row, 1).text()

        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Eliminar Trabajador")
        msg_box.setText(f"¿Está seguro de que desea eliminar al trabajador?\n\nNombre: {worker_name}\nRut: {worker_rut}")
        msg_box.setIcon(QMessageBox.Question)
        yes_button = msg_box.addButton(QMessageBox.Yes)
        no_button = msg_box.addButton(QMessageBox.No)
        yes_button.setMinimumWidth(120)
        no_button.setMinimumWidth(120)
        msg_box.exec_()

        if msg_box.clickedButton() == yes_button:
            self.db_manager.delete_contratista(worker_id)
            self.worker_table.removeRow(selected_row)
            self.update_placeholder_visibility()

    def show_warning(self, message):
        warning_box = QMessageBox(self)
        warning_box.setWindowTitle("Error")
        warning_box.setText(message)
        warning_box.setIcon(QMessageBox.Warning)
        ok_button = warning_box.addButton(QMessageBox.Ok)
        ok_button.setMinimumWidth(120)
        warning_box.exec_()

if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication, QStackedWidget
    app = QApplication(sys.argv)
    stacked_widget = QStackedWidget()
    gestionar_window = Gestionar(stacked_widget)
    stacked_widget.addWidget(gestionar_window)
    stacked_widget.setCurrentWidget(gestionar_window)
    stacked_widget.show()
    sys.exit(app.exec_())