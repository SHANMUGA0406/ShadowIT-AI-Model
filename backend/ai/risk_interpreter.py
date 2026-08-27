import json
from pathlib import Path


# ============================================================
# SHADOW IT AI
# MODULE 12 - RISK INTERPRETATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_DIR = (
    BASE_DIR
    / "ai"
    / "models"
)

LABEL_MAPPING_PATH = (
    MODEL_DIR
    / "label_mapping.json"
)

FEATURE_CONFIG_PATH = (
    MODEL_DIR
    / "feature_config.json"
)


# ============================================================
# AUTHORITATIVE FEATURE ORDER
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

RISK_MAPPING = {
    0: "Low",
    1: "Medium",
    2: "High",
    3: "Critical",
}


# ============================================================
# RISK PRIORITY
# ============================================================

RISK_PRIORITY = {
    "Low": "LOW",
    "Medium": "MEDIUM",
    "High": "HIGH",
    "Critical": "IMMEDIATE",
}


# ============================================================
# RISK DESCRIPTIONS
# ============================================================

RISK_DESCRIPTIONS = {

    "Low":
        "The device presents a relatively low security risk "
        "based on the evaluated security features.",

    "Medium":
        "The device presents a moderate security risk and "
        "should be reviewed and monitored.",

    "High":
        "The device presents a high security risk and "
        "requires security remediation.",

    "Critical":
        "The device presents a critical security risk and "
        "requires immediate security attention.",
}


# ============================================================
# FEATURE INTERPRETATIONS
# ============================================================

FEATURE_INTERPRETATIONS = {

    "unknown_device": {
        "positive":
            "The device is not recognized as an approved device, "
            "which indicates potential Shadow IT activity.",
        "negative":
            "The device is recognized as an approved device."
    },

    "open_port_count": {
        "positive":
            "A high number of open ports increases the device's "
            "potential attack surface.",
        "negative":
            "The number of open ports does not strongly increase "
            "the identified risk."
    },

    "critical_cve_count": {
        "positive":
            "Critical vulnerabilities were identified, increasing "
            "the likelihood of exploitation.",
        "negative":
            "The number of critical vulnerabilities does not "
            "strongly increase the identified risk."
    },

    "patch_status": {
        "positive":
            "The device has an outdated patch status, increasing "
            "exposure to known vulnerabilities.",
        "negative":
            "The device has an updated patch status."
    },

    "os_outdated": {
        "positive":
            "The device is running an outdated operating system, "
            "which increases security exposure.",
        "negative":
            "The operating system is not identified as outdated."
    },

    "sensitive_network_access": {
        "positive":
            "The device has access to sensitive network resources, "
            "which increases the potential impact of compromise.",
        "negative":
            "Sensitive network access is not identified."
    },
}


# ============================================================
# HELPER
# ============================================================

def print_section(title):

    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


# ============================================================
# LOAD JSON FILE
# ============================================================

def load_json_file(path, name):

    if not path.exists():

        print(
            f"ERROR - {name} not found:"
        )

        print(path)

        return None

    try:

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except Exception as error:

        print(
            f"ERROR - Failed to load {name}."
        )

        print(
            f"Error: {error}"
        )

        return None


# ============================================================
# LOAD CONFIGURATION
# ============================================================

def load_configuration():

    print_section(
        "1. LOADING RISK CONFIGURATION"
    )

    label_mapping = load_json_file(
        LABEL_MAPPING_PATH,
        "label_mapping.json"
    )

    if label_mapping is None:

        return None

    feature_config = load_json_file(
        FEATURE_CONFIG_PATH,
        "feature_config.json"
    )

    if feature_config is None:

        return None

    print(
        "Label mapping loaded successfully."
    )

    print(
        "Feature configuration loaded successfully."
    )

    return {
        "label_mapping": label_mapping,
        "feature_config": feature_config,
    }


# ============================================================
# VALIDATE FEATURE CONFIGURATION
# ============================================================

