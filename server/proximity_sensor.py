from device import Device

class ProximitySensor(Device):
    def __init__(self, name, location, id):
        super().__init__(name, location, id)
        self.proximity = False
        self.subscribed = False

    def get_data(self):
        if self.proximity:
            print("{} has detected a movement".format(super(ProximitySensor,self).get_info(), self.proximity))
        else:
            print("{} has not detected any movement".format(super(ProximitySensor,self).get_info(), self.proximity))
    
    def set_data(self, new_proximity):
        self.proximity = new_proximity
        if self.proximity and self.subscribed:
            self.get_data()

    def update(self):
        self.subscribed = not self.subscribed
        if self.subscribed:
            print("You have subscribed to {}. Once movement is detected, you'll be noticed".format(super(ProximitySensor,self).get_info().lower()))
            self.get_data()
        else:
            print("You have unsubscribed to {}. Data will not be sent anymore".format(super(ProximitySensor,self).get_info().lower()))    