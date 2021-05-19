import socket
import msgpack
import threading
import time as t

FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!D"
statusRunning = True

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


    def activate_sensor(self, msg):
        self.establishConnection()
        thread = threading.Thread(target=self.collect_data, args=(msg))
        thread.start()

    def collect_data(self, msg):
        global statusRunning
        while statusRunning:
            self.send_msg(msg)
            x = self.recv_msg()
            self.addValue(x["value"])
            self.printValues()


if __name__ == "__main__":
    SensorMils = Sensor("Mils", "127.0.0.1", 5050)
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
