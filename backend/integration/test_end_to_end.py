# ============================================================
# SHADOW IT AI
# MODULE 18 - END-TO-END INTEGRATION TEST
# ============================================================

import sys
from pathlib import Path


# ============================================================
# PROJECT ROOT
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))


# ============================================================
# MODULE IMPORTS
# ============================================================

from scanner.scan import scan_network
from shadow_it.detect import detect_shadow_it
from ai.feature_extractor import extract_features
from ai.predict import predict_risk
from impact.impact_analyzer import analyze_impact
from decision.decision_engine import generate_decision


# ============================================================
# DISPLAY HELPERS
# ============================================================

def print_section(title):

    print()
    print("=" * 70)
    print(title)
    print("=" * 70)


# ============================================================
# MODULE 1 — DEVICE DISCOVERY
# ============================================================

def test_device_discovery():

    print_section(
        "1. DEVICE DISCOVERY"
    )

    devices = scan_network()

    if not isinstance(devices, list):
        raise AssertionError(
            "Scanner did not return a list."
        )

    print(
        f"Devices discovered: {len(devices)}"
    )

    for device in devices:

        print(
            f"   Hostname : {device.get('hostname', '')}"
        )

        print(
            f"   IP       : {device.get('ip', '')}"
        )

        print(
            f"   Ports    : {device.get('ports', [])}"
        )

    print(
        "Device discovery: PASS"
    )

    return devices


# ============================================================
# MODULE 2 — SHADOW IT DETECTION
# ============================================================

def test_shadow_it_detection(devices):

    print_section(
        "2. SHADOW IT DETECTION"
    )

    detected_devices = detect_shadow_it(
        devices
    )

    if not isinstance(
        detected_devices,
        list
    ):
        raise AssertionError(
            "Shadow IT detector did not return a list."
        )

    for device in detected_devices:

        print(
            f"   {device.get('hostname', '')} "
            f"-> {device.get('status', '')}"
        )

    print(
        "Shadow IT detection: PASS"
    )

    return detected_devices


# ============================================================
# MODULE 3 — FEATURE EXTRACTION
# ============================================================

def test_feature_extraction(devices):

    print_section(
        "3. FEATURE EXTRACTION"
    )

    processed_devices = []

    for device in devices:

        features = extract_features(
            device
        )

        required_features = [
            "unknown_device",
            "open_port_count",
            "critical_cve_count",
            "patch_status",
            "os_outdated",
            "sensitive_network_access"
        ]

        for feature in required_features:

            if feature not in features:

                raise AssertionError(
                    f"Missing feature: {feature}"
                )

        device["features"] = features

        print(
            f"   {device.get('hostname', '')}"
        )

        for feature, value in features.items():

            print(
                f"      {feature:<30}: {value}"
            )

        processed_devices.append(
            device
        )

    print(
        "Feature extraction: PASS"
    )

    return processed_devices


# ============================================================
# MODULE 3 — AI RISK PREDICTION
# ============================================================

def test_prediction(devices):

    print_section(
        "4. AI RISK PREDICTION"
    )

    valid_risks = [
        "Low",
        "Medium",
        "High",
        "Critical"
    ]

    for device in devices:

        prediction = predict_risk(
            device["features"]
        )

        risk = prediction.get(
            "risk"
        )

        confidence = prediction.get(
            "confidence"
        )

        if risk not in valid_risks:

            raise AssertionError(
                f"Invalid risk level: {risk}"
            )

        if not isinstance(
            confidence,
            (int, float)
        ):

            raise AssertionError(
                "Confidence is not numeric."
            )

        device["risk"] = risk

        device["confidence"] = confidence

        device["probabilities"] = (
            prediction.get(
                "probabilities",
                {}
            )
        )

        print(
            f"   {device.get('hostname', '')}"
        )

        print(
            f"      Risk       : {risk}"
        )

        print(
            f"      Confidence : {confidence:.2f}%"
        )

        print(
            f"      Probabilities: "
            f"{prediction.get('probabilities', {})}"
        )

    print(
        "AI risk prediction: PASS"
    )

    return devices


# ============================================================
# MODULE 17 — IMPACT ANALYSIS
# ============================================================

def test_impact_analysis(devices):

    print_section(
        "5. SECURITY IMPACT ANALYSIS"
    )

    for device in devices:

        impacts = analyze_impact(
            device
        )

        if not isinstance(
            impacts,
            list
        ):

            raise AssertionError(
                "Impact analyzer did not return a list."
            )

        device[
            "security_impacts"
        ] = impacts

        print(
            f"   {device.get('hostname', '')}"
        )

        if impacts:

            for impact in impacts:

                print(
                    f"      - {impact}"
                )

        else:

            print(
                "      - No immediate security impacts detected."
            )

    print(
        "Security impact analysis: PASS"
    )

    return devices


# ============================================================
# MODULE 17 — DECISION ENGINE
# ============================================================

def test_decision_engine(devices):

    print_section(
        "6. DECISION ENGINE"
    )

    for device in devices:

        features = device[
            "features"
        ]

        decision_input = {

            "unknown_device":
                features[
                    "unknown_device"
                ],

            "open_port_count":
                features[
                    "open_port_count"
                ],

            "critical_cve_count":
                features[
                    "critical_cve_count"
                ],

            "patch_status":
                features[
                    "patch_status"
                ],

            "os_outdated":
                features[
                    "os_outdated"
                ],

            "sensitive_network_access":
                features[
                    "sensitive_network_access"
                ],

            "risk":
                device[
                    "risk"
                ],

            "confidence":
                device[
                    "confidence"
                ]
        }

        decision = generate_decision(
            decision_input
        )

        if not isinstance(
            decision,
            dict
        ):

            raise AssertionError(
                "Decision engine did not return a dictionary."
            )

        required_fields = [
            "risk_level",
            "confidence",
            "priority",
            "primary_decision",
            "severity",
            "severity_score",
            "response_time",
            "containment_recommended",
            "escalation",
            "security_findings",
            "security_impact",
            "recommendations"
        ]

        for field in required_fields:

            if field not in decision:

                raise AssertionError(
                    f"Decision field missing: {field}"
                )

        device[
            "decision"
        ] = decision

        print(
            f"   {device.get('hostname', '')}"
        )

        print(
            f"      Risk       : "
            f"{decision['risk_level']}"
        )

        print(
            f"      Priority   : "
            f"{decision['priority']}"
        )

        print(
            f"      Severity   : "
            f"{decision['severity']}"
        )

        print(
            f"      Decision   : "
            f"{decision['primary_decision']}"
        )

        print(
            f"      Actions    : "
            f"{decision['action_count']}"
        )

    print(
        "Decision engine: PASS"
    )

    return devices


# ============================================================
# FINAL INTEGRATION RESULT
# ============================================================

def print_final_result(devices):

    print_section(
        "7. FINAL END-TO-END RESULT"
    )

    print(
        f"Total devices processed: {len(devices)}"
    )

    for index, device in enumerate(
        devices,
        start=1
    ):

        print()

        print(
            f"DEVICE {index}"
        )

        print(
            f"   Hostname       : "
            f"{device.get('hostname', '')}"
        )

        print(
            f"   IP             : "
            f"{device.get('ip', '')}"
        )

        print(
            f"   Status         : "
            f"{device.get('status', '')}"
        )

        print(
            f"   Risk           : "
            f"{device.get('risk', '')}"
        )

        print(
            f"   Confidence     : "
            f"{device.get('confidence', 0):.2f}%"
        )

        print(
            f"   Impacts        : "
            f"{len(device.get('security_impacts', []))}"
        )

        decision = device.get(
            "decision",
            {}
        )

        print(
            f"   Priority       : "
            f"{decision.get('priority', '')}"
        )

        print(
            f"   Primary Action : "
            f"{decision.get('primary_decision', '')}"
        )

    print()
    print(
        "=" * 70
    )

    print(
        "END-TO-END INTEGRATION TEST: PASSED"
    )

    print(
        "Scanner -> Shadow IT -> Features -> AI -> Impact -> Decision"
    )

    print(
        "=" * 70
    )


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print("#" * 70)
    print("# SHADOW IT AI")
    print("# MODULE 18 - END-TO-END INTEGRATION TEST")
    print("#" * 70)

    try:

        # ----------------------------------------------------
        # 1. DEVICE DISCOVERY
        # ----------------------------------------------------

        devices = test_device_discovery()

        # ----------------------------------------------------
        # 2. SHADOW IT
        # ----------------------------------------------------

        devices = test_shadow_it_detection(
            devices
        )

        # ----------------------------------------------------
        # 3. FEATURES
        # ----------------------------------------------------

        devices = test_feature_extraction(
            devices
        )

        # ----------------------------------------------------
        # 4. AI PREDICTION
        # ----------------------------------------------------

        devices = test_prediction(
            devices
        )

        # ----------------------------------------------------
        # 5. IMPACT
        # ----------------------------------------------------

        devices = test_impact_analysis(
            devices
        )

        # ----------------------------------------------------
        # 6. DECISION
        # ----------------------------------------------------

        devices = test_decision_engine(
            devices
        )

        # ----------------------------------------------------
        # 7. FINAL RESULT
        # ----------------------------------------------------

        print_final_result(
            devices
        )

        return True

    except Exception as error:

        print()
        print(
            "=" * 70
        )

        print(
            "END-TO-END INTEGRATION TEST: FAILED"
        )

        print(
            f"Error: {error}"
        )

        print(
            "=" * 70
        )

        return False


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":

    success = main()

    if not success:

        raise SystemExit(1)
