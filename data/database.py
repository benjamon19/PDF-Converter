import sqlite3
import bcrypt
import os

class DatabaseManager:
    _db_initialized = False

    def __init__(self, db_path='data/database.db'):
        self.db_path = db_path
        self.ensure_data_directory()
        self.connect_to_db()
        self.init_db()

    def ensure_data_directory(self):
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

    def connect_to_db(self):
        try:
            self.db_connection = sqlite3.connect(self.db_path)
            self.db_cursor = self.db_connection.cursor()
        except sqlite3.Error as err:
            print(f"Error: {err}")

    def init_db(self):
        if DatabaseManager._db_initialized:
            return

        try:
            self.db_cursor.execute("""
                CREATE TABLE IF NOT EXISTS contratante (
                    idContratante INTEGER PRIMARY KEY AUTOINCREMENT,
                    Nombre TEXT,
                    Rut TEXT NOT NULL UNIQUE,
                    Empresa TEXT,
                    Contacto TEXT,
                    Email TEXT,
                    Contraseña TEXT NOT NULL
                )
            """)

            self.db_cursor.execute("""
                CREATE TABLE IF NOT EXISTS contratista (
                    idContratista INTEGER PRIMARY KEY AUTOINCREMENT,
                    Nombre TEXT,
                    "Estado Civil" TEXT,
                    "Fecha de Nacimiento" DATE,
                    "Fonasa o Isapre" TEXT,
                    AFP TEXT,
                    Contacto TEXT,
                    Email TEXT,
                    Rut TEXT NOT NULL UNIQUE,
                    "Ciudad de residencia" TEXT,
                    "Pais de residencia" TEXT,
                    Nacionalidad TEXT,
                    Domicilio TEXT
                )
            """)

            self.db_cursor.execute("""
                CREATE TABLE IF NOT EXISTS contrato (
                    idContrato INTEGER PRIMARY KEY AUTOINCREMENT,
                    Descripcion TEXT,
                    Contratante INTEGER NOT NULL,
                    Contratista INTEGER NOT NULL,
                    Plantilla INTEGER NOT NULL,
                    PDF TEXT,
                    "Fecha del Contrato" DATE NOT NULL,
                    "Fecha inicio del contrato" DATE NOT NULL,
                    "Fecha de Finalizacion del contrato" DATE,
                    "Sueldo Base" TEXT,
                    "Bono Asistencia" TEXT,
                    Colacion TEXT,
                    "Tipo Contrato" TEXT,
                    FOREIGN KEY (Contratante) REFERENCES contratante(idContratante),
                    FOREIGN KEY (Contratista) REFERENCES contratista(idContratista),
                    FOREIGN KEY (Plantilla) REFERENCES plantilla(idPlantilla)
                )
            """)

            self.db_cursor.execute("""
                CREATE TABLE IF NOT EXISTS firmas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    path TEXT
                )
            """)

            self.db_cursor.execute("""
                CREATE TABLE IF NOT EXISTS plantilla (
                    idPlantilla INTEGER PRIMARY KEY AUTOINCREMENT,
                    Nombre TEXT,
                    RutaPdf TEXT NOT NULL
                )
            """)

            self.db_cursor.execute("""
                CREATE TABLE IF NOT EXISTS rubro (
                    idRubro INTEGER PRIMARY KEY AUTOINCREMENT,
                    Nombre TEXT NOT NULL,
                    Descripcion TEXT
                )
            """)

            self.db_cursor.execute("INSERT OR IGNORE INTO rubro (idRubro, Nombre) VALUES (1, 'General')")
            self.db_connection.commit()

            self.db_cursor.execute("SELECT * FROM contratante WHERE Rut = 'admin'")
            result = self.db_cursor.fetchone()
            if not result:
                hashed_password = bcrypt.hashpw('1234'.encode('utf-8'), bcrypt.gensalt())
                self.db_cursor.execute("INSERT INTO contratante (Nombre, Rut, Empresa, Contacto, Email, Contraseña) VALUES (?, ?, ?, ?, ?, ?)",
                                       ('Administrador', 'admin', 'N/A', 'N/A', 'admin@example.com', hashed_password))
                self.db_connection.commit()

            self.add_column_if_not_exists('contratista', 'AFP', 'TEXT')
            self.add_column_if_not_exists('contratista', 'Domicilio', 'TEXT')

            print("Base de datos creada/cargada correctamente.")
            DatabaseManager._db_initialized = True
        except sqlite3.Error as err:
            print(f"Error: {err}")

    def add_column_if_not_exists(self, table, column, column_type):
        self.db_cursor.execute(f"PRAGMA table_info({table})")
        columns = [info[1] for info in self.db_cursor.fetchall()]
        if column not in columns:
            self.db_cursor.execute(f"ALTER TABLE {table} ADD COLUMN {column} {column_type}")
            self.db_connection.commit()

    def load_contratante_data(self):
        try:
            self.db_cursor.execute("SELECT idContratante, Nombre, Rut, Empresa, Email, Contacto FROM contratante")
            return self.db_cursor.fetchall()
        except sqlite3.Error as err:
            print(f"Error al cargar contratante: {err}")
            return []

    def load_contratista_data(self):
        try:
            self.db_cursor.execute("SELECT idContratista, Rut, Nombre, \"Estado Civil\", \"Fecha de Nacimiento\", \"Fonasa o Isapre\", AFP, Contacto, Email, \"Ciudad de residencia\", \"Pais de residencia\", Nacionalidad, Domicilio FROM contratista")
            return self.db_cursor.fetchall()
        except sqlite3.Error as err:
            print(f"Error al cargar contratista: {err}")
            return []

    def load_contrato_data(self):
        try:
            self.db_cursor.execute("SELECT idContrato, Descripcion, Contratante, Contratista, Plantilla, PDF, \"Fecha del Contrato\", \"Fecha inicio del contrato\", \"Fecha de Finalizacion del contrato\", \"Sueldo Base\", \"Bono Asistencia\", Colacion, \"Tipo Contrato\" FROM contrato")
            return self.db_cursor.fetchall()
        except sqlite3.Error as err:
            print(f"Error al cargar contrato: {err}")
            return []

    def load_firmas_data(self):
        try:
            self.db_cursor.execute("SELECT id, name, path FROM firmas")
            return self.db_cursor.fetchall()
        except sqlite3.Error as err:
            print(f"Error al cargar firmas: {err}")
            return []

    def load_plantilla_data(self):
        try:
            self.db_cursor.execute("SELECT idPlantilla, Nombre, RutaPdf FROM plantilla")
            return self.db_cursor.fetchall()
        except sqlite3.Error as err:
            print(f"Error al cargar plantilla: {err}")
            return []

    def load_rubro_data(self):
        try:
            self.db_cursor.execute("SELECT idRubro, Nombre, Descripcion FROM rubro")
            return self.db_cursor.fetchall()
        except sqlite3.Error as err:
            print(f"Error al cargar rubro: {err}")
            return []

    def validate_contratante(self, rut, contraseña):
        try:
            self.db_cursor.execute("SELECT Contraseña FROM contratante WHERE Rut = ?", (rut,))
            result = self.db_cursor.fetchone()
            if result and bcrypt.checkpw(contraseña.encode('utf-8'), result[0]):
                return True
            return False
        except sqlite3.Error as err:
            print(f"Error al validar el usuario: {err}")
            return False

    def save_contratante(self, nombre, rut, contacto, email, password):
        try:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            self.db_cursor.execute("INSERT INTO contratante (Nombre, Rut, Empresa, Contacto, Email, Contraseña) VALUES (?, ?, ?, ?, ?, ?)",
                                   (nombre, rut, "N/A", contacto, email, hashed_password))
            self.db_connection.commit()
            return True
        except sqlite3.Error as err:
            print(f"Error al guardar el contratante: {err}")
            return False

    def save_contratista(self, fields_data):
        try:
            self.db_cursor.execute("SELECT idContratista FROM contratista WHERE Rut = ?", (fields_data["RUT"],))
            result = self.db_cursor.fetchone()

            if result:
                self.db_cursor.execute("""
                    UPDATE contratista SET
                        Nombre = ?, "Estado Civil" = ?, "Fecha de Nacimiento" = ?, "Fonasa o Isapre" = ?, AFP = ?, 
                        Contacto = ?, Email = ?, "Ciudad de residencia" = ?, "Pais de residencia" = ?, 
                        Nacionalidad = ?, Domicilio = ?
                    WHERE Rut = ?
                """, (
                    fields_data["NOMBRE"], fields_data["ESTADO_CIVIL"], fields_data["FECHA_NACIMIENTO"], 
                    fields_data["FONASA_ISAPRE"], fields_data["AFP"], fields_data["CONTACTO"], fields_data["EMAIL"], 
                    fields_data["CIUDAD"], fields_data["PAIS"], fields_data["NACIONALIDAD"], fields_data["DOMICILIO"], fields_data["RUT"]
                ))
            else:
                self.db_cursor.execute("""
                    INSERT INTO contratista (
                        Nombre, "Estado Civil", "Fecha de Nacimiento", "Fonasa o Isapre", AFP, 
                        Contacto, Email, Rut, "Ciudad de residencia", "Pais de residencia", 
                        Nacionalidad, Domicilio
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    fields_data["NOMBRE"], fields_data["ESTADO_CIVIL"], fields_data["FECHA_NACIMIENTO"], 
                    fields_data["FONASA_ISAPRE"], fields_data["AFP"], fields_data["CONTACTO"], fields_data["EMAIL"], 
                    fields_data["RUT"], fields_data["CIUDAD"], fields_data["PAIS"], 
                    fields_data["NACIONALIDAD"], fields_data["DOMICILIO"]
                ))

            self.db_connection.commit()
        except sqlite3.Error as err:
            print(f"Error al actualizar los datos del contratista: {err}")
            return False
        return True

    def delete_contratista(self, worker_id):
        try:
            self.db_cursor.execute("DELETE FROM contratista WHERE idContratista = ?", (worker_id,))
            self.db_connection.commit()
        except sqlite3.Error as err:
            print(f"Error al eliminar el trabajador: {err}")

    def get_contratista_by_rut(self, rut):
        try:
            self.db_cursor.execute("SELECT idContratista, Rut, Nombre, \"Estado Civil\", \"Fecha de Nacimiento\", \"Fonasa o Isapre\", AFP, Contacto, Email, \"Ciudad de residencia\", \"Pais de residencia\", Nacionalidad, Domicilio FROM contratista WHERE Rut = ?", (rut,))
            return self.db_cursor.fetchone()
        except sqlite3.Error as err:
            print(f"Error al obtener contratista por RUT: {err}")
            return None

    def save_template(self, name, file_path):
        try:
            self.db_cursor.execute("INSERT INTO plantilla (Nombre, RutaPdf) VALUES (?, ?)", (name, file_path))
            self.db_connection.commit()
            return True
        except sqlite3.Error as err:
            print(f"Error al guardar la plantilla: {err}")
            return False

    def delete_template(self, name):
        try:
            self.db_cursor.execute("DELETE FROM plantilla WHERE Nombre = ?", (name,))
            self.db_connection.commit()
            return True
        except sqlite3.Error as err:
            print(f"Error al eliminar la plantilla: {err}")
            return False

    def get_plantilla_by_id(self, plantilla_id):
        try:
            self.db_cursor.execute("SELECT * FROM plantilla WHERE idPlantilla = ?", (plantilla_id,))
            return self.db_cursor.fetchone()
        except sqlite3.Error as err:
            print(f"Error al obtener la plantilla: {err}")
            return None

    # Funciones relacionadas con firmas
    def load_signatures(self):
        try:
            self.db_cursor.execute("SELECT id, name, path FROM firmas")
            return self.db_cursor.fetchall()
        except sqlite3.Error as err:
            print(f"Error al cargar firmas: {err}")
            return []

    def save_signature(self, name, path):
        try:
            self.db_cursor.execute("INSERT INTO firmas (name, path) VALUES (?, ?)", (name, path))
            self.db_connection.commit()
            return True
        except sqlite3.Error as err:
            print(f"Error al guardar la firma: {err}")
            return False

    def delete_signature(self, signature_id):
        try:
            self.db_cursor.execute("SELECT path FROM firmas WHERE id = ?", (signature_id,))
            path = self.db_cursor.fetchone()
            if path and os.path.exists(path[0]):
                os.remove(path[0])
            self.db_cursor.execute("DELETE FROM firmas WHERE id = ?", (signature_id,))
            self.db_connection.commit()
            return True
        except sqlite3.Error as err:
            print(f"Error al eliminar la firma: {err}")
            return False

    def rut_exists(self, rut):
        try:
            self.db_cursor.execute("SELECT 1 FROM contratante WHERE Rut = ?", (rut,))
            return self.db_cursor.fetchone() is not None
        except sqlite3.Error as err:
            print(f"Error al verificar si el RUT existe: {err}")
            return False