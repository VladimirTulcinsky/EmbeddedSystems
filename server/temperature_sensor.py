from device import Device

class TemperatureSensor(Device):
    def __init__(self, name, location, id):
        super().__init__(name, location, id)
        self.temperature = 1000

    def get_data(self):
        print("{} has registered a temperature of {}°C".format(super(TemperatureSensor,self).get_info(), self.temperature))
        

    def update(self):
        print("You have subscribed to {}. Once temperature data is sent, you'll be noticed".format(super(TemperatureSensor,self).get_info().lower()))