from device import Device

class TemperatureSensor(Device):
    def __init__(self, name, location, id):
        super().__init__(name, location, id)
        self.temperature = 1000

    def get_data(self):
        print("{} has registered a temperature of {}°C".format(super(TemperatureSensor,self).get_info(), self.temperature))
        