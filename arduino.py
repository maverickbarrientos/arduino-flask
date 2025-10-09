import serial
import json
import time

def arduino(port='COM4', baud=9600):
    return serial.Serial(port, baud)