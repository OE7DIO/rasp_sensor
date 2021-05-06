import socket
import msgpack
import threading

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
        print(self.__listOfValues)
    


PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!D"
SERVER = "127.0.0.1"
ADDR = (SERVER, PORT)

SensorMils = Sensor("Mils", "127.0.0.1", 5050)

def activate_sensor(Sensor, msg):
    Sensor.establishConnection()
    thread = threading.Thread(target=collect_data, args=(msg, Sensor))
    thread.start()

def collect_data(msg, Sensor):

    while 1:
        Sensor.send_msg(msg)
        x = Sensor.recv_msg()
        Sensor.addValue(x["value"])
        Sensor.printValues()


try:
    activate_sensor(SensorMils, "a Fleischinger Kaas")
    #SensorMils.establishConnection()
    while 1:
        #collect_data("An schenen Messwert lieferns ma do!", SensorMils)
        t.sleep(10)
        pass

finally:
    send(DISCONNECT_MESSAGE, SensorMils)
