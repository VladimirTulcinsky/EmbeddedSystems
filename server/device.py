class Device:

    def __init__(self, name, location, id):
        self.name = name
        self.location = location
        self.id = id

    def get_info(self):
        return "Device '{}' with id {} located in {}".format(self.name, self.id, self.location)