import socket
import service
import lamp as lp
import proximity_sensor as ps
import noise_sensor as ns
import door_lock as dl


def run_server():
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
        device_message = data.decode('utf-8').rsplit('=', 1)[-1]
        # print("dev id", device_id)
        # print("dev message", device_message)
        obj_to_update = get_device_with_id(device_id)
        obj_to_update.set_data(format_data(device_message, "recieve"))


def get_device_with_id(id):
    return next((obj for obj in service.IoT_devices if obj.id == int(id)), None)

# length signifies the number of bytes, thus needs to be multiplied by two, to compare to len(hex_str) which will count every character, so two characters per byte
def bin2hex(binstr, length_in_bytes): 
    print(int( binstr, 2))
    nb_hex_characters = length_in_bytes * 2
    hex_str = hex(int(binstr, 2))[2:] 
    if len(hex_str) < nb_hex_characters:
        padding = nb_hex_characters - len(hex_str)
        hex_str = padding *'0'+hex_str
    return hex_str

def send_message(id, message, device):
    # Set IP to adress of a mote (id = network::id_of_mote)
    UDP_IP = "bbbb::c30c:0:0:{}".format(id)
    UDP_PORT = 3000
    message = bytes(format_data(message, "send", device), "utf-8")
    print("message = ", message)
    sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
    sock.sendto(message, (UDP_IP, UDP_PORT))

# 2 bits
def get_type_device(device):
    conf = ""
    if isinstance(device, ps.ProximitySensor):
        conf = "01"
    if isinstance(device, ns.NoiseSensor):
        conf = "01"
    if isinstance(device, lp.Lamp):
        conf = "00"
    if isinstance(device, dl.DoorLock):
        conf = "00"
    
    return conf
        
# 10 bits
def get_sequence():
    value = service.sequence_number
    bin_value = str(bin(value))[2:]
    if len(bin_value) < 10:
        padding = 10 - len(bin_value)
        bin_value = padding *'0'+bin_value
    service.sequence_number =+1 
    return bin_value

# 4 bits
def get_type_of_data(device):
    conf = ""
    if isinstance(device, ps.ProximitySensor):
        conf = "0000"
    if isinstance(device, ns.NoiseSensor):
        conf = "0001"
    if isinstance(device, lp.Lamp):
        conf = "0010"
    if isinstance(device, dl.DoorLock):
        conf = "0011"
    
    return conf
    
def padd_message(message):
    return_value = str(message)
    if len(return_value) < 8:
        padding = 8 - len(return_value)
        return_value = padding *'0'+str(message)
        print('return value: ' + return_value)
    
    return return_value
    



# todo: update this method when format of protocol is decided
def format_data(device_message, status, device=None):

    formatted_message = ""

    if status == "send":
        # the binary string that combines the protocol (type (2), sequence (10), type of data (4)) with the payload (8)
        binary_str = "{}{}{}{}".format(get_type_device(device), get_sequence(),get_type_of_data(device), padd_message(device_message))   
        formatted_message = bin2hex(binary_str, 3)

    elif status == "recieve":
        if isinstance(device_message, str):
            formatted_message = int(device_message)
        elif isinstance(device_message, int):
            formatted_message = device_message

   
    
    return formatted_message