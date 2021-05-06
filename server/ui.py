def show_devices(devices):
    print("*****************************")
    for obj in devices:
        obj.get_data()
    print("*****************************")

def get_device_from_user(devices):
    obj_to_update = None
    show_devices(devices)
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