def validate_configuration(configuration):

    print_section(
        "2. VALIDATING CONFIGURATION"
    )

    feature_config = configuration[
        "feature_config"
    ]

    # --------------------------------------------------------
    # Support common feature_config formats
    # --------------------------------------------------------

    if isinstance(
        feature_config,
        dict
    ):

        configured_features = (
            feature_config.get(
                "features",
                feature_config.get(
                    "feature_columns",
                    []
                )
            )
        )

    elif isinstance(
        feature_config,
        list
    ):

        configured_features = (
            feature_config
        )

    else:

        configured_features = []

    if configured_features:

        if list(
            configured_features
        ) != FEATURE_COLUMNS:

            print(
                "ERROR - Feature configuration mismatch."
            )

            print(
                "\nExpected:"
            )

            for index, feature in enumerate(
                FEATURE_COLUMNS,
                start=1
            ):

                print(
                    f"   {index}. {feature}"
                )

            print(
                "\nReceived:"
            )

            for index, feature in enumerate(
                configured_features,
                start=1
            ):

                print(
                    f"   {index}. {feature}"
                )

            return False

    print(
        "Feature configuration validation: PASS"
    )

    print(
        "\nAuthoritative feature order:"
    )

    for index, feature in enumerate(
        FEATURE_COLUMNS,
        start=1
    ):

        print(
            f"   {index}. {feature}"
        )

    return True


# ============================================================
# VALIDATE DEVICE
# ============================================================

def validate_device(device):

    print_section(
        "3. VALIDATING DEVICE FEATURES"
    )

    missing_features = [
        feature
        for feature in FEATURE_COLUMNS
        if feature not in device
    ]

    if missing_features:

        print(
            "ERROR - Missing device features:"
        )

        for feature in missing_features:

            print(
                f"   - {feature}"
            )

        return False

    try:

        for feature in FEATURE_COLUMNS:

            value = float(
                device[feature]
            )

            if feature in [
                "unknown_device",
                "patch_status",
                "os_outdated",
                "sensitive_network_access",
            ]:

                if value not in [
                    0,
                    1,
                ]:

                    print(
                        f"ERROR - Invalid binary value "
                        f"for {feature}: {value}"
                    )

                    return False

            if feature in [
                "open_port_count",
                "critical_cve_count",
            ]:

                if value < 0:

                    print(
                        f"ERROR - Negative value "
                        f"for {feature}."
                    )

                    return False

    except (
        TypeError,
        ValueError
    ) as error:

        print(
            "ERROR - Invalid device feature value."
        )

        print(
            f"Error: {error}"
        )

        return False

    print(
        "Device feature validation: PASS"
    )

    return True


# ============================================================
# FEATURE-LEVEL SECURITY ANALYSIS
# ============================================================

def analyze_features(device):

    findings = []

    # --------------------------------------------------------
    # Unknown device
    # --------------------------------------------------------

    if int(device["unknown_device"]) == 1:

        findings.append(
            {
                "feature": "unknown_device",
                "severity": "High",
                "finding":
                    FEATURE_INTERPRETATIONS[
                        "unknown_device"
                    ]["positive"],
            }
        )

    # --------------------------------------------------------
    # Open ports
    # --------------------------------------------------------

    open_ports = int(
        device["open_port_count"]
    )

    if open_ports >= 10:

        findings.append(
            {
                "feature": "open_port_count",
                "severity": "High",
                "finding":
                    f"The device has {open_ports} open ports, "
                    "which creates a large attack surface.",
            }
        )

    elif open_ports >= 5:

        findings.append(
            {
                "feature": "open_port_count",
                "severity": "Medium",
                "finding":
                    f"The device has {open_ports} open ports, "
                    "which increases its attack surface.",
            }
        )

    # --------------------------------------------------------
    # Critical CVEs
    # --------------------------------------------------------

    critical_cves = int(
        device["critical_cve_count"]
    )

    if critical_cves >= 5:

        findings.append(
            {
                "feature": "critical_cve_count",
                "severity": "Critical",
                "finding":
                    f"The device has {critical_cves} critical "
                    "vulnerabilities requiring immediate remediation.",
            }
        )

    elif critical_cves >= 1:

        findings.append(
            {
                "feature": "critical_cve_count",
                "severity": "High",
                "finding":
                    f"The device has {critical_cves} critical "
                    "vulnerability/vulnerabilities.",
            }
        )

    # --------------------------------------------------------
    # Patch status
    # --------------------------------------------------------

    if int(device["patch_status"]) == 0:

        findings.append(
            {
                "feature": "patch_status",
                "severity": "High",
                "finding":
                    FEATURE_INTERPRETATIONS[
                        "patch_status"
                    ]["positive"],
            }
        )

    # --------------------------------------------------------
    # OS status
    # --------------------------------------------------------

    if int(device["os_outdated"]) == 1:

        findings.append(
            {
                "feature": "os_outdated",
                "severity": "High",
                "finding":
                    FEATURE_INTERPRETATIONS[
                        "os_outdated"
                    ]["positive"],
            }
        )

    # --------------------------------------------------------
    # Sensitive network access
    # --------------------------------------------------------

    if int(
        device["sensitive_network_access"]
    ) == 1:

        findings.append(
            {
                "feature":
                    "sensitive_network_access",
                "severity": "High",
                "finding":
                    FEATURE_INTERPRETATIONS[
                        "sensitive_network_access"
                    ]["positive"],
            }
        )

    return findings


