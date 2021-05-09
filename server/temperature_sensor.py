from device import Device

class TemperatureSensor(Device):
    def __init__(self, name, location, id):
        super().__init__(name, location, id)
        self.temperature = 1000
        self.subscribed = False

    def get_data(self):
        print("{} has registered a temperature of {}°C".format(super(TemperatureSensor,self).get_info(), self.temperature))
        
    def set_data(self, new_temperature):
        self.temperature = new_temperature

    def update(self):
        self.subscribed = not self.subscribed
        if self.subscribed:
            print("You have subscribed to {}. Once temperature data is sent, you'll be noticed".format(super(TemperatureSensor,self).get_info().lower()))
            self.get_data()
        else:
            print("You have unsubscribed to {}. Data will not be sent anymore".format(super(TemperatureSensor,self,self).get_info().lower()))    