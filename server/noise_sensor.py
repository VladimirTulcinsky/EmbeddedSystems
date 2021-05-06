from device import Device

class NoiseSensor(Device):
    def __init__(self, name, location, id):
        super().__init__(name, location, id)
        self.dBA = 50

    def get_data(self):
        if self.dBA > 90:
            print("{} has registered that noise treshold has been exceeded with {} dBA".format(super(NoiseSensor,self).get_info(), self.dBA))
        
        else:
            print("{}: everything is fine, currently registering {} dBA".format(super(NoiseSensor,self).get_info(), self.dBA))

    def update(self):
        print("You have subscribed to {}. Once noise data is sent, you'll be noticed".format(super(NoiseSensor,self).get_info().lower()))