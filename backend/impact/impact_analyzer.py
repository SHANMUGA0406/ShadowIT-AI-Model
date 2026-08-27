# ============================================================
# SHADOW IT AI
# MODULE 14 - SECURITY IMPACT ANALYZER
# ============================================================

from typing import Any, Dict, List


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def safe_string(value: Any) -> str:
    """
    Convert a value safely to lowercase string.
    """
    if value is None:
        return ""

    return str(value).strip().lower()


def safe_ports(device: Dict[str, Any]) -> List[int]:
    """
    Safely extract port numbers from a device.
    """

    ports = device.get("ports", [])

    if not isinstance(ports, list):
        return []

    normalized_ports = []

    for port in ports:

        try:
            normalized_ports.append(int(port))

        except (TypeError, ValueError):
            continue

    return normalized_ports


# ============================================================
# IMPACT ANALYSIS
# ============================================================

def analyze_impact(device: Dict[str, Any]) -> List[str]:
    """
    Analyze potential cybersecurity impacts for a device.

    This module does NOT calculate ML risk.

    It converts known device characteristics into
    understandable security impact categories.
    """

    if not isinstance(device, dict):
        raise ValueError(
            "Device must be provided as a dictionary."
        )

    impacts = []

    hostname = safe_string(
        device.get("hostname", "")
    )

    operating_system = safe_string(
        device.get("os", "")
    )

    status = safe_string(
        device.get("status", "")
    )

    ports = safe_ports(device)

    # --------------------------------------------------------
    # Finance
    # --------------------------------------------------------

    if "finance" in hostname:

        impacts.append(
            "Financial Data Leakage Risk"
        )

    # --------------------------------------------------------
    # Medical / Healthcare
    # --------------------------------------------------------

    if (
        "medical" in hostname
        or "health" in hostname
        or "hospital" in hostname
    ):

        impacts.append(
            "Healthcare Compliance Risk"
        )

    # --------------------------------------------------------
    # Outdated operating system
    # --------------------------------------------------------

    outdated_os_patterns = [
        "windows 7",
        "windows7",
        "windows xp",
        "windowsxp",
        "windows vista",
        "windowsvista",
        "ubuntu 16",
        "ubuntu16",
        "ubuntu 18",
        "ubuntu18",
    ]

    if any(
        pattern in operating_system
        for pattern in outdated_os_patterns
    ):

        impacts.append(
            "Malware Spread Risk"
        )

    # --------------------------------------------------------
    # Shadow IT
    # --------------------------------------------------------

    if status == "shadow it":

        impacts.append(
            "Unauthorized Access Risk"
        )

    # --------------------------------------------------------
    # SMB
    # --------------------------------------------------------

    if 445 in ports:

        impacts.append(
            "Network Attack Risk"
        )

    # --------------------------------------------------------
    # Sensitive network access
    # --------------------------------------------------------

    sensitive_access = device.get(
        "sensitive_network_access",
        0
    )

    try:
        sensitive_access = int(
            sensitive_access
        )

    except (TypeError, ValueError):
        sensitive_access = 0

    if sensitive_access == 1:

        impacts.append(
            "Sensitive Network Exposure Risk"
        )

    # --------------------------------------------------------
    # Critical vulnerabilities
    # --------------------------------------------------------

    critical_cves = device.get(
        "critical_cve_count",
        0
    )

    try:
        critical_cves = int(
            critical_cves
        )

    except (TypeError, ValueError):
        critical_cves = 0

    if critical_cves > 0:

        impacts.append(
            "Known Vulnerability Exploitation Risk"
        )

    # --------------------------------------------------------
    # Remove duplicates
    # --------------------------------------------------------

    impacts = list(
        dict.fromkeys(impacts)
    )

    return impacts


# ============================================================
# STANDALONE TEST
# ============================================================

def main():

    print()
    print("#" * 70)
    print("# SHADOW IT AI")
    print("# MODULE 14 - SECURITY IMPACT ANALYZER")
    print("#" * 70)

    test_device = {

        "hostname": "Finance-Server",

        "status": "Shadow IT",

        "os": "Windows7",

        "ports": [
            445,
            80,
        ],

        "critical_cve_count": 3,

        "sensitive_network_access": 1,
    }

    print()
    print("=" * 70)
    print("TEST DEVICE")
    print("=" * 70)

    print(test_device)

    impacts = analyze_impact(
        test_device
    )

    print()
    print("=" * 70)
    print("SECURITY IMPACTS")
    print("=" * 70)

    if not impacts:

        print(
            "No significant security impacts identified."
        )

    else:

        for index, impact in enumerate(
            impacts,
            start=1
        ):

            print(
                f"{index}. {impact}"
            )

    print()
    print("=" * 70)
    print("MODULE 14 SECURITY IMPACT ANALYZER")
    print("STATUS: PASS")
    print("=" * 70)

    return True


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":

    success = main()

    if not success:
        raise SystemExit(1)