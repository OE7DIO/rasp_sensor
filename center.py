import serial
import time

ser = serial.Serial(
    port='COM3',\
    baudrate=9600,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
        timeout=0)


serCOM1 = serial.Serial(port='COM1', baudrate=9600, timeout=0)


print("connected to: " + ser.portstr)

while True:
    line = ser.read(10)

    print(line.decode("ascii"))
    time.sleep(1)
    

ser.close()

print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAaaaaaaa")