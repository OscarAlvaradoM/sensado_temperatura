import serial
import time
from datetime import datetime

ser = serial.Serial('/dev/cu.usbserial-0001', 9600)  # cambia al puerto al que se esté conectando (COM3, COM4, etc. en Windows o /dev/ttyUSB0, /dev/ttyACM0, etc. en Linux)
time.sleep(2)

hour_register = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")

with open(f"../Data/temperatura_celular_{hour_register}.csv", "w") as f:
    while True:
        line = ser.readline().decode().strip()
        print(line)
        f.write(line + "\n")
