import socket 
import threading
import time as t

HEADER = 64
PORT = 5050
SERVER = "0.0.0.0"
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!D"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    print(f"Der Hansl von: {addr} gönnt sich jetzt a die Messwerte")

    connected = True
    while connected:
        t.sleep(1)
        conn.send("A cooler Messwert".encode(FORMAT))
        msg = conn.recv(4096).decode(FORMAT)
        if msg == DISCONNECT_MESSAGE or msg == None:
            print(f"{threading.activeCount() - 1} Leit gönnen sich grad die Sensorwerte")
            connected = False

        print(f"[{addr}] {msg}")

    conn.close()
        

def start():
    server.listen()
    print(f"Da Server horcht auf alle IPs: {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"{threading.activeCount() - 1} Leit gönnen sich grad die Sensorwerte")


print("Da 4-Takt Motor laffn an!")
start()