# ============================================================
# RISK INTERPRETATION
# ============================================================

def interpret_risk(
    risk,
    confidence,
    device
):

    findings = analyze_features(
        device
    )

    # --------------------------------------------------------
    # Risk description
    # --------------------------------------------------------

    description = (
        RISK_DESCRIPTIONS.get(
            risk,
            "The device risk could not be determined."
        )
    )

    # --------------------------------------------------------
    # Build human-readable explanation
    # --------------------------------------------------------

    explanation_parts = []

    if risk == "Critical":

        explanation_parts.append(
            "Immediate security attention is required."
        )

    elif risk == "High":

        explanation_parts.append(
            "Security remediation should be performed promptly."
        )

    elif risk == "Medium":

        explanation_parts.append(
            "The device should be reviewed and monitored."
        )

    else:

        explanation_parts.append(
            "Continue normal monitoring and security controls."
        )

    if findings:

        explanation_parts.append(
            "The main security findings are:"
        )

        for finding in findings[:5]:

            explanation_parts.append(
                finding["finding"]
            )

    explanation = " ".join(
        explanation_parts
    )

    # --------------------------------------------------------
    # Security impact
    # --------------------------------------------------------

    if risk == "Critical":

        impact = (
            "A compromise of this device could provide "
            "significant opportunity for unauthorized access, "
            "exploitation of known vulnerabilities, or access "
            "to sensitive network resources."
        )

    elif risk == "High":

        impact = (
            "The device may provide attackers with a meaningful "
            "attack path if its security weaknesses are exploited."
        )

    elif risk == "Medium":

        impact = (
            "The device has identifiable security weaknesses "
            "that could become more significant if left unresolved."
        )

    else:

        impact = (
            "The current feature profile indicates relatively "
            "limited security exposure."
        )

    # --------------------------------------------------------
    # Recommended actions
    # --------------------------------------------------------

    recommendations = []

    if int(device["unknown_device"]) == 1:

        recommendations.append(
            "Verify device ownership and authorization."
        )

    if int(device["critical_cve_count"]) > 0:

        recommendations.append(
            "Remediate critical vulnerabilities immediately."
        )

    if int(device["patch_status"]) == 0:

        recommendations.append(
            "Apply the latest security patches."
        )

    if int(device["os_outdated"]) == 1:

        recommendations.append(
            "Upgrade the operating system to a supported version."
        )

    if int(device["open_port_count"]) >= 5:

        recommendations.append(
            "Review unnecessary open ports and disable "
            "unneeded services."
        )

    if int(
        device["sensitive_network_access"]
    ) == 1:

        recommendations.append(
            "Review and restrict sensitive network access."
        )

    if risk == "Critical":

        recommendations.insert(
            0,
            "Consider isolating the device from sensitive "
            "network resources until remediation is completed."
        )

    elif risk == "High":

        recommendations.insert(
            0,
            "Prioritize this device for security remediation."
        )

    if not recommendations:

        recommendations.append(
            "Continue monitoring the device and maintain "
            "standard security controls."
        )

    return {
        "risk": risk,
        "confidence": round(
            float(confidence),
            2
        ),
        "priority": RISK_PRIORITY.get(
            risk,
            "UNKNOWN"
        ),
        "description": description,
        "explanation": explanation,
        "security_impact": impact,
        "findings": findings,
        "recommendations": recommendations,
    }


