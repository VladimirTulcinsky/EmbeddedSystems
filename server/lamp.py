from device import Device
import socket
from network import send_message

class Lamp(Device):
    def __init__(self, name, location, id):
        super().__init__(name, location, id)
        self.on = False
        self.id = id

    def get_data(self):
        if self.on:
            print("{} has the light on".format(super(Lamp,self).get_info(), self.on))
        
        else:
            print("{} has the light off".format(super(Lamp,self).get_info(), self.on))
    
    def update(self):
        self.on = not self.on
        message = 1 if self.on else 0
        send_message(self.id, message)
        state = "lighting" if self.on else "switching off"
        print("{} is now {} the lamp".format(super(Lamp,self).get_info(), state))