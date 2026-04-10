import socket
import sqlite3
from datetime import datetime

# Configuración del servidor

HOST = '127.0.0.1'
PORT = 5000
DB_NAME = 'chat.db'


# Inicializar base de datos

def inicializar_db():
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        # Crear tabla si no existe
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mensajes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contenido TEXT NOT NULL,
                fecha_envio TEXT NOT NULL,
                ip_cliente TEXT NOT NULL
            )
        ''')

        conn.commit()
        conn.close()

    except Exception as e:
        print(f"Error al inicializar la DB: {e}")


# Guardar mensaje en DB

def guardar_mensaje(contenido, ip_cliente):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute('''
            INSERT INTO mensajes (contenido, fecha_envio, ip_cliente)
            VALUES (?, ?, ?)
        ''', (contenido, fecha, ip_cliente))

        conn.commit()
        conn.close()

        return fecha

    except Exception as e:
        print(f"Error al guardar mensaje: {e}")
        return None


# Inicializar socket servidor

def inicializar_socket():
    try:
        servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Permite reutilizar el puerto si queda ocupado
        servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        servidor.bind((HOST, PORT))
        servidor.listen(5)

        print(f"Servidor escuchando en {HOST}:{PORT}")
        return servidor

    except OSError as e:
        print(f"Error con el puerto: {e}")
        return None


# Manejo de clientes

def manejar_cliente(conn, addr):
    print(f"Conectado con {addr}")

    try:
        while True:
            data = conn.recv(1024)

            if not data:
                break

            mensaje = data.decode()

            # Guardar en DB
            fecha = guardar_mensaje(mensaje, addr[0])

            if fecha:
                respuesta = f"Mensaje recibido: {fecha}"
            else:
                respuesta = "Error al guardar el mensaje"

            conn.send(respuesta.encode())

    except Exception as e:
        print(f"Error con cliente {addr}: {e}")

    finally:
        conn.close()
        print(Conexión cerrada con {addr}")


# Aceptar conexiones

def aceptar_conexiones(servidor):
    while True:
        try:
            conn, addr = servidor.accept()
            manejar_cliente(conn, addr)

        except Exception as e:
            print(f"Error aceptando conexiones: {e}")


# MAIN

if __name__ == "__main__":
    inicializar_db()
    servidor = inicializar_socket()

    if servidor:
        aceptar_conexiones(servidor)