import os
import sys
from itertools import cycle
from PyQt5.QtWidgets import (QMessageBox, QLineEdit, QDialog, QVBoxLayout, QScrollArea, QLabel, QHBoxLayout, 
                             QSpacerItem, QSizePolicy, QPushButton, QWidget, QProgressBar)
from PyQt5.QtGui import QIcon
from data.database import DatabaseManager

def resource_path(relative_path):
    """ Obtener la ruta absoluta al recurso, funciona para desarrollo y para PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class Backend:
    def __init__(self):
        self.db_manager = DatabaseManager()

    def validate_rut(self, rut):
        rut = rut.replace(".", "").upper()
        try:
            rut_body, verifier = rut.split("-")
            rut_body = int(rut_body)
            return verifier == self.calculate_verifier(rut_body)
        except (ValueError, IndexError):
            return False

    def calculate_verifier(self, rut_body):
        reversed_digits = map(int, reversed(str(rut_body)))
        factors = cycle(range(2, 8))
        s = sum(d * f for d, f in zip(reversed_digits, factors))
        mod = (-s) % 11
        return {10: "K", 11: "0"}.get(mod, str(mod))

    def validate_password(self, password):
        return len(password) >= 8 and any(char.isupper() for char in password) and any(char in '!@#$%^&*()_+=.,;:-[]"' for char in password)

    def validate_password_strength(self, password):
        strength = 0
        if len(password) >= 8:
            strength += 1
        if any(char.isupper() for char in password):
            strength += 1
        if any(char in '!@#$%^&*()_+=.,;:-[]"' for char in password):
            strength += 1
        return strength

    def save_contratante(self, nombre, rut, contacto, email, password):
        return self.db_manager.save_contratante(nombre, rut, contacto, email, password)

    def validate_contratante(self, username, password):
        return self.db_manager.validate_contratante(username, password)

    def load_terms_conditions(self):
        try:
            with open(resource_path("terms_conditions.txt"), "r", encoding="utf-8") as file:
                return file.read()
        except Exception as e:
            return f"Error al cargar los términos y condiciones: {e}"

    def show_warning(self, parent, message):
        warning_box = QMessageBox(parent)
        warning_box.setWindowTitle("Error")
        warning_box.setText(message)
        warning_box.setIcon(QMessageBox.Warning)
        warning_box.setStandardButtons(QMessageBox.Ok)
        ok_button = warning_box.button(QMessageBox.Ok)
        warning_box.exec_()

    def show_message(self, parent, message):
        message_box = QMessageBox(parent)
        message_box.setWindowTitle("Información")
        message_box.setText(message)
        message_box.setIcon(QMessageBox.Information)
        message_box.setStandardButtons(QMessageBox.Ok)
        ok_button = message_box.button(QMessageBox.Ok)
        message_box.exec_()

    def clear_fields(self, *fields):
        for field in fields:
            field.clear()

    def toggle_password_visibility(self, password_input, password_action, icons):
        if password_input.echoMode() == QLineEdit.Password:
            password_input.setEchoMode(QLineEdit.Normal)
            password_action.setIcon(QIcon(resource_path(icons['show'])))
        else:
            password_input.setEchoMode(QLineEdit.Password)
            password_action.setIcon(QIcon(resource_path(icons['hide'])))

    def register_contratante(self, name_input, rut_input, contact_input, email_input, password_input, password_progress, password_requirements, rut_error_label):
        nombre = name_input.text()
        rut = rut_input.text()
        contacto = contact_input.text()
        email = email_input.text()
        password = password_input.text()

        if not nombre or not rut or not contacto or not email:
            self.show_warning(name_input, "Por favor, rellene todos los campos")
        else:
            valid_rut = self.validate_rut(rut)
            if not valid_rut:
                rut_input.setStyleSheet("border: 1px solid red;")
                rut_error_label.setText("RUT no válido. Ingrese RUT sin puntos y con guion.")
            elif not self.validate_password(password):
                self.show_warning(password_input, "La contraseña debe tener al menos 8 caracteres, una mayúscula y un símbolo.")
            elif self.db_manager.rut_exists(rut):
                rut_input.setStyleSheet("border: 1px solid red;")
                rut_error_label.setText("El RUT ya existe en la base de datos.")
            else:
                if self.save_contratante(nombre, rut, contacto, email, password):
                    self.show_message(name_input, "Registro exitoso. Ahora puede iniciar sesión.")
                    self.clear_fields(name_input, rut_input, contact_input, email_input, password_input)
                    rut_input.setStyleSheet("") 
                    rut_error_label.setText("")  
                else:
                    self.show_warning(name_input, "Error al registrar el usuario.")

    def update_password_strength(self, password_input, password_progress, password_requirements):
        password = password_input.text()
        strength = self.validate_password_strength(password)

        if strength == 1:
            password_progress.setValue(33)
            password_progress.setStyleSheet("QProgressBar::chunk { background-color: red; }")
            password_requirements.setStyleSheet("color: red;")
        elif strength == 2:
            password_progress.setValue(66)
            password_progress.setStyleSheet("QProgressBar::chunk { background-color: orange; }")
            password_requirements.setStyleSheet("color: orange;")
        elif strength == 3:
            password_progress.setValue(100)
            password_progress.setStyleSheet("QProgressBar::chunk { background-color: green; }")
            password_requirements.setStyleSheet("color: green;")
        else:
            password_progress.setValue(0)

    def check_credentials(self, username_input, password_input, terms_checkbox, stacked_widget):
        username = username_input.text()
        password = password_input.text()

        if not username or not password:
            self.show_warning(username_input, "Por favor, rellene todos los campos")
        elif not terms_checkbox.isChecked():
            self.show_warning(terms_checkbox, "Debe aceptar los términos y condiciones")
        elif self.validate_contratante(username, password):
            self.transition_to_new_window(stacked_widget)
        else:
            self.show_warning(username_input, "Usuario o contraseña incorrectos")

    def transition_to_new_window(self, stacked_widget):
        from menu import MainWindow
        new_window = MainWindow(stacked_widget)
        stacked_widget.addWidget(new_window)
        stacked_widget.setCurrentWidget(new_window)

    def show_terms_conditions(self, parent):
        dialog = TermsConditionsDialog(parent)
        dialog.exec_()

    def show_form(self, stacked_widget, form_container, login_form, register_form, login_button, register_button, white_box, form_type):
        if (form_type == 'login'):
            form_container.setCurrentWidget(login_form)
            login_button.setStyleSheet("font-weight: bold; font-size: 16px; color: black; border-bottom: none;")
            register_button.setStyleSheet("font-weight: normal; font-size: 14px; color: black; border-bottom: none;")
            white_box.setFixedSize(500, 460)
        else:
            form_container.setCurrentWidget(register_form)
            login_button.setStyleSheet("font-weight: normal; font-size: 14px; color: black; border-bottom: none;")
            register_button.setStyleSheet("font-weight: bold; font-size: 16px; color: black; border-bottom: 2px solid #00BFFF;")
            white_box.setFixedSize(500, 750) 

class TermsConditionsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Términos y Condiciones")
        self.setFixedSize(400, 300)
        self.backend = Backend()
        layout = QVBoxLayout()

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        content_widget = QWidget()
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(10, 10, 10, 10)
        
        terms_text = QLabel(self.backend.load_terms_conditions())
        terms_text.setWordWrap(True)
        content_layout.addWidget(terms_text)

        content_widget.setLayout(content_layout)
        scroll_area.setWidget(content_widget)

        layout.addWidget(scroll_area)

        button_layout = QHBoxLayout()
        button_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum))  # Espaciador
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        button_layout.addWidget(ok_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)
