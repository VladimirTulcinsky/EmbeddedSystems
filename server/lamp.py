from device import Device

class Lamp(Device):
    def __init__(self, name, location, id):
        super().__init__(name, location, id)
        self.on = False

    def get_data(self):
        if self.on:
            print("{} has the light on".format(super(Lamp,self).get_info(), self.on))
        
        else:
            print("{} has the light off".format(super(Lamp,self).get_info(), self.on))
    
    def set_data(self):
        self.on = not self.on
        state = "lighting" if self.on else "switching off"
        print("{} is now {} the lamp".format(super(Lamp,self).get_info(), state))