def show_devices(devices):
    devices_info = []
    for obj in devices:
        devices_info.append(obj.get_info())
    pretty_print(devices_info)   

def pretty_print(txt):
    print("\n")
    print("ALL DEVICES:")
    print("*****************************")
    if isinstance(txt, list):
        for item in txt:
            print(item)
    else:
        print(txt)
    print("*****************************")
    print("\n")

def get_device_from_user(devices):
    show_devices(devices)
    obj_to_update = None
    while not obj_to_update:      
        user_input = int(input("Which device id do you want to update? "))
        obj_to_update = next((obj for obj in devices if obj.id == user_input), None)
        if not obj_to_update:
            print("\n")
            print("This device doesn't exist, choose another one!")
            show_devices(devices)
    else:
        print("\n")
        return obj_to_update

