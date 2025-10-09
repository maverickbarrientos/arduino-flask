import serial, time
arduino = serial.Serial('COM4', 9600)
time.sleep(2)
print("✅ Arduino connected.")
arduino.close()
