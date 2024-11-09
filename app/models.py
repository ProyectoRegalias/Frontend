import os
import mysql.connector
from mysql.connector import Error
import json

# Cargar configuración desde archivo JSON
def cargar_configuracion():
    config_file = os.path.join(os.path.dirname(__file__), 'config.json')  # Ruta relativa al archivo config.json
    try:
        with open(config_file, 'r') as file:
            config = json.load(file)
            return config['database']
    except Exception as e:
        print(f"Error al cargar la configuración: {e}")
        return None


# Configuración de la conexión a la base de datos usando el archivo de configuración
def crear_conexion():
    db_config = cargar_configuracion()
    if db_config:
        try:
            conexion = mysql.connector.connect(
                host=db_config['host'],
                database=db_config['database'],
                user=db_config['user'],
                password=db_config['password']
            )
            if conexion.is_connected():
                return conexion
        except Error as e:
            print(f"Error al conectar a MySQL: {e}")
    return None


# Función para cargar usuarios
def cargar_usuarios():
    usuarios = {}
    conexion = crear_conexion()
    if conexion:
        try:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("SELECT username, password FROM Usuario")
            for row in cursor.fetchall():
                usuarios[row['username']] = row['password']
        except Error as e:
            print(f"Error al cargar usuarios: {e}")
        finally:
            cursor.close()
            conexion.close()
    return usuarios


# Función para guardar un usuario
def guardar_usuario(username, password):
    print("Intentando guardar usuario en la base de datos...")
    conexion = crear_conexion()
    if conexion:
        try:
            cursor = conexion.cursor()
            print("Conexión a la base de datos establecida.")
            cursor.execute("INSERT INTO Usuario (username, password) VALUES (%s, %s)", (username, password))
            conexion.commit()
            print("Usuario guardado exitosamente.")
        except mysql.connector.Error as e:
            print(f"Error al guardar usuario: {e}")
        finally:
            cursor.close()
            conexion.close()
    else:
        print("Error al conectar a la base de datos.")


# Función para cargar el historial de un usuario
def cargar_historial_usuario(username):
    historial = []
    conexion = crear_conexion()
    if conexion:
        try:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("SELECT pregunta, respuesta FROM historial WHERE username = %s", (username,))
            historial = cursor.fetchall()
        except Error as e:
            print(f"Error al cargar historial: {e}")
        finally:
            cursor.close()
            conexion.close()
    return historial


# Función para guardar datos de un usuario
def guardar_datos_usuario(username, pregunta, respuesta):
    conexion = crear_conexion()
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute(
                "INSERT INTO historial (username, pregunta, respuesta) VALUES (%s, %s, %s)",
                (username, pregunta, respuesta)
            )
            conexion.commit()
        except Error as e:
            print(f"Error al guardar historial: {e}")
        finally:
            cursor.close()
            conexion.close()
