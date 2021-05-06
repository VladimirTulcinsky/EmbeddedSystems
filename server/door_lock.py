from device import Device

class DoorLock(Device):
    def __init__(self, name, location, id):
        super().__init__(name, location, id)
        self.locked = False

    def get_data(self):
        if self.locked:
            print("{} has registered a locked door".format(super(DoorLock,self).get_info(), self.locked))
        
        else:
            print("{} has registered an open door".format(super(DoorLock,self).get_info(), self.locked))
    
    def set_data(self):
        self.locked = not self.locked
        state = "closing" if self.locked else "opening"
        print("{} is now {} the door".format(super(DoorLock,self).get_info(), state))