# ============================================================
# DISPLAY RESULT
# ============================================================

def display_result(result):

    print_section(
        "4. RISK INTERPRETATION"
    )

    print(
        f"Risk Level     : {result['risk']}"
    )

    print(
        f"Confidence     : {result['confidence']:.2f}%"
    )

    print(
        f"Priority       : {result['priority']}"
    )

    print(
        "\nRisk description:"
    )

    print(
        result["description"]
    )

    print_section(
        "5. SECURITY FINDINGS"
    )

    if result["findings"]:

        for index, finding in enumerate(
            result["findings"],
            start=1
        ):

            print(
                f"{index}. "
                f"[{finding['severity']}] "
                f"{finding['finding']}"
            )

    else:

        print(
            "No significant feature-level findings identified."
        )

    print_section(
        "6. SECURITY IMPACT"
    )

    print(
        result["security_impact"]
    )

    print_section(
        "7. RECOMMENDED ACTIONS"
    )

    for index, recommendation in enumerate(
        result["recommendations"],
        start=1
    ):

        print(
            f"{index}. {recommendation}"
        )


# ============================================================
# MAIN
# ============================================================

def main():

    print("\n" + "#" * 70)
    print("# SHADOW IT AI")
    print("# MODULE 12 - RISK INTERPRETATION")
    print("#" * 70)

    # --------------------------------------------------------
    # Load configuration
    # --------------------------------------------------------

    configuration = (
        load_configuration()
    )

    if configuration is None:

        return False

    # --------------------------------------------------------
    # Validate configuration
    # --------------------------------------------------------

    if not validate_configuration(
        configuration
    ):

        return False

    # --------------------------------------------------------
    # Test device
    # --------------------------------------------------------

    print_section(
        "TEST DEVICE"
    )

    test_device = {

        "unknown_device": 1,

        "open_port_count": 8,

        "critical_cve_count": 3,

        "patch_status": 0,

        "os_outdated": 1,

        "sensitive_network_access": 1,
    }

    print(
        "Test feature values:"
    )

    for feature in FEATURE_COLUMNS:

        print(
            f"   {feature:<28}: "
            f"{test_device[feature]}"
        )

    # --------------------------------------------------------
    # Validate device
    # --------------------------------------------------------

    if not validate_device(
        test_device
    ):

        return False

    # --------------------------------------------------------
    # Prediction from Module 10
    # --------------------------------------------------------

    predicted_class = 3

    confidence = 72.89

    risk = RISK_MAPPING[
        predicted_class
    ]

    print_section(
        "MODEL PREDICTION"
    )

    print(
        f"Predicted class : {predicted_class}"
    )

    print(
        f"Predicted risk  : {risk}"
    )

    print(
        f"Confidence      : {confidence:.2f}%"
    )

    # --------------------------------------------------------
    # Interpret
    # --------------------------------------------------------

    result = interpret_risk(
        risk,
        confidence,
        test_device
    )

    # --------------------------------------------------------
    # Display
    # --------------------------------------------------------

    display_result(
        result
    )

    # --------------------------------------------------------
    # Final result
    # --------------------------------------------------------

    print_section(
        "FINAL MODULE 12 RESULT"
    )

    print(
        "MODULE 12 RISK INTERPRETATION "
        "COMPLETED SUCCESSFULLY"
    )

    print(
        f"\nRisk Level : {result['risk']}"
    )

    print(
        f"Priority   : {result['priority']}"
    )

    print(
        f"Confidence : {result['confidence']:.2f}%"
    )

    print(
        "\nTop security findings:"
    )

    for finding in result["findings"][:3]:

        print(
            f"   - {finding['feature']} "
            f"({finding['severity']})"
        )

    print(
        "\nRecommended action count:"
    )

    print(
        f"   {len(result['recommendations'])}"
    )

    print_section(
        "STATUS: PASS"
    )

    return True


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":

    success = main()

    if not success:

        raise SystemExit(1)