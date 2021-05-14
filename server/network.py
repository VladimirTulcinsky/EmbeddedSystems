import socket
import service
import random
import string
# import lamp as lp
# import proximity_sensor as ps
# import noise_sensor as ns
# import door_lock as dl

from proximity_sensor import ProximitySensor
from noise_sensor import NoiseSensor
from lamp import Lamp
from door_lock import DoorLock
from ui import show_devices


def run_server():
    # for i in range(4):
    #     if i == 0:
    #         device_message = bytes("C04801", "utf-8")
    #     if i == 1:
    #         device_message = bytes("404800", "utf-8")
    #     device_id = 2
    #     formatted_data = format_data(device_message, "recieve", device_id)
    #     obj_to_update = get_device_with_id(device_id)
    #     if obj_to_update:
    #         obj_to_update.set_data(formatted_data)
    while(True):
        UDP_IP = "bbbb::1"
        UDP_PORT = 5678

        sock = socket.socket(socket.AF_INET6, # Internet
                                socket.SOCK_DGRAM) # UDP
        sock.bind((UDP_IP, UDP_PORT))

        while True:
            data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
            # print("received message: {}".format(data.decode('utf-8')))
            # print("received addr: {}".format(addr[0]))
            device_id = addr[0].rsplit(':', 1)[-1]
            # device_message = data.decode('utf-8').rsplit('=', 1)[-1]
            device_message = data.decode('utf-8')
            # print("dev id", device_id)
            # print("dev message", device_message)
            formatted_data = format_receiving_data(device_message, device_id)
            obj_to_update = get_device_with_id(device_id)
            if obj_to_update:
                obj_to_update.set_data(formatted_data)


def get_device_with_id(id):
    return next((obj for obj in service.IoT_devices if obj.id == int(id)), None)

# length signifies the number of bytes, thus needs to be multiplied by two, to compare to len(hex_str) which will count every character, so two characters per byte
def bin2hex(binstr, length_in_bytes): 
    # print(int( binstr, 2))
    nb_hex_characters = length_in_bytes * 2
    hex_str = hex(int(binstr, 2))[2:] 
    if len(hex_str) < nb_hex_characters:
        padding = nb_hex_characters - len(hex_str)
        hex_str = padding *'0'+hex_str
    return hex_str

def hex2bin(data_to_format):
    scale = 16 ## equals to hexadecimal
    num_of_bits = 24
    return bin(int(data_to_format, scale))[2:].zfill(num_of_bits)

def bin2dec(binary_string):
    return int(binary_string,2)

def send_message(id, message, device=None):
    # Set IP to adress of a mote (id = network::id_of_mote)
    UDP_IP = "bbbb::c30c:0:0:{}".format(id)
    UDP_PORT = 3000
    message = bytes(format_sending_data(message, id, device), "utf-8")
    # print("message = ", message)
    sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
    sock.sendto(message, (UDP_IP, UDP_PORT))


# 2 bits
def get_type_response(device=None):
    conf = ""
    if device:
        if isinstance(device, ProximitySensor):
            conf = "01"
        elif isinstance(device, NoiseSensor):
            conf = "01"
        elif isinstance(device, Lamp):
            conf = "00"
        elif isinstance(device, DoorLock):
            conf = "00"
    else:
        conf = "01"
    
    return conf
        
# 8 bits
def get_sequence():
    value = service.sequence_number
    bin_value = str(bin(value))[2:]
    if len(bin_value) < service.MAX_SEQUENCE_BITS:
        padding = service.MAX_SEQUENCE_BITS - len(bin_value)
        bin_value = padding *'0'+bin_value
    service.sequence_number =+1 
    if service.sequence_number == 256:
        service.sequence_number = 0
    return bin_value

# 4 bits
def get_type_of_data(device=None):
    type_of_data = ""
    if device:
        if isinstance(device, ProximitySensor):
            type_of_data = "0000"
        elif isinstance(device, NoiseSensor):
            type_of_data = "0001"
        elif isinstance(device, Lamp):
            type_of_data = "0010"
        elif isinstance(device, DoorLock):
            type_of_data = "0011"
    # 1111 is the server
    else:
        type_of_data = "1111"
    
    return type_of_data

