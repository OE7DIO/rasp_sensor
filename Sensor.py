import socket 
import threading
import time as t

def how_many_persons_are_looking_at_my_raspi():
    x = threading.activeCount() - 1
    if x == 1:
        print(f"{x} Person gönnt sich grad die Sensorwerte")
    else:
        print(f"{x} Leit gönnen sich grad die Sensorwerte")

def how_many_persons_will_be_looking_at_my_raspi():
    x = threading.activeCount() - 2
    if x == 1:
        print(f"{x} Person gönnt sich grad die Sensorwerte")
    else:
        print(f"{x} Leit gönnen sich grad die Sensorwerte")


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
            how_many_persons_will_be_looking_at_my_raspi()
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
        how_many_persons_are_looking_at_my_raspi()


print("Da 4-Takt Motor lafft an!")
start()
