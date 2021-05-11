#!/usr/bin/env python3
from device import Device
from proximity_sensor import ProximitySensor
from noise_sensor import NoiseSensor
from lamp import Lamp
from door_lock import DoorLock
from network import run_server
import service
import ui
import time
import threading

def main():
    proximity_sensor = ProximitySensor("Proximus", "sas", 2)
    noise_sensor = NoiseSensor("Decibeau","safe", 3)
    lamp_actuator = Lamp("Pixar", "reception", 4)
    door_lock_actuator = DoorLock("Pandora", "safe", 5)

    # Share data between threads
    service.init([proximity_sensor, noise_sensor, lamp_actuator, door_lock_actuator])
    
    print("Starting server")
    thread = threading.Thread(target=run_server)
    thread.daemon = True
    thread.start()

    while True:
        device_to_update = ui.get_device_from_user(service.IoT_devices)
        device_to_update.update()


if __name__== "__main__":
    main()