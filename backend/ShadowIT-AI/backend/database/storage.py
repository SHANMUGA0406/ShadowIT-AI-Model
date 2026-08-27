devices_db = []


def save_devices(devices):

    global devices_db

    devices_db = devices

    for index, device in enumerate(devices_db):

        device["id"] = index + 1


    return devices_db



def get_devices():

    return devices_db



def get_device(device_id):

    for device in devices_db:

        if device["id"] == device_id:

            return device


    return None