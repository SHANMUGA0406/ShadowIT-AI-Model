import json
from pathlib import Path


# ============================================================
# SHADOW IT AI
# MODULE 17 - FINAL DECISION ENGINE
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_DIR = BASE_DIR / "ai" / "models"

LABEL_MAPPING_PATH = MODEL_DIR / "label_mapping.json"
FEATURE_CONFIG_PATH = MODEL_DIR / "feature_config.json"


# ============================================================
# AUTHORITATIVE FEATURE CONFIGURATION
# ============================================================

FEATURE_COLUMNS = [
    "unknown_device",
    "open_port_count",
    "critical_cve_count",
    "patch_status",
    "os_outdated",
    "sensitive_network_access",
]


# ============================================================
# AUTHORITATIVE RISK MAPPING
# ============================================================

RISK_NAMES = {
    0: "Low",
    1: "Medium",
    2: "High",
    3: "Critical",
}


# ============================================================
# RISK CONFIGURATION
# ============================================================

RISK_CONFIGURATION = {

    "Low": {
        "priority": "LOW",
        "severity": "Low",
        "severity_score": 25,
        "response_time": "Within 7 days",
        "containment_recommended": False,
        "escalation": False,
    },

    "Medium": {
        "priority": "MODERATE",
        "severity": "Medium",
        "severity_score": 50,
        "response_time": "Within 3 days",
        "containment_recommended": False,
        "escalation": False,
    },

    "High": {
        "priority": "HIGH",
        "severity": "High",
        "severity_score": 75,
        "response_time": "Within 24 hours",
        "containment_recommended": True,
        "escalation": True,
    },

    "Critical": {
        "priority": "IMMEDIATE",
        "severity": "Critical",
        "severity_score": 100,
        "response_time": "Immediately",
        "containment_recommended": True,
        "escalation": True,
    },
}


# ============================================================
# HELPER
# ============================================================

def print_section(title):

    print()
    print("=" * 70)
    print(title)
    print("=" * 70)


# ============================================================
# LOAD CONFIGURATION
# ============================================================

def load_configuration():

    print_section(
        "1. LOADING DECISION ENGINE CONFIGURATION"
    )

    if not LABEL_MAPPING_PATH.exists():

        print(
            "ERROR: Label mapping not found:"
        )

        print(
            LABEL_MAPPING_PATH
        )

        return False

    if not FEATURE_CONFIG_PATH.exists():

        print(
            "ERROR: Feature configuration not found:"
        )

        print(
            FEATURE_CONFIG_PATH
        )

        return False

    try:

        with open(
            LABEL_MAPPING_PATH,
            "r",
            encoding="utf-8"
        ) as file:

            json.load(file)

        with open(
            FEATURE_CONFIG_PATH,
            "r",
            encoding="utf-8"
        ) as file:

            json.load(file)

    except Exception as error:

        print(
            "ERROR: Failed to load configuration."
        )

        print(
            f"Error: {error}"
        )

        return False

    print(
        "Label mapping loaded successfully."
    )

    print(
        "Feature configuration loaded successfully."
    )

    return True


# ============================================================
# VALIDATE DEVICE FEATURES
# ============================================================

def validate_features(device):

    if not isinstance(device, dict):

        return False

    missing_features = [
        feature
        for feature in FEATURE_COLUMNS
        if feature not in device
    ]

    if missing_features:

        return False

    binary_features = [
        "unknown_device",
        "patch_status",
        "os_outdated",
        "sensitive_network_access",
    ]

    for feature in binary_features:

        value = device[feature]

        if value not in [0, 1]:

            return False

    if device["open_port_count"] < 0:

        return False

    if device["critical_cve_count"] < 0:

        return False

    return True


# ============================================================
# SECURITY FINDINGS
# ============================================================

def generate_security_findings(device):

    findings = []

    # --------------------------------------------------------
    # UNKNOWN DEVICE
    # --------------------------------------------------------

    if device["unknown_device"] == 1:

        findings.append({
            "feature": "unknown_device",
            "severity": "High",
            "finding":
                "Device is not recognized as an approved device."
        })

    # --------------------------------------------------------
    # OPEN PORTS
    # --------------------------------------------------------

    if device["open_port_count"] >= 10:

        findings.append({
            "feature": "open_port_count",
            "severity": "High",
            "finding":
                f"Device has {device['open_port_count']} "
                f"open ports, creating a large attack surface."
        })

    elif device["open_port_count"] >= 5:

        findings.append({
            "feature": "open_port_count",
            "severity": "Medium",
            "finding":
                f"Device has {device['open_port_count']} "
                f"open ports, increasing its attack surface."
        })

    # --------------------------------------------------------
    # CRITICAL CVEs
    # --------------------------------------------------------

    if device["critical_cve_count"] > 0:

        findings.append({
            "feature": "critical_cve_count",
            "severity": "High",
            "finding":
                f"Device has {device['critical_cve_count']} "
                f"critical vulnerabilities."
        })

    # --------------------------------------------------------
    # PATCH STATUS
    # --------------------------------------------------------

    if device["patch_status"] == 0:

        findings.append({
            "feature": "patch_status",
            "severity": "High",
            "finding":
                "Device has an outdated patch status."
        })

    # --------------------------------------------------------
    # OUTDATED OS
    # --------------------------------------------------------

    if device["os_outdated"] == 1:

        findings.append({
            "feature": "os_outdated",
            "severity": "High",
            "finding":
                "Device is running an outdated operating system."
        })

    # --------------------------------------------------------
    # SENSITIVE NETWORK ACCESS
    # --------------------------------------------------------

    if device["sensitive_network_access"] == 1:

        findings.append({
            "feature": "sensitive_network_access",
            "severity": "High",
            "finding":
                "Device has access to sensitive network resources."
        })

    return findings


# ============================================================
# DETERMINE PRIORITY
# ============================================================

def determine_priority(risk_level):

    configuration = RISK_CONFIGURATION.get(
        risk_level,
        RISK_CONFIGURATION["Low"]
    )

    return configuration["priority"]


# ============================================================
# PRIMARY SECURITY DECISION
# ============================================================

def determine_primary_decision(
    risk_level,
    device
):

    if risk_level == "Critical":

        return "ISOLATE DEVICE"

    if risk_level == "High":

        return "RESTRICT DEVICE ACCESS"

    if risk_level == "Medium":

        return "INVESTIGATE AND REMEDIATE"

    return "MONITOR DEVICE"


# ============================================================
# RECOMMENDED ACTIONS
# ============================================================

def generate_recommended_actions(
    risk_level,
    device
):

    actions = []

    # --------------------------------------------------------
    # CRITICAL
    # --------------------------------------------------------

    if risk_level == "Critical":

        actions.append(
            "Isolate the device from sensitive network resources."
        )

        actions.append(
            "Verify device ownership and authorization."
        )

    # --------------------------------------------------------
    # UNKNOWN DEVICE
    # --------------------------------------------------------

    if device["unknown_device"] == 1:

        actions.append(
            "Verify whether the device is authorized "
            "to operate on the network."
        )

    # --------------------------------------------------------
    # CRITICAL CVEs
    # --------------------------------------------------------

    if device["critical_cve_count"] > 0:

        actions.append(
            "Remediate critical vulnerabilities immediately."
        )

    # --------------------------------------------------------
    # PATCH STATUS
    # --------------------------------------------------------

    if device["patch_status"] == 0:

        actions.append(
            "Apply the latest security patches."
        )

    # --------------------------------------------------------
    # OUTDATED OS
    # --------------------------------------------------------

    if device["os_outdated"] == 1:

        actions.append(
            "Upgrade the operating system to a supported version."
        )

    # --------------------------------------------------------
    # OPEN PORTS
    # --------------------------------------------------------

    if device["open_port_count"] >= 5:

        actions.append(
            "Review unnecessary open ports and disable "
            "unneeded services."
        )

    # --------------------------------------------------------
    # SENSITIVE NETWORK
    # --------------------------------------------------------

    if device["sensitive_network_access"] == 1:

        actions.append(
            "Review and restrict sensitive network access."
        )

    # --------------------------------------------------------
    # LOW-RISK FALLBACK
    # --------------------------------------------------------

    if not actions:

        actions.append(
            "Continue normal security monitoring."
        )

    # --------------------------------------------------------
    # REMOVE DUPLICATES
    # --------------------------------------------------------

    unique_actions = []

    for action in actions:

        if action not in unique_actions:

            unique_actions.append(action)

    return unique_actions


