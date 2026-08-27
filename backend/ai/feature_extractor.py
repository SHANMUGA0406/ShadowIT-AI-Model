# ============================================================
# SHADOW IT AI
# FEATURE EXTRACTION
# ============================================================

def extract_features(device):
    """
    Convert discovered device information into
    the exact feature format expected by the final ML model.
    """

    # --------------------------------------------------------
    # 1. UNKNOWN DEVICE
    # --------------------------------------------------------

    if device.get("status") == "Shadow IT":
        unknown_device = 1
    else:
        unknown_device = 0

    # --------------------------------------------------------
    # 2. OPEN PORT COUNT
    # --------------------------------------------------------

    ports = device.get("ports", [])

    open_port_count = len(ports)

    # --------------------------------------------------------
    # 3. CRITICAL CVE COUNT
    # --------------------------------------------------------
    # Current prototype does not yet perform real CVE lookup.
    # Keep this as a safe default until vulnerability
    # enrichment is connected.

    critical_cve_count = int(
        device.get("critical_cve_count", 0)
    )

    # --------------------------------------------------------
    # 4. PATCH STATUS
    # --------------------------------------------------------
    # 1 = Updated
    # 0 = Outdated

    patch_status = device.get(
        "patch_status",
        1
    )

    if isinstance(patch_status, bool):
        patch_status = int(patch_status)

    elif isinstance(patch_status, str):

        normalized = patch_status.strip().lower()

        if normalized in [
            "updated",
            "update",
            "patched",
            "patch",
            "yes",
            "true",
            "1"
        ]:
            patch_status = 1

        elif normalized in [
            "outdated",
            "unpatched",
            "not patched",
            "no",
            "false",
            "0"
        ]:
            patch_status = 0

        else:
            patch_status = 1

    patch_status = int(patch_status)

    # --------------------------------------------------------
    # 5. OS OUTDATED
    # --------------------------------------------------------
    # IMPORTANT:
    # The final model expects os_outdated.
    #
    # 1 = outdated
    # 0 = not outdated

    if "os_outdated" in device:

        os_outdated = device["os_outdated"]

        if isinstance(os_outdated, bool):
            os_outdated = int(os_outdated)

        elif isinstance(os_outdated, str):

            normalized = (
                os_outdated
                .strip()
                .lower()
            )

            if normalized in [
                "yes",
                "true",
                "outdated",
                "1"
            ]:
                os_outdated = 1

            else:
                os_outdated = 0

        os_outdated = int(os_outdated)

    else:

        os_value = str(
            device.get("os", "")
        ).strip().lower()

        # Known outdated operating systems
        outdated_os = [
            "windows 7",
            "windows7",
            "windows xp",
            "windowsxp",
            "windows vista",
            "windowsvista",
            "ubuntu 18",
            "ubuntu18",
            "ubuntu 16",
            "ubuntu16"
        ]

        os_outdated = 0

        for old_os in outdated_os:

            if old_os in os_value:

                os_outdated = 1
                break

    # --------------------------------------------------------
    # 6. SENSITIVE NETWORK ACCESS
    # --------------------------------------------------------

    sensitive_network_access = device.get(
        "sensitive_network_access",
        0
    )

    if isinstance(
        sensitive_network_access,
        bool
    ):

        sensitive_network_access = int(
            sensitive_network_access
        )

    elif isinstance(
        sensitive_network_access,
        str
    ):

        normalized = (
            sensitive_network_access
            .strip()
            .lower()
        )

        if normalized in [
            "yes",
            "true",
            "1"
        ]:

            sensitive_network_access = 1

        else:

            sensitive_network_access = 0

    sensitive_network_access = int(
        sensitive_network_access
    )

    # --------------------------------------------------------
    # FINAL FEATURE VECTOR
    # --------------------------------------------------------

    features = {

        "unknown_device":
            unknown_device,

        "open_port_count":
            open_port_count,

        "critical_cve_count":
            critical_cve_count,

        "patch_status":
            patch_status,

        "os_outdated":
            os_outdated,

        "sensitive_network_access":
            sensitive_network_access

    }

    return features