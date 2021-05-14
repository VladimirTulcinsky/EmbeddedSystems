from device import Device


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

    def set_data(self, new_status):
        self.on = new_status
        self.get_data()
    
    def update(self):
        message = "0" if self.on else "1"
        state = "switching off" if self.on else "lighting"
        print("{} is now {} the lamp".format(super(Lamp,self).get_info(), state))

        
        return message
        

      