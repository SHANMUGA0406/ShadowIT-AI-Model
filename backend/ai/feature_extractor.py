def extract_features(device):
    """
    Convert scanned device data into ML features.
    """

    # Unknown device
    if device["status"] == "Shadow IT":
        unknown_device = 1
    else:
        unknown_device = 0


    # Number of open ports
    open_port_count = len(device["ports"])


    # Critical CVE placeholder
    critical_cve_count = 0


    # Patch status
    # 1 = Updated
    # 0 = Outdated
    patch_status = 1


    # OS conversion
    os_value = device.get("os", "")

    if os_value == "":
        os_version = 0
    elif "Windows7" in os_value:
        os_version = 0
    elif "Windows10" in os_value:
        os_version = 1
    elif "Ubuntu20" in os_value:
        os_version = 2
    elif "Ubuntu22" in os_value:
        os_version = 3
    else:
        os_version = 0


    # Sensitive network placeholder
    sensitive_network_access = 0


    return {
        "unknown_device": unknown_device,
        "open_port_count": open_port_count,
        "critical_cve_count": critical_cve_count,
        "patch_status": patch_status,
        "os_version": os_version,
        "sensitive_network_access": sensitive_network_access
    }