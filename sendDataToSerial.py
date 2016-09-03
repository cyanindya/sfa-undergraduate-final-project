# -*- coding: utf-8 -*-
"""
The module containing the function to send classification result
over serial communication.
"""

# Imports the pyserial module
import serial


# Defines a port to use for data transmission and opens said port.
def openPort(destinationPort, baudRate, timeout=None, portopen=True):
    ser = serial.Serial()

    ser.port = destinationPort
    ser.baudrate = baudRate
    ser.timeout = timeout

    if portopen:
        ser.open()

    return ser


# Sends data through previously-opened port.
def sendData(port, data):
    # Checks whether the port is open
    if port.is_open:
        port.write(b'%r' % data)  # write in byte
    else:
        pass

    # Closes the port after data transfer
    port.close()
