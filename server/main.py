#!/usr/bin/env python3
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

    IoT_devices = [temperature_sensor, noise_sensor, lamp_actuator, door_lock_actuator]

    while True:
        device_to_update = ui.get_device_from_user(IoT_devices)
        device_to_update.update()


if __name__== "__main__":
    main()