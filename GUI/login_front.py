import os
import sys
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QPushButton, 
                             QVBoxLayout, QStackedWidget, QCheckBox, 
                             QHBoxLayout, QGridLayout, QProgressBar)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from LOGIC.login_back import Backend

def resource_path(relative_path):
    """ Obtener la ruta absoluta al recurso, funciona para desarrollo y para PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class RegisterForm(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.backend = Backend()
        layout = QVBoxLayout()

        name_label = QLabel("Nombre *", self)
        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Nombre y Primer Apellido")
        self.name_input.setObjectName("nameInput")

        rut_label = QLabel("Rut *", self)
        self.rut_input = QLineEdit(self)
        self.rut_input.setPlaceholderText("Sin puntos y con guion")
        self.rut_input.setObjectName("rutInput")

        self.rut_error_label = QLabel("", self)
        self.rut_error_label.setStyleSheet("color: red;")

        contact_label = QLabel("Contacto *", self)
        self.contact_input = QLineEdit(self)
        self.contact_input.setPlaceholderText("+56912345678")
        self.contact_input.setObjectName("contactInput")

        email_label = QLabel("Email *", self)
        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText("example@gmail.com")
        self.email_input.setObjectName("emailInput")

        password_label = QLabel("Contraseña *", self)
        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Contraseña")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setObjectName("passwordInput")

        self.password_progress = QProgressBar(self)
        self.password_progress.setObjectName("passwordProgress")
        self.password_progress.setTextVisible(False)
        self.password_input.textChanged.connect(lambda: self.backend.update_password_strength(self.password_input, self.password_progress, self.password_requirements))

        self.password_requirements = QLabel(self)
        self.password_requirements.setObjectName("passwordRequirements")
        self.password_requirements.setText("Debe contener al menos 8 caracteres, una mayúscula y un símbolo.")
        self.password_requirements.setStyleSheet("color: red;")

        icons = {
            'show': resource_path("icons/ver.svg"),
            'hide': resource_path("icons/esconder.svg")
        }
        self.password_action = self.password_input.addAction(QIcon(icons['hide']), QLineEdit.TrailingPosition)
        self.password_action.triggered.connect(lambda: self.backend.toggle_password_visibility(self.password_input, self.password_action, icons))

        register_button = QPushButton("Registrar", self)
        register_button.setObjectName("registerButton")
        register_button.clicked.connect(lambda: self.backend.register_contratante(
            self.name_input, self.rut_input, self.contact_input, self.email_input, self.password_input, self.password_progress, self.password_requirements, self.rut_error_label
        ))

        layout.addWidget(name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(rut_label)
        layout.addWidget(self.rut_input)
        layout.addWidget(self.rut_error_label)
        layout.addWidget(contact_label)
        layout.addWidget(self.contact_input)
        layout.addWidget(email_label)
        layout.addWidget(self.email_input)
        layout.addWidget(password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.password_progress)
        layout.addWidget(self.password_requirements)
        layout.addWidget(register_button)

        self.setLayout(layout)

class LoginForm(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.backend = Backend()
        layout = QVBoxLayout()

        username_label = QLabel("Usuario *", self)
        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Rut sin puntos y con guion")
        self.username_input.setObjectName("usernameInput")

        icon_user = QIcon(resource_path("icons/user.svg"))
        self.username_input.addAction(icon_user, QLineEdit.LeadingPosition)

        password_label = QLabel("Contraseña *", self)
        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Contraseña")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setObjectName("passwordInput")

        icon_lock = QIcon(resource_path("icons/lock.svg"))
        self.password_input.addAction(icon_lock, QLineEdit.LeadingPosition)

        icons = {
            'show': resource_path("icons/ver.svg"),
            'hide': resource_path("icons/esconder.svg")
        }
        self.password_action = self.password_input.addAction(QIcon(icons['hide']), QLineEdit.TrailingPosition)
        self.password_action.triggered.connect(lambda: self.backend.toggle_password_visibility(self.password_input, self.password_action, icons))

        terms_layout = QHBoxLayout()
        self.terms_checkbox = QCheckBox("Acepto los términos y condiciones", self)
        self.terms_checkbox.setObjectName("termsCheckbox")
        terms_label = QLabel('<a href="#">Leer términos y condiciones</a>', self)
        terms_label.setObjectName("termsLabel")
        terms_label.setOpenExternalLinks(False)
        terms_label.linkActivated.connect(lambda: self.backend.show_terms_conditions(self))

        terms_layout.addWidget(self.terms_checkbox)
        terms_layout.addWidget(terms_label)

        login_button = QPushButton("Iniciar sesión", self)
        login_button.setObjectName("loginButton")
        login_button.clicked.connect(lambda: self.backend.check_credentials(
            self.username_input, self.password_input, self.terms_checkbox, self.stacked_widget
        ))

        layout.addWidget(username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(password_label)
        layout.addWidget(self.password_input)
        layout.addLayout(terms_layout)
        layout.addWidget(login_button)

        self.setLayout(layout)

class LoginWindow(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()

        self.stacked_widget = stacked_widget
        self.backend = Backend()

        # Configuración de la ventana
        self.setWindowTitle('Interfaz con Recuadro Blanco')
        self.setGeometry(100, 100, 900, 700)

        try:
            style_path = resource_path("styles/style.qss")
            with open(style_path, "r") as file:
                stylesheet = file.read()
                stylesheet = stylesheet.replace("{unchecked_icon}", resource_path("icons/checkbox_unchecked.svg").replace("\\", "/"))
                stylesheet = stylesheet.replace("{checked_icon}", resource_path("icons/checkbox_checked.svg").replace("\\", "/"))
                self.setStyleSheet(stylesheet)
        except Exception as e:
            print(f"Error al cargar el archivo de estilo: {e}")

        # Layout principal de grid
        grid_layout = QGridLayout()
        grid_layout.setColumnStretch(0, 1)
        grid_layout.setColumnStretch(1, 1)
        grid_layout.setColumnStretch(2, 1)

        self.white_box = QWidget(self)
        self.white_box.setObjectName("whiteBox")
        white_box_layout = QVBoxLayout()
        white_box_layout.setAlignment(Qt.AlignCenter)

        # Logo
        logo_label = QLabel(self)
        logo_label.setObjectName("logoLabel")
        logo_pixmap = QPixmap(resource_path("images/logo.png"))
        logo_label.setPixmap(logo_pixmap.scaled(250, 250, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo_label.setAlignment(Qt.AlignCenter)
        white_box_layout.addWidget(logo_label)

        # Texto Convertidor de contratos PDF
        converter_label = QLabel("Convertidor de contratos PDF", self)
        converter_label.setObjectName("converterLabel")
        converter_label.setAlignment(Qt.AlignCenter)
        white_box_layout.addWidget(converter_label)

        # Botones de Iniciar sesión y Registrarse
        buttons_layout = QHBoxLayout()
        buttons_layout.setAlignment(Qt.AlignCenter)

        self.login_button = QLabel('<a href="#" style="color: #0cb7f2; text-decoration: none;">Iniciar sesión</a>', self)
        self.login_button.setObjectName("loginButton")
        self.login_button.linkActivated.connect(lambda: self.backend.show_form(self.stacked_widget, self.form_container, self.login_form, self.register_form, self.login_button, self.register_button, self.white_box, 'login'))

        self.register_button = QLabel('<a href="#" style="color: #0cb7f2; text-decoration: none;">Registrarse</a>', self)
        self.register_button.setObjectName("registerButton")
        self.register_button.linkActivated.connect(lambda: self.backend.show_form(self.stacked_widget, self.form_container, self.login_form, self.register_form, self.login_button, self.register_button, self.white_box, 'register'))

        buttons_layout.addWidget(self.register_button)
        buttons_layout.addWidget(self.login_button)
        white_box_layout.addLayout(buttons_layout)

        self.form_container = QStackedWidget(self)
        self.login_form = LoginForm(self.stacked_widget)
        self.register_form = RegisterForm(self.stacked_widget)
        self.form_container.addWidget(self.login_form)
        self.form_container.addWidget(self.register_form)

        white_box_layout.addWidget(self.form_container)

        self.white_box.setLayout(white_box_layout)

        grid_layout.addWidget(QWidget(), 0, 0)
        grid_layout.addWidget(self.white_box, 0, 1, 1, 1, alignment=Qt.AlignCenter)
        grid_layout.addWidget(QWidget(), 0, 2)

        self.setLayout(grid_layout)

        self.backend.show_form(self.stacked_widget, self.form_container, self.login_form, self.register_form, self.login_button, self.register_button, self.white_box, 'login')
