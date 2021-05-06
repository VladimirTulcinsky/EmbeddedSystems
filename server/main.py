#!/usr/bin/env python3
import socket
from device import Device
from temperature_sensor import TemperatureSensor
from noise_sensor import NoiseSensor
from lamp import Lamp
from door_lock import DoorLock
import ui

def main():
    temperature_sensor = TemperatureSensor("Damsecho", "locker room", 1)
    noise_sensor = NoiseSensor("Decibeau","dancefloor", 2)
    lamp_actuator = Lamp("Pixar", "restroom", 3)
    door_lock_actuator = DoorLock("Pandora", "safe", 4)

    IoT_objects = [temperature_sensor, noise_sensor, lamp_actuator, door_lock_actuator]

    ui.show_interactive_ui(IoT_objects)

    # UDP_IP = "bbbb::1"
    # UDP_PORT = 5678

    # sock = socket.socket(socket.AF_INET6, # Internet
    #                      socket.SOCK_DGRAM) # UDP
    # sock.bind((UDP_IP, UDP_PORT))

    # while True:
    #     data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    #     print("received message: %s" % data)


if __name__== "__main__":
    main()