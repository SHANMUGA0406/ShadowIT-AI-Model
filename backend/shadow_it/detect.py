import json
import os


def detect_shadow_it(devices):
    """
    Compare discovered devices with approved devices
    and identify Shadow IT devices.
    """

    # Get the location of approved_devices.json
    current_folder = os.path.dirname(__file__)

    json_file = os.path.join(
        current_folder,
        "approved_devices.json"
    )

    # Load approved devices
    with open(json_file, "r") as file:
        approved_devices = json.load(file)

    # Check every discovered device
    for device in devices:

        # Assume device is Shadow IT
        device["status"] = "Shadow IT"

        # Compare with approved devices
        for approved in approved_devices:

            # Match using MAC address
            mac_match = (
                device.get("mac", "") != ""
                and device.get("mac", "") == approved.get("mac", "")
            )

            # Match using hostname
            hostname_match = (
                device.get("hostname", "")
                == approved.get("hostname", "")
            )

            # If either matches, authorize the device
            if mac_match or hostname_match:

                device["status"] = "Authorized"

                break

    return devices