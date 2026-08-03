import json
import os

def detect_shadow_it(devices):

    current_folder = os.path.dirname(__file__)
    json_file = os.path.join(current_folder, "approved_devices.json")

    with open(json_file, "r") as file:
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