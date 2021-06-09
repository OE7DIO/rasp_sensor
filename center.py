import socket
import msgpack
import threading
import time as t
import configparser
import os

FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!D"
statusRunning = True
Sensors=[]

class Sensor():
    def __init__(self, name, ip, port):
        self.__name = name
        self.__address = (ip, port)
        self.__data = []
    
    def __str__(self):
        print(f"Sensor {self.__name}:")
        x = ""
        for count, value in enumerate(self.__data[1]):
            x = x + f"{self.__data[0][count]}: {value} {self.__data[2][count]}"
            for i in range(40*(count+1) - len(x)):
                x = x +" "
        return x

    def establishConnection(self):
        while statusRunning:
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
        self.establishConnection()
        thread = threading.Thread(target=self.collect_data, args=(msg))
        thread.start()

    def collect_data(self, msg):
        global statusRunning
        while statusRunning:
            try:
                self.send_msg(msg)
                x = self.recv_msg()
                self.__data = [x["type"], x["value"], x["unit"]]
            except:
                t.sleep(5)
                self.establishConnection()





def read_config():
    global Sensors
    try:
        config_object = configparser.ConfigParser()
        config_object.read("centerConfig.conf")
        senfo = config_object["SENSORINFO"]
        SensorNames : list = list(senfo["name"].split(","))
        SensorIPs : list = list(senfo["ip"].split(","))
        SensorPorts : list = list(senfo["port"].split(","))

        for count, name in enumerate(SensorNames):
            Sensors.append(Sensor(name, SensorIPs[count], int(SensorPorts[count])))

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
        Sensors.append(Sensor(senfo[0], senfo[1], int(senfo[2])))
    
    return "Schad"





if __name__ == "__main__":
    senfo = read_config()
    print("configuration found: ", senfo)
        
    
    try:
        for sensor in Sensors:
            sensor.activate_sensor("1")
        while 1:
            try:
                for Sensor in Sensors:
                    print(Sensor)
                t.sleep(1)
                os.system('cls')
                pass
            except Exception:
                pass

    finally:
        for sensor in Sensors:
            sensor.send_msg(DISCONNECT_MESSAGE)
        statusRunning = False