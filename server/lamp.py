from device import Device
import socket
import network

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

    def set_data(self):
        pass
        # self.on = not self.on
        # state = "lighting" if self.on else "switching off"
        # print("{} is now {} the lamp".format(super(Lamp,self).get_info(), state))
    
    def update(self):
        # self.on = not self.on
        message = 0 if self.on else 1
        network.send_message(self.id, message, self)
        # state = "lighting" if self.on else "switching off"
        # print("{} is now {} the lamp".format(super(Lamp,self).get_info(), state))