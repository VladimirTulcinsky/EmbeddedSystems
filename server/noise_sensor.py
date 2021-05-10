from device import Device

class NoiseSensor(Device):
    def __init__(self, name, location, id):
        super().__init__(name, location, id)
        self.dBA = 50
        self.subscribed = False

    def get_data(self):
        if self.dBA > 90:
            print("{} has registered that noise treshold has been exceeded with {} dBA".format(super(NoiseSensor,self).get_info(), self.dBA))
        
        else:
            print("{}: everything is fine, currently registering {} dBA".format(super(NoiseSensor,self).get_info(), self.dBA))

    def set_data(self, new_noise):
        self.dBA = new_noise
        if self.subscribed:
            self.get_data()

    def update(self):
        self.subscribed = not self.subscribed
        if self.subscribed:
            print("You have subscribed to {}.".format(super(NoiseSensor,self).get_info().lower()))
            self.get_data()
        else:
            print("You have unsubscribed to {}. Data will not be sent anymore".format(super(NoiseSensor,self).get_info().lower()))