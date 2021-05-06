def show_interactive_ui(devices):
    for obj in devices:
        obj.get_data()

    while True:

        user_input = int(input("Which device id do you want to update? "))
        obj_to_update = next((obj for obj in devices if obj.id == user_input), None)
        obj_to_update.set_data()