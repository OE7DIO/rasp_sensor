import RPi.GPIO as GPIO
import time
import random




def init_sensor():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(16, GPIO.OUT)
    GPIO.setup(20, GPIO.IN)
    GPIO.output(16, True)
    print("INIT Funktioniert")


def get_data():
    name = "Kontakt:"
    return [name, GPIO.input(20), ""]