import socket
import msgpack
import threading
import time as t
import configparser
import os
import sys

FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!D"
status_running = True
sensors=[]


class Sensor():
    def __init__(self, name, ip, port):
        self.__name = name
        self.__address = (ip, port)
        self.__data = []
        self.__connection_status = "Connection Lost!"
    
    def __str__(self):
        print(f"Sensor {self.__name}: {self.__connection_status}")
        x = ""
        for count, value in enumerate(self.__data[1]):
            x = x + f"{self.__data[0][count]}: {value} {self.__data[2][count]}"
            for i in range(40*(count+1) - len(x)):
                x = x +" "
        return x

    def establish_connection(self):
        while status_running:
            try:
                self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.__sock.connect(self.__address)
                break
            except ConnectionRefusedError:
                t.sleep(5)
                continue
    
    def send_msg(self, msg):
        message = msg.encode(FORMAT)
        self.__sock.send(message)
    
    def recv_msg(self):
        self.__unpacker = msgpack.Unpacker()
        self.__buffer = self.__sock.recv(4096)
        self.__unpacker.feed(self.__buffer)
        for x in self.__unpacker:
            return x

    def activate_sensor(self, msg):
        self.establish_connection()
        thread = threading.Thread(target=self.collect_data, args=(msg))
        thread.start()

    def collect_data(self, msg):
        global status_running
        while status_running:
            try:
                self.send_msg(msg)
                x = self.recv_msg()
                self.__data = [x["type"], x["value"], x["unit"]]
                self.__connection_status = "Connected"
            except:
                self.__connection_status = "Connection Lost!"
                t.sleep(5)
                self.establish_connection()


def clear_screen():
    if sys.platform == "linux":
        os.system("clear")
    elif sys.platform == "win32":
        os.system("cls")


def read_config():
    global sensors
    try:
        config_object = configparser.ConfigParser()
        config_object.read("centerConfig.conf")
        senfo = config_object["SENSORINFO"]
        sensor_names : list = list(senfo["name"].split(","))
        sensor_IPs : list = list(senfo["ip"].split(","))
        sensor_ports : list = list(senfo["port"].split(","))

        for count, name in enumerate(sensor_names):
            sensors.append(Sensor(name, sensor_IPs[count], int(sensor_ports[count])))

    except Exception:
        print("no configuration file found, enter senfo here manually:")
        senfo = [input("Sensorname: "), input("Sensor ip: "),input("Port to listen to: ")]
        config_object = configparser.ConfigParser()
        config_object["SENSORINFO"] = {
            "name" : senfo[0],
            "ip" :  senfo[1], 
            "port" : senfo[2]
        }

        with open("config.conf", 'w') as conf:
            config_object.write(conf)
        print("config has been stored in file for future use.")
        sensors.append(Sensor(senfo[0], senfo[1], int(senfo[2])))
    
    return "Schad"





if __name__ == "__main__":
    if sys.version_info < (3, 6):
        print("Es wird eine Python Version 3.6 oder höher benötigt!")
        quit()
    senfo = read_config()
    print("configuration found: ", senfo)
        
    
    try:
        for sensor in sensors:
            sensor.activate_sensor("1")
        while 1:
            clear_screen()
            try:
                for Sensor in sensors:
                    print(Sensor)
                    print("\n")
                t.sleep(1)
                clear_screen()
                pass
            except Exception:
                pass

    finally:
        for sensor in sensors:
            sensor.send_msg(DISCONNECT_MESSAGE)
        status_running = False