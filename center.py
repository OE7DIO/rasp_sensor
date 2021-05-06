import socket
import msgpack
import threading

class Sensor():
    def __init__(self, name):
        self.__name = name
        self.__listOfValues = []
    
    def addValue(self, newValue):
        self.__listOfValues.append(newValue)

    def printValues(self):
        print(self.__listOfValues)

PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!D"
SERVER = "127.0.0.1"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

SensorMils = Sensor("Mils")

def send(msg, Sensor):
    message = msg.encode(FORMAT)
    client.send(message)

    unpacker = msgpack.Unpacker()
    buffer = client.recv(4096)
    unpacker.feed(buffer)
    for d in unpacker:
        x = d
    print(x)
    Sensor.addValue(x["value"])
    Sensor.printValues()


try:
    while 1:
        send("An schenen Messwert lieferns ma do!", SensorMils)

finally:
    send(DISCONNECT_MESSAGE)
