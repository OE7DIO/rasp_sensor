import serial
import time

class Sensor():
    def __init__(self):
        self.wertetabelle = []
    
    def appendwertetabelle(self, newTemp):
        self.wertetabelle.append(newTemp)

ser = serial.Serial(port='COM3', baudrate=9600, timeout=0)

serCOM1 = serial.Serial(port='COM1', baudrate=9600, timeout=0)

print("connected to: " + ser.portstr)


SensorCOM3 = Sensor()

while True:
    line = ser.readline()
    line = line.decode("ascii")
    a = line.split()

    try: 
        if a[0] == "SensorCOM3":
            print(line)
            line = line.split()
            a = line[0] + ".appendwertetabelle(" + line[1] + ")"
            eval(a)
            print(SensorCOM3.wertetabelle)

        elif line != " $":
            print(line)

    except:
        continue
    time.sleep(0.4)
    

ser.close()

print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAaaaaaaa")