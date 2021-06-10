import socket 
import threading
import time as t
import msgpack
import configparser
import random
import sys

def n_recievers():
    x = threading.active_count() - 1
    if x == 1:
        print("{} Person gönnt sich grad die Sensorwerte".format(x))
    else:
        print("{} Leit gönnen sich grad die Sensorwerte".format(x))


PORT = 5050
SERVER = "0.0.0.0"
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!D"
custom_sensors = []




def handle_client(conn, addr):
    global custom_sensors
    print("Der Hansl von: {} gönnt sich jetzt a die Messwerte".format(addr))
    connected = True
    while connected:
        t.sleep(1)
        try:
            msg = conn.recv(4096).decode(FORMAT)
        except:
            connected = False
            conn.close()
            print("[{}]: Connection Lost!".format(addr))
            break
        if msg == DISCONNECT_MESSAGE or msg == None:
            connected = False
            conn.close()
            print("[{}]: Connection Lost!".format(addr))
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

            
            for custom_sensor in custom_sensors:
                try:
                    exec("import " + custom_sensor)
                    x = eval(custom_sensor + ".get_data()")
                    message["type"].append(x[0])
                    message["value"].append(x[1])
                    message["unit"].append(x[2])
                except:
                    print("Warning: Customsensors {} 'get_data' function is corrupt".format(custom_sensor))

            packer = msgpack.Packer()
            conn.sendall(packer.pack(message))        
    conn.close()


def read_config():
    global custom_sensors
    try:
        config_object = configparser.ConfigParser()
        config_object.read("SensorConfig.conf")
        senfo = config_object["CUSTOMSENSORS"]
        custom_sensors = list(senfo["filename"].split(","))

        for custom_sensor in custom_sensors:
            try:
                
                exec("import " + custom_sensor)
            except:
                print("ERROR: Customsensor {} is corrupt!".format(custom_sensor))
        for custom_sensor in custom_sensors:
            try:
                eval(custom_sensor + ".init_sensor()")
            except:
                print("Warning: Customsensor {} has no 'init_sensor' function".format(custom_sensor))

    except Exception:
        config_object = configparser.ConfigParser()
        config_object["CUSTOMSENSORS"] = {
            "filename" : ""
        }

        with open("SensorConfig.conf", 'w') as conf:
            config_object.write(conf)
        print("a config file has been created.")
    
    return "Schad"
        

if __name__ == "__main__":
    read_config()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()

    print("Da 4-Takt Motor lafft an!")
    print("Da Server horcht auf alle IPs: {}".format(SERVER))
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        n_recievers()
