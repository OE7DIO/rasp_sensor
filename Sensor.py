import socket 
import threading
import time as t
import msgpack
import random
import sys

def n_recievers():
    x = threading.activeCount() - 1
    if x == 1:
        print(f"{x} Person gönnt sich grad die Sensorwerte")
    else:
        print(f"{x} Leit gönnen sich grad die Sensorwerte")


PORT = 5050
SERVER = "0.0.0.0"
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!D"




def handle_client(conn, addr):
    global old_python
    if old_python:
        print("Der Hansl von: {} gönnt sich jetzt a die Messwerte".format(addr))
    else:
        print(f"Der Hansl von: {addr} gönnt sich jetzt a die Messwerte")

    connected = True
    while connected:
        t.sleep(1)
        try:
            msg = conn.recv(4096).decode(FORMAT)
        except:
            connected = False
            conn.close()
            if old_python:
                print("[{}]: Connection Lost!".format(addr))
            else:
                print(f"[{addr}] Connection Lost!")
            break
        if msg == DISCONNECT_MESSAGE or msg == None:
            connected = False
            conn.close()
            if old_python:
                print("[{}]: Connection Lost!".format(addr))
            else:
                print(f"[{addr}] Connection Lost!")
            break


        else:
            message = {
                "source" : "Source",
                "ID" : 1,
                "time" : t.time(),
                "type" : ["Temperatur", "Wasserstand", "Taster"],
                "value" : [random.randint(0, 100), random.randint(5, 20), random.randint(0, 1)],
                "unit" : ["°C", "m", ""],
            }
        
            packer = msgpack.Packer()
            conn.sendall(packer.pack(message))

    if old_python:
        print("[{}]: Connection Lost!".format(addr))
    else:
        print(f"[{addr}] Connection Lost!")
    conn.close()
        

if __name__ == "__main__":
    global old_python
    old_python = False
    if sys.version_info < (3, 6):
        old_python = True

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()

    print("Da 4-Takt Motor lafft an!")
    if old_python:
        print("Da Server horcht auf alle IPs: {}".format(SERVER))
    else:
        print(f"Da Server horcht auf alle IPs: {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        n_recievers()