# 10 bits
def padd_message(message):
    return "{0:010b}".format(message)    
    
def handle_type_response(binary_str, id):
    type_of_response = binary_str[0:2]
    # Mote requests ack from server
    if type_of_response == "00":
        # send message with ack
        send_message(id,0)

    # Mote requests ack from server
    elif type_of_response == "01":
        # send message with ack
        pass

    elif type_of_response == "10":
        pass

    # The mote wants to create an object
    elif type_of_response == "11":
        create_new_device(binary_str,id)
        send_message(id,1023)

def set_sequence(binary_str):
    # Convert binary sequence number to decimal number
    service.sequence_number = bin2dec(binary_str[2:10])

# The type of data for the server is 1111
# TYPE OF DATA:
# 0000 = proximity
# 0001 = noise 
# 0010 = lamp 
# 0011 = lock 


def handle_type_data_and_payload(binary_str):
    type_data = binary_str[10:14]
    payload = binary_str[14:24]
    data_for_device = None
    payload = bin2dec(payload)
    # proximity or noise
    if type_data == "0000" or type_data == "0001":
        return payload
    # lamp
    elif type_data == "0010":
        if payload != (0 or 1):
            return 0
    # doorlock
    elif type_data == "0011":
        #TODO: update with pin code
        if payload != (0 or 1):
            return 0
    return payload
        


def get_random_name():
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(10))

def get_random_location():
    locations = ['sas', 'kitchen', 'safe','attic','bedroom','locker','wc']
    return random.choice(locations)

def create_new_device(binary_str, id):
    device = get_device_with_id(id)
    if not device:
        type_of_data = binary_str[10:14] 
        new_device = None
        new_name = get_random_name()
        new_location = get_random_location()

        # The mote is a proximity sensor
        if type_of_data == "0000":
            new_device = ProximitySensor(new_name, new_location, int(id))

        # The mote is a noise sensor
        elif type_of_data == "0001":
            new_device = NoiseSensor(new_name, new_location, int(id))

        # The mote is a lamp
        elif type_of_data == "0010":
            new_device = Lamp(new_name, new_location, int(id))

        # The mote is a doorlock
        elif type_of_data == "0011":
            new_device = DoorLock(new_name, new_location, int(id))
        
        else:
            pass

        service.IoT_devices.append(new_device)
        show_devices()

    

def format_sending_data(device_message, device_id=None, device=None):

    formatted_message = ""

    # the binary string that combines the protocol (type of response(2), sequence (8), type of data (4)) with the payload (10)
    binary_str = "{}{}{}{}".format(get_type_response(device), get_sequence(),get_type_of_data(device), padd_message(device_message))   
    formatted_message = bin2hex(binary_str, 3)

    return formatted_message

def format_receiving_data(device_message, device_id=None, device=None):

    formatted_message = ""

    binary_str = hex2bin(device_message)
    
    handle_type_response(binary_str,device_id)
    formatted_message = handle_type_data_and_payload(binary_str) 

    return formatted_message

def prepare_server_response():
    pass

# Receives hex
# convert to binary string
# def receiving_data_handler(device_message, device_id=None):

#     formatted_message = ""

#     binary_str = hex2bin(device_message)
    
#     # Gets int for noise
#     # Gets true or false for other devices
#     # formatted_message = handle_type_data_and_payload(binary_str) 



#     type_of_response = binary_str[0:2] 
#     sequence_number = binary_str[2:10]
#     type_of_data = binary_str[10:14] 
#     payload = binary_str[14:24]

#     # if type_of_response needs no ack or is an ack message
#     if type_of_response == "01" or type_of_response == "10":
#         return

#     # Preparing response from the server to the mote
#     # response_type_of_response = handle_type_response(type_of_response)
#     response_sequence_number = service.sequence_number
#     response_type_of_data = handle_type_data(type_of_data, device_id)
#     response_payload = handle_payload(type_of_data)
#     # response_type_of_response = handle_type_response(type_of_response)
    
    
#     # Updates the current sequence number with
#     # set_sequence()

#     return formatted_message

