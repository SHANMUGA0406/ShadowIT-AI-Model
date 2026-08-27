def analyze_impact(device):

    impacts = []


    # Finance server impact
    if "finance" in device["hostname"].lower():
        impacts.append(
            "Financial Data Leakage Risk"
        )


    # Old Windows impact
    if "Windows7" in device.get("os", ""):
        impacts.append(
            "Malware Spread Risk"
        )


    # Medical device impact
    if "medical" in device["hostname"].lower():
        impacts.append(
            "Healthcare Compliance Risk"
        )


    # Shadow IT impact
    if device["status"] == "Shadow IT":
        impacts.append(
            "Unauthorized Access Risk"
        )


    # SMB port impact
    if 445 in device["ports"]:
        impacts.append(
            "Network Attack Risk"
        )


    return impacts



# Temporary Testing

test_device = {

    "hostname": "Finance-Server",

    "status": "Shadow IT",

    "os": "Windows7",

    "ports": [445,80]

}


result = analyze_impact(test_device)

print(result)