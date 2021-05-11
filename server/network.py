import socket
import service

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

def send_message(id, message):
    # Set IP to adress of a mote (id = network::id_of_mote)
    UDP_IP = "bbbb::c30c:0:0:{}".format(id)
    UDP_PORT = 3000
    message = bytes(format_data(message, "send"), "utf-8")
    sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
    sock.sendto(message, (UDP_IP, UDP_PORT))

# todo: update this method when format of protocol is decided
def format_data(device_message, status):
    formatted_message = None

    if status == "send":
        if isinstance(device_message, str):
            formatted_message = device_message
        elif isinstance(device_message, int):
            formatted_message = str(device_message)

    elif status == "recieve":
        if isinstance(device_message, str):
            formatted_message = int(device_message)
        elif isinstance(device_message, int):
            formatted_message = device_message

   
    
    return formatted_message