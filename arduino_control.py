from time import sleep
import serial


class Arduino:
    def __init__(self):
        # Establish the connection on a specific port
        self.ser = serial.Serial("/dev/cu.usbmodem141401", 9600)
        self.hidden = False

    # Show camera and send command to arduino servo
    def show(self):
        self.ser.write(str("s").encode())
        self.hidden = False

    # Hide camera and send command to arduino servo
    def hide(self):
        self.ser.write(str("h").encode())
        self.hidden = True

    # Returns status of our servo
    def isHidden(self):
        return self.hidden
