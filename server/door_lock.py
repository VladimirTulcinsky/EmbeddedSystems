from device import Device
import socket
import network

class DoorLock(Device):
    def __init__(self, name, location, id):
        super().__init__(name, location, id)
        self.locked = False
        self.id = id

    def get_data(self):
        if self.locked:
            print("{} has registered a locked door".format(super(DoorLock,self).get_info(), self.locked))
        
        else:
            print("{} has registered an open door".format(super(DoorLock,self).get_info(), self.locked))
    
    def update(self):
        self.locked = not self.locked
        state = "closing" if self.locked else "opening"
        print("{} is now {} the door".format(super(DoorLock,self).get_info(), state))
        message = 0 if self.locked else 1
        network.send_message(self.id, message, self)
