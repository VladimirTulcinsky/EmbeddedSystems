import socket

UDP_IP = "bbbb::1"
UDP_PORT = 5678

sock = socket.socket(socket.AF_INET6, # Internet
                        socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    print("received message: %s" % data)