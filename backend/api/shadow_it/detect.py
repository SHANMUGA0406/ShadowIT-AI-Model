import json

def detect_shadow_it(devices):

    with open("shadow_it/approved_devices.json", "r") as file:
        approved_devices = json.load(file)

    for device in devices:

        device["status"] = "Shadow IT"

        for approved in approved_devices:

            if (
                device["mac"] == approved["mac"] and device["mac"] != ""
            ) or (
                device["hostname"] == approved["hostname"]
            ):

                device["status"] = "Authorized"
                break

    return devices