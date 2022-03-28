from ..utils.utils import PORT
import socket
from _thread import start_new_thread


SERVER = "localhost"


def client_thread(conn: socket):
    conn.send(str.encode("CONNECTED playerID ACK"))
    while True:
        try:
            data = conn.recv(2048)
            response = data.decode("UTF-8")

            conn.sendall(str.encode("pong"))
        except:
            break

    conn.close()


def main():
    print("SERVER STARTED")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.bind((SERVER, PORT))
        print(f"BOUND TO PORT {PORT}")
    except socket.error as error:
        print(error)

    print("WAITING FOR CONNECTIONS")
    s.listen()
    stay_alive = True
    while stay_alive:
        conn, addr = s.accept()
        print(f"CONNECTION FROM {addr}")
        start_new_thread(client_thread, (conn,))
