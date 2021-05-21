import socket
import msgpack
import threading
import time as t
import configparser

FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!D"
statusRunning = True
Sensors=[]

class Sensor():
    def __init__(self, name, ip, port):
        self.__name = name
        self.__address = (ip, port)
        self.__listOfValues = []
    
    def establishConnection(self):
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__sock.connect(self.__address)
    
    def send_msg(self, msg):
        message = msg.encode(FORMAT)
        self.__sock.send(message)
    
    def recv_msg(self):
        self.__unpacker = msgpack.Unpacker()
        self.__buffer = self.__sock.recv(4096)
        self.__unpacker.feed(self.__buffer)
        for x in self.__unpacker:
            return x
    
    def addValue(self, newValue):
        self.__listOfValues.append(newValue)

    def printValues(self):
        print(self.__listOfValues[-1])


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
                self.addValue(x["value"])
                self.printValues()
            except:
                t.sleep(5)
                self.establishConnection()

def read_config():
    config_object = configparser.ConfigParser()
    config_object.read("config.config")
    senfo = config_object["SENSORINFO"]
    SensorNames : list = list(senfo["name"].split(","))
    SensorIPs : list = list(senfo["ip"].split(","))
    SensorPorts : list = list(senfo["port"].split(","))

    for count, name in enumerate(SensorNames):
        tempSensor = [name, SensorIPs[0], SensorPorts[0]]
        Sensors.append(tempSensor)
        






    senfo = [senfo["name"], senfo["ip"], senfo["port"]]

    
    return senfo

if __name__ == "__main__":
    try:
        senfo = read_config()
        print("configuration found: ", senfo)
        
    except Exception:
        print("no configuration file found, enter senfo here manually:")
        senfo = [input("Sensorname: "), input("Sensor ip: "),input("Port to listen to: ")]
        config_object = configparser.ConfigParser()
        config_object["senfo"] = {
            "name" : senfo[0],
            "ip" :  senfo[1], 
            "port" : senfo[2]
        }

        with open("config.config", 'w') as conf:
            config_object.write(conf)
        print("config has been stored in file for future use.")

    #print(Sensors[4][0], Sensors[4][1], Sensors[4][2])
    SensorMils = Sensor(str((Sensors[0])[0]), str((Sensors[0])[1]), int((Sensors[0])[2]))
    
    #SensorMils = Sensor("Mils", "127.0.0.1", 5050)
    #SensorHall = Sensor("Mils", "127.0.0.1", 5051)
    try:
        SensorMils.activate_sensor("1")
        #SensorHall.activate_sensor("mit Senf Bitte")
        while 1:
            t.sleep(10)
            pass

    finally:
        SensorMils.send_msg(DISCONNECT_MESSAGE)
        #SensorHall.send_msg(DISCONNECT_MESSAGE)
        statusRunning = False