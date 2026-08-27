# ============================================================
# SHADOW IT AI
# MODULE 23 - FINAL SYSTEM VALIDATION
# ============================================================

import sys
from pathlib import Path


# ============================================================
# PROJECT PATH
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
# HEADER
# ============================================================

print()
print("#" * 70)
print("# SHADOW IT AI")
print("# MODULE 23 - FINAL SYSTEM VALIDATION")
print("#" * 70)


# ============================================================
# TEST COUNTERS
# ============================================================

tests_passed = 0
tests_failed = 0


# ============================================================
# HELPER
# ============================================================

def record_test(name, passed):

    global tests_passed
    global tests_failed

    if passed:

        print(f"{name}: PASS")
        tests_passed += 1

    else:

        print(f"{name}: FAIL")
        tests_failed += 1


# ============================================================
# 1. DEVICE DISCOVERY
# ============================================================

print()
print("=" * 70)
print("1. DEVICE DISCOVERY")
print("=" * 70)

try:

    discovered_devices = scan_network()

    print(
        f"Devices discovered: "
        f"{len(discovered_devices)}"
    )

    for device in discovered_devices:

        print(
            f"   {device.get('hostname', 'Unknown')} "
            f"-> "
            f"{device.get('ip', 'Unknown')}"
        )

    record_test(
        "Device discovery",
        isinstance(discovered_devices, list)
    )

except Exception as error:

    print(
        f"Discovery error: {error}"
    )

    discovered_devices = []

    record_test(
        "Device discovery",
        False
    )


# ============================================================
# 2. SHADOW IT DETECTION
# ============================================================

print()
print("=" * 70)
print("2. SHADOW IT DETECTION")
print("=" * 70)

try:

    detected_devices = detect_shadow_it(
        discovered_devices
    )

    valid_statuses = [
        "Authorized",
        "Shadow IT"
    ]

    detection_valid = True

    for device in detected_devices:

        status = device.get(
            "status"
        )

        print(
            f"   {device.get('hostname', 'Unknown')} "
            f"-> {status}"
        )

        if status not in valid_statuses:

            detection_valid = False

    record_test(
        "Shadow IT detection",
        detection_valid
    )

except Exception as error:

    print(
        f"Detection error: {error}"
    )

    detected_devices = []

    record_test(
        "Shadow IT detection",
        False
    )


# ============================================================
# 3. FEATURE ENGINEERING
# ============================================================

print()
print("=" * 70)
print("3. FEATURE ENGINEERING")
print("=" * 70)

FEATURE_COLUMNS = [
    "unknown_device",
    "open_port_count",
    "critical_cve_count",
    "patch_status",
    "os_outdated",
    "sensitive_network_access"
]

processed_devices = []

feature_test_passed = True

for device in detected_devices:

    try:

        features = extract_features(
            device
        )

        missing_features = [
            feature
            for feature in FEATURE_COLUMNS
            if feature not in features
        ]

        if missing_features:

            feature_test_passed = False

            print(
                f"   Missing features: "
                f"{missing_features}"
            )

            continue

        device["features"] = features

        processed_devices.append(
            device
        )

        print(
            f"   {device.get('hostname', 'Unknown')}"
        )

        for feature in FEATURE_COLUMNS:

            print(
                f"      {feature:<30}: "
                f"{features[feature]}"
            )

    except Exception as error:

        print(
            f"   Feature error: {error}"
        )

        feature_test_passed = False


record_test(
    "Feature engineering",
    feature_test_passed
)


# ============================================================
# 4. AI RISK PREDICTION
# ============================================================

print()
print("=" * 70)
print("4. AI RISK PREDICTION")
print("=" * 70)

prediction_test_passed = True

valid_risks = [
    "Low",
    "Medium",
    "High",
    "Critical"
]

for device in processed_devices:

    try:

        prediction = predict_risk(
            device["features"]
        )

        risk = prediction.get(
            "risk"
        )

        confidence = prediction.get(
            "confidence"
        )

        probabilities = prediction.get(
            "probabilities"
        )

        print(
            f"   {device.get('hostname', 'Unknown')}"
        )

        print(
            f"      Risk       : {risk}"
        )

        print(
            f"      Confidence : {confidence}%"
        )

        print(
            f"      Probabilities: "
            f"{probabilities}"
        )

        if risk not in valid_risks:

            prediction_test_passed = False

        if not isinstance(
            confidence,
            (int, float)
        ):

            prediction_test_passed = False

        if not isinstance(
            probabilities,
            dict
        ):

            prediction_test_passed = False

        device["risk"] = risk

        device["confidence"] = confidence

        device["probabilities"] = probabilities

    except Exception as error:

        print(
            f"   Prediction error: {error}"
        )

        prediction_test_passed = False


record_test(
    "AI risk prediction",
    prediction_test_passed
)


# ============================================================
# 5. SECURITY IMPACT ANALYSIS
# ============================================================

