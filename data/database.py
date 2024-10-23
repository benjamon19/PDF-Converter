import pymysql
import bcrypt
import os
from data import config

class DatabaseManager:

    def __init__(self):
        self.host = config.DB_HOST
        self.user = config.DB_USER
        self.password = config.DB_PASSWORD
        self.db_name = config.DB_NAME
        self.connect_to_db()

    def connect_to_db(self):
        try:
            self.db_connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.db_name,
                port=3306,  # Asegúrate de que este es el puerto correcto
                cursorclass=pymysql.cursors.DictCursor,
                autocommit=True
            )
            self.db_cursor = self.db_connection.cursor()
            print("Conexión exitosa a la base de datos")
        except pymysql.MySQLError as err:
            self.db_connection = None
            print(f"Error al conectar a la base de datos: {err}")

    def load_contratante_data(self):
        try:
            self.db_cursor.execute("SELECT idContratante, Nombre, Rut, Empresa, Email, Contacto FROM contratante")
            return self.db_cursor.fetchall()
        except pymysql.MySQLError as err:
            print(f"Error al cargar contratante: {err}")
            return []

    def load_contratista_data(self):
        try:
            self.db_cursor.execute("""
                SELECT idContratista, Rut, Nombre, EstadoCivil, FechaNacimiento, FonasaIsapre, AFP,
                Contacto, Email, CiudadResidencia, PaisResidencia, Nacionalidad, Domicilio
                FROM contratista
            """)
            return self.db_cursor.fetchall()
        except pymysql.MySQLError as err:
            print(f"Error al cargar contratista: {err}")
            return []

    def load_contrato_data(self):
        try:
            self.db_cursor.execute("""
                SELECT idContrato, Descripcion, Contratante, Contratista, Plantilla, PDF,
                FechaContrato, FechaInicioContrato, FechaFinContrato,
                SueldoBase, BonoAsistencia, Colacion, TipoContrato
                FROM contrato
            """)
            return self.db_cursor.fetchall()
        except pymysql.MySQLError as err:
            print(f"Error al cargar contrato: {err}")
            return []

    def load_firmas_data(self):
        try:
            self.db_cursor.execute("SELECT id, name, path FROM firmas")
            return self.db_cursor.fetchall()
        except pymysql.MySQLError as err:
            print(f"Error al cargar firmas: {err}")
            return []

    def load_plantilla_data(self):
        try:
            self.db_cursor.execute("SELECT idPlantilla, Nombre, RutaPdf FROM plantilla")
            return self.db_cursor.fetchall()
        except pymysql.MySQLError as err:
            print(f"Error al cargar plantilla: {err}")
            return []

    def load_rubro_data(self):
        try:
            self.db_cursor.execute("SELECT idRubro, Nombre, Descripcion FROM rubro")
            return self.db_cursor.fetchall()
        except pymysql.MySQLError as err:
            print(f"Error al cargar rubro: {err}")
            return []

    def validate_contratante(self, rut, contraseña):
        try:
            self.db_cursor.execute("SELECT Contraseña FROM contratante WHERE Rut = %s", (rut,))
            result = self.db_cursor.fetchone()
            if result and bcrypt.checkpw(contraseña.encode('utf-8'), result['Contraseña']):
                return True
            return False
        except pymysql.MySQLError as err:
            print(f"Error al validar el usuario: {err}")
            return False

    def save_contratante(self, nombre, rut, contacto, email, password):
        try:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            self.db_cursor.execute("""
                INSERT INTO contratante (Nombre, Rut, Empresa, Contacto, Email, Contraseña)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (nombre, rut, "N/A", contacto, email, hashed_password))
            return True
        except pymysql.MySQLError as err:
            print(f"Error al guardar el contratante: {err}")
            return False

    def save_contratista(self, fields_data):
        try:
            self.db_cursor.execute("SELECT idContratista FROM contratista WHERE Rut = %s", (fields_data["RUT"],))
            result = self.db_cursor.fetchone()
            if result:
                self.db_cursor.execute("""
                    UPDATE contratista SET
                        Nombre = %s, EstadoCivil = %s, FechaNacimiento = %s, FonasaIsapre = %s, AFP = %s,
                        Contacto = %s, Email = %s, CiudadResidencia = %s, PaisResidencia = %s,
                        Nacionalidad = %s, Domicilio = %s
                    WHERE Rut = %s
                """, (
                    fields_data["NOMBRE"], fields_data["ESTADO_CIVIL"], fields_data["FECHA_NACIMIENTO"],
                    fields_data["FONASA_ISAPRE"], fields_data["AFP"], fields_data["CONTACTO"], fields_data["EMAIL"],
                    fields_data["CIUDAD"], fields_data["PAIS"], fields_data["NACIONALIDAD"], fields_data["DOMICILIO"],
                    fields_data["RUT"]
                ))
            else:
                self.db_cursor.execute("""
                    INSERT INTO contratista (
                        Nombre, EstadoCivil, FechaNacimiento, FonasaIsapre, AFP,
                        Contacto, Email, Rut, CiudadResidencia, PaisResidencia,
                        Nacionalidad, Domicilio
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    fields_data["NOMBRE"], fields_data["ESTADO_CIVIL"], fields_data["FECHA_NACIMIENTO"],
                    fields_data["FONASA_ISAPRE"], fields_data["AFP"], fields_data["CONTACTO"], fields_data["EMAIL"],
                    fields_data["RUT"], fields_data["CIUDAD"], fields_data["PAIS"],
                    fields_data["NACIONALIDAD"], fields_data["DOMICILIO"]
                ))
            return True
        except pymysql.MySQLError as err:
            print(f"Error al actualizar los datos del contratista: {err}")
            return False

    def delete_contratista(self, worker_id):
        try:
            self.db_cursor.execute("DELETE FROM contratista WHERE idContratista = %s", (worker_id,))
        except pymysql.MySQLError as err:
            print(f"Error al eliminar el trabajador: {err}")

    def get_contratista_by_rut(self, rut):
        try:
            self.db_cursor.execute("""
                SELECT idContratista, Rut, Nombre, EstadoCivil, FechaNacimiento, FonasaIsapre, AFP, Contacto, Email,
                CiudadResidencia, PaisResidencia, Nacionalidad, Domicilio
                FROM contratista WHERE Rut = %s
            """, (rut,))
            return self.db_cursor.fetchone()
        except pymysql.MySQLError as err:
            print(f"Error al obtener contratista por RUT: {err}")
            return None

    def save_template(self, name, file_path):
        try:
            self.db_cursor.execute("INSERT INTO plantilla (Nombre, RutaPdf) VALUES (%s, %s)", (name, file_path))
            return True
        except pymysql.MySQLError as err:
            print(f"Error al guardar la plantilla: {err}")
            return False

    def delete_template(self, name):
        try:
            self.db_cursor.execute("DELETE FROM plantilla WHERE Nombre = %s", (name,))
            return True
        except pymysql.MySQLError as err:
            print(f"Error al eliminar la plantilla: {err}")
            return False

    def get_plantilla_by_id(self, plantilla_id):
        try:
            self.db_cursor.execute("SELECT * FROM plantilla WHERE idPlantilla = %s", (plantilla_id,))
            return self.db_cursor.fetchone()
        except pymysql.MySQLError as err:
            print(f"Error al obtener la plantilla: {err}")
            return None

    def load_signatures(self):
        try:
            self.db_cursor.execute("SELECT id, name, path FROM firmas")
            return self.db_cursor.fetchall()
        except pymysql.MySQLError as err:
            print(f"Error al cargar firmas: {err}")
            return []

    def save_signature(self, name, path):
        try:
            self.db_cursor.execute("INSERT INTO firmas (name, path) VALUES (%s, %s)", (name, path))
            return True
        except pymysql.MySQLError as err:
            print(f"Error al guardar la firma: {err}")
            return False

    def delete_signature(self, signature_id):
        try:
            self.db_cursor.execute("SELECT path FROM firmas WHERE id = %s", (signature_id,))
            path = self.db_cursor.fetchone()
            if path and os.path.exists(path['path']):
                os.remove(path['path'])
            self.db_cursor.execute("DELETE FROM firmas WHERE id = %s", (signature_id,))
            return True
        except pymysql.MySQLError as err:
            print(f"Error al eliminar la firma: {err}")
            return False

    def rut_exists(self, rut):
        try:
            self.db_cursor.execute("SELECT 1 FROM contratante WHERE Rut = %s", (rut,))
            return self.db_cursor.fetchone() is not None
        except pymysql.MySQLError as err:
            print(f"Error al verificar si el RUT existe: {err}")
            return False

if __name__ == "__main__":
    db_manager = DatabaseManager()
    contratantes = db_manager.load_contratante_data()
    print("Contratantes:", contratantes)