# ============================================================
# SECURITY IMPACT
# ============================================================

def determine_security_impact(
    risk_level,
    device
):

    if risk_level == "Critical":

        return (
            "A compromise of this device could provide "
            "significant opportunity for unauthorized access, "
            "exploitation of known vulnerabilities, or access "
            "to sensitive network resources."
        )

    if risk_level == "High":

        return (
            "The device presents significant security exposure "
            "and should be remediated promptly."
        )

    if risk_level == "Medium":

        return (
            "The device presents moderate security exposure "
            "and should be investigated and monitored."
        )

    return (
        "The device currently presents limited security risk "
        "but should remain under normal monitoring."
    )


# ============================================================
# CREATE DECISION SUMMARY
# ============================================================

def create_decision_summary(
    risk_level,
    confidence,
    priority,
    primary_decision,
    findings,
    actions,
    impact
):

    configuration = RISK_CONFIGURATION.get(
        risk_level,
        RISK_CONFIGURATION["Low"]
    )

    return {

        # ----------------------------------------------------
        # AI RESULT
        # ----------------------------------------------------

        "risk_level": risk_level,

        "confidence": confidence,

        # ----------------------------------------------------
        # DECISION INTELLIGENCE
        # ----------------------------------------------------

        "priority": priority,

        "primary_decision": primary_decision,

        "severity": configuration[
            "severity"
        ],

        "severity_score": configuration[
            "severity_score"
        ],

        "response_time": configuration[
            "response_time"
        ],

        "containment": configuration[
            "containment_recommended"
        ],

        "containment_recommended": configuration[
            "containment_recommended"
        ],

        "escalation": configuration[
            "escalation"
        ],

        # ----------------------------------------------------
        # SECURITY ANALYSIS
        # ----------------------------------------------------

        "security_findings": findings,

        "security_impact": impact,

        # ----------------------------------------------------
        # IMPORTANT API COMPATIBILITY
        # ----------------------------------------------------

        "recommended_actions": actions,

        "recommendations": actions,

        "action_count": len(actions),
    }


# ============================================================
# API-COMPATIBLE DECISION FUNCTION
# ============================================================

def generate_decision(device):

    """
    Generate actionable security decisions.

    Expected device structure:

        {
            "unknown_device": 0 or 1,
            "open_port_count": integer,
            "critical_cve_count": integer,
            "patch_status": 0 or 1,
            "os_outdated": 0 or 1,
            "sensitive_network_access": 0 or 1,
            "risk": "Low/Medium/High/Critical",
            "confidence": number
        }
    """

    # --------------------------------------------------------
    # VALIDATE FEATURES
    # --------------------------------------------------------

    if not validate_features(device):

        raise ValueError(
            "Invalid or missing device features."
        )

    # --------------------------------------------------------
    # GET RISK
    # --------------------------------------------------------

    risk_level = device.get(
        "risk",
        "Low"
    )

    if risk_level not in [
        "Low",
        "Medium",
        "High",
        "Critical"
    ]:

        raise ValueError(
            f"Invalid risk level: {risk_level}"
        )

    # --------------------------------------------------------
    # GET CONFIDENCE
    # --------------------------------------------------------

    confidence = device.get(
        "confidence",
        0
    )

    # --------------------------------------------------------
    # FINDINGS
    # --------------------------------------------------------

    findings = generate_security_findings(
        device
    )

    # --------------------------------------------------------
    # PRIORITY
    # --------------------------------------------------------

    priority = determine_priority(
        risk_level
    )

    # --------------------------------------------------------
    # PRIMARY DECISION
    # --------------------------------------------------------

    primary_decision = determine_primary_decision(
        risk_level,
        device
    )

    # --------------------------------------------------------
    # ACTIONS
    # --------------------------------------------------------

    actions = generate_recommended_actions(
        risk_level,
        device
    )

    # --------------------------------------------------------
    # SECURITY IMPACT
    # --------------------------------------------------------

    impact = determine_security_impact(
        risk_level,
        device
    )

    # --------------------------------------------------------
    # FINAL DECISION
    # --------------------------------------------------------

    return create_decision_summary(
        risk_level=risk_level,
        confidence=confidence,
        priority=priority,
        primary_decision=primary_decision,
        findings=findings,
        actions=actions,
        impact=impact
    )


