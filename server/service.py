def init(devices):
    global IoT_devices
    IoT_devices = devices
    global sequence_number
    sequence_number = 1
    global MAX_SEQUENCE_BITS
    MAX_SEQUENCE_BITS = 8
    global MAX_PAYLOAD_BITS
    MAX_PAYLOAD_BITS = 10
