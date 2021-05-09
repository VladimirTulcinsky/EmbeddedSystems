#!/usr/bin/env python3
from device import Device
from temperature_sensor import TemperatureSensor
from noise_sensor import NoiseSensor
from lamp import Lamp
from door_lock import DoorLock
import ui
import time
import socket
import threading

IoT_devices = []

def run_server():
    global IoT_devices
    UDP_IP = "bbbb::1"
    UDP_PORT = 5678

    sock = socket.socket(socket.AF_INET6, # Internet
                            socket.SOCK_DGRAM) # UDP
    sock.bind((UDP_IP, UDP_PORT))

    while True:
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        # print("received message: {}".format(data.decode('utf-8')))
        # print("received addr: {}".format(addr[0]))
        device_id = addr[0].rsplit(':', 1)[-1]
        device_message = data.decode('utf-8').rsplit('=', 1)[-1]
        # print("dev id", device_id)
        # print("dev message", device_message)
        obj_to_update = get_device_with_id(device_id)
        obj_to_update.set_data(format_data(device_message))


def get_device_with_id(id):
    return next((obj for obj in IoT_devices if obj.id == int(id)), None)

# todo: update this method when format of protocol is decided
def format_data(device_message):
    formatted_message = None

    if isinstance(device_message, str):
        formatted_message = int(device_message)
    elif isinstance(device_message, int):
        formatted_message = device_message
    
    return formatted_message

def main():
    temperature_sensor = TemperatureSensor("Damsecho", "locker room", 1)
    noise_sensor = NoiseSensor("Decibeau","dancefloor", 2)
    lamp_actuator = Lamp("Pixar", "restroom", 3)
    door_lock_actuator = DoorLock("Pandora", "safe", 4)

    # Share data between threads
    global IoT_devices
    IoT_devices = [temperature_sensor, noise_sensor, lamp_actuator, door_lock_actuator]
    
    print("Starting server")
    thread = threading.Thread(target=run_server)
    thread.daemon = True
    thread.start()

    while True:
        device_to_update = ui.get_device_from_user(IoT_devices)
        device_to_update.update()


if __name__== "__main__":
    main()