print()
print("=" * 70)
print("5. SECURITY IMPACT ANALYSIS")
print("=" * 70)

impact_test_passed = True

for device in processed_devices:

    try:

        impacts = analyze_impact(
            device
        )

        print(
            f"   {device.get('hostname', 'Unknown')}"
        )

        if impacts:

            for impact in impacts:

                print(
                    f"      - {impact}"
                )

        else:

            print(
                "      No security impacts detected."
            )

        if not isinstance(
            impacts,
            list
        ):

            impact_test_passed = False

        device["security_impacts"] = impacts

    except Exception as error:

        print(
            f"   Impact error: {error}"
        )

        impact_test_passed = False


record_test(
    "Security impact analysis",
    impact_test_passed
)


# ============================================================
# 6. DECISION ENGINE
# ============================================================

print()
print("=" * 70)
print("6. DECISION ENGINE")
print("=" * 70)

decision_test_passed = True

for device in processed_devices:

    try:

        features = device[
            "features"
        ]

        decision_input = {

            "unknown_device":
                features["unknown_device"],

            "open_port_count":
                features["open_port_count"],

            "critical_cve_count":
                features["critical_cve_count"],

            "patch_status":
                features["patch_status"],

            "os_outdated":
                features["os_outdated"],

            "sensitive_network_access":
                features[
                    "sensitive_network_access"
                ],

            "risk":
                device["risk"],

            "confidence":
                device["confidence"]
        }

        decision = generate_decision(
            decision_input
        )

        print(
            f"   {device.get('hostname', 'Unknown')}"
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

        required_decision_fields = [
            "risk_level",
            "confidence",
            "priority",
            "primary_decision",
            "severity",
            "severity_score",
            "response_time",
            "recommended_actions"
        ]

        for field in required_decision_fields:

            if field not in decision:

                decision_test_passed = False

        device["decision"] = decision

    except Exception as error:

        print(
            f"   Decision error: {error}"
        )

        decision_test_passed = False


record_test(
    "Decision engine",
    decision_test_passed
)


# ============================================================
# 7. COMPLETE PIPELINE VALIDATION
# ============================================================

print()
print("=" * 70)
print("7. COMPLETE PIPELINE VALIDATION")
print("=" * 70)

pipeline_test_passed = True

required_device_fields = [
    "hostname",
    "ip",
    "ports",
    "status",
    "features",
    "risk",
    "confidence",
    "probabilities",
    "security_impacts",
    "decision"
]

for device in processed_devices:

    missing_fields = [
        field
        for field in required_device_fields
        if field not in device
    ]

    if missing_fields:

        pipeline_test_passed = False

        print(
            f"   Missing fields for "
            f"{device.get('hostname', 'Unknown')}: "
            f"{missing_fields}"
        )

    else:

        print(
            f"   {device.get('hostname', 'Unknown')}"
            " -> COMPLETE"
        )


if len(processed_devices) == 0:

    pipeline_test_passed = False


record_test(
    "Complete pipeline validation",
    pipeline_test_passed
)


# ============================================================
# 8. FINAL DATA CONSISTENCY
# ============================================================

print()
print("=" * 70)
print("8. FINAL DATA CONSISTENCY")
print("=" * 70)

consistency_test_passed = True

for device in processed_devices:

    risk = device.get(
        "risk"
    )

    decision = device.get(
        "decision",
        {}
    )

    decision_risk = decision.get(
        "risk_level"
    )

    if risk != decision_risk:

        print(
            f"   Risk mismatch: "
            f"{risk} != {decision_risk}"
        )

        consistency_test_passed = False

    else:

        print(
            f"   {device.get('hostname', 'Unknown')} "
            f"-> Risk consistent: {risk}"
        )


record_test(
    "Final data consistency",
    consistency_test_passed
)


# ============================================================
# FINAL RESULT
# ============================================================

print()
print("=" * 70)
print("MODULE 23 FINAL RESULT")
print("=" * 70)

print(
    f"Tests Passed : {tests_passed}"
)

print(
    f"Tests Failed : {tests_failed}"
)

print(
    f"Total Tests  : "
    f"{tests_passed + tests_failed}"
)

print(
    f"Devices Processed : "
    f"{len(processed_devices)}"
)

print()

if tests_failed == 0:

    print(
        "MODULE 23 FINAL SYSTEM VALIDATION: PASSED"
    )

    print()

    print(
        "Scanner -> Shadow IT -> Features -> "
        "AI -> Impact -> Decision"
    )

    print()

    print(
        "COMPLETE SHADOW IT AI PIPELINE VERIFIED"
    )

else:

    print(
        "MODULE 23 FINAL SYSTEM VALIDATION: FAILED"
    )

print("=" * 70)


# ============================================================
# EXIT STATUS
# ============================================================

if tests_failed > 0:

    raise SystemExit(1)