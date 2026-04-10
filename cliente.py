import socket

HOST = '127.0.0.1'
PORT = 5000


def iniciar_cliente():
    try:
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente.connect((HOST, PORT))

        print("Conectado al servidor")
        print("Escribí mensajes (escribí 'exito' para salir)\n")

        while True:
            mensaje = input("Mensaje: ")

            if mensaje.lower() == "exito":
                print("Cerrando conexión...")
                break

            cliente.send(mensaje.encode())

            respuesta = cliente.recv(1024).decode()
            print(f"Servidor: {respuesta}")

        cliente.close()

    except ConnectionRefusedError:
        print("No se pudo conectar al servidor")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    iniciar_cliente()