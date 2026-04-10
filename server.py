import socket
import sqlite3
from datetime import datetime

HOST = '127.0.0.1'
PORT = 5000
DB_NAME = 'chat.db'


# Inicializar base de datos
def inicializar_db():
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

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
        print(f"Error DB: {e}")


# Guardar mensaje
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
        print(f"Error guardando: {e}")
        return None


# Inicializar socket
def inicializar_socket():
    try:
        servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        servidor.bind((HOST, PORT))
        servidor.listen(5)

        print(f"Servidor escuchando en {HOST}:{PORT}")
        return servidor

    except OSError as e:
        print(f"Error puerto: {e}")
        return None


# Manejar cliente
def manejar_cliente(conn, addr):
    print(f"Conectado: {addr}")

    try:
        while True:
            data = conn.recv(1024)

            if not data:
                break

            mensaje = data.decode()

            fecha = guardar_mensaje(mensaje, addr[0])

            if fecha:
                respuesta = f"Mensaje recibido: {fecha}"
            else:
                respuesta = "Error al guardar"

            conn.send(respuesta.encode())

    except Exception as e:
        print(f"Error cliente: {e}")

    finally:
        conn.close()
        print(f"Desconectado: {addr}")


# Aceptar conexiones
def aceptar_conexiones(servidor):
    while True:
        try:
            conn, addr = servidor.accept()
            manejar_cliente(conn, addr)

        except Exception as e:
            print(f"Error conexión: {e}")


# MAIN
if __name__ == "__main__":
    inicializar_db()
    servidor = inicializar_socket()

    if servidor:
        aceptar_conexiones(servidor)