# ============================================================
# MODULE 17 TEST
# ============================================================

def main():

    print()
    print("#" * 70)
    print("# SHADOW IT AI")
    print("# MODULE 17 - FINAL DECISION ENGINE")
    print("#" * 70)

    # --------------------------------------------------------
    # 1. CONFIGURATION
    # --------------------------------------------------------

    if not load_configuration():

        return False

    # --------------------------------------------------------
    # 2. TEST DEVICE
    # --------------------------------------------------------

    print_section(
        "2. TEST DEVICE"
    )

    device = {

        "unknown_device": 1,

        "open_port_count": 8,

        "critical_cve_count": 3,

        "patch_status": 0,

        "os_outdated": 1,

        "sensitive_network_access": 1,

        "risk": "Critical",

        "confidence": 72.89,
    }

    print(
        "Test device feature values:"
    )

    for feature in FEATURE_COLUMNS:

        print(
            f"   {feature:<30}: "
            f"{device[feature]}"
        )

    # --------------------------------------------------------
    # 3. VALIDATE
    # --------------------------------------------------------

    print_section(
        "3. VALIDATING DEVICE FEATURES"
    )

    if not validate_features(device):

        print(
            "Device feature validation: FAIL"
        )

        return False

    print(
        "Device feature validation: PASS"
    )

    # --------------------------------------------------------
    # 4. GENERATE DECISION
    # --------------------------------------------------------

    print_section(
        "4. GENERATING SECURITY DECISION"
    )

    decision = generate_decision(
        device
    )

    # --------------------------------------------------------
    # 5. PRINT RESULT
    # --------------------------------------------------------

    print_section(
        "5. SECURITY FINDINGS"
    )

    findings = decision[
        "security_findings"
    ]

    for index, finding in enumerate(
        findings,
        start=1
    ):

        print(
            f"{index}. "
            f"[{finding['severity']}] "
            f"{finding['finding']}"
        )

    print_section(
        "6. DECISION"
    )

    print(
        f"Risk Level       : "
        f"{decision['risk_level']}"
    )

    print(
        f"Confidence       : "
        f"{decision['confidence']:.2f}%"
    )

    print(
        f"Priority         : "
        f"{decision['priority']}"
    )

    print(
        f"Severity         : "
        f"{decision['severity']}"
    )

    print(
        f"Severity Score   : "
        f"{decision['severity_score']}/100"
    )

    print(
        f"Response Time    : "
        f"{decision['response_time']}"
    )

    print(
        f"Containment      : "
        f"{decision['containment_recommended']}"
    )

    print(
        f"Escalation       : "
        f"{decision['escalation']}"
    )

    print(
        f"Primary Decision : "
        f"{decision['primary_decision']}"
    )

    print_section(
        "7. SECURITY IMPACT"
    )

    print(
        decision["security_impact"]
    )

    print_section(
        "8. RECOMMENDED ACTIONS"
    )

    for index, action in enumerate(
        decision["recommendations"],
        start=1
    ):

        print(
            f"{index}. {action}"
        )

    print_section(
        "9. FINAL RESULT"
    )

    print(
        f"Risk Level       : "
        f"{decision['risk_level']}"
    )

    print(
        f"Priority         : "
        f"{decision['priority']}"
    )

    print(
        f"Severity Score   : "
        f"{decision['severity_score']}/100"
    )

    print(
        f"Primary Decision : "
        f"{decision['primary_decision']}"
    )

    print(
        f"Finding Count    : "
        f"{len(decision['security_findings'])}"
    )

    print(
        f"Action Count     : "
        f"{decision['action_count']}"
    )

    print()
    print(
        "Decision engine successfully converted "
        "the AI risk assessment into actionable "
        "security decisions."
    )

    print()
    print("#" * 70)
    print(
        "MODULE 17 DECISION ENGINE VERIFICATION PASSED"
    )
    print("#" * 70)

    return True


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":

    success = main()

    if not success:

        raise SystemExit(1)