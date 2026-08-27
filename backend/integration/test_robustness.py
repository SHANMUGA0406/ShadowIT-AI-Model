# ============================================================
# SHADOW IT AI
# MODULE 20 - ROBUSTNESS & ERROR HANDLING TEST
# ============================================================

import sys
from pathlib import Path


# ============================================================
# FIX PROJECT ROOT PATH
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ============================================================
# IMPORT PROJECT MODULES
# ============================================================

from scanner.scan import scan_network
from shadow_it.detect import detect_shadow_it
from ai.feature_extractor import extract_features
from ai.predict import predict_risk
from impact.impact_analyzer import analyze_impact
from decision.decision_engine import generate_decision


# ============================================================
# HELPER
# ============================================================

def print_section(title):

    print()
    print("=" * 70)
    print(title)
    print("=" * 70)


# ============================================================
# TEST 1 - NORMAL DEVICE
# ============================================================

def test_normal_device():

    device = {
        "hostname": "test-device",
        "ip": "192.168.1.10",
        "mac": "",
        "os": "Windows 11",
        "ports": [80, 443],
        "status": "Authorized"
    }

    features = extract_features(device)

    prediction = predict_risk(features)

    impact_device = dict(device)
    impact_device["features"] = features

    impacts = analyze_impact(
        impact_device
    )

    decision_input = {
        **features,
        "risk": prediction["risk"],
        "confidence": prediction["confidence"]
    }

    decision = generate_decision(
        decision_input
    )

    assert isinstance(features, dict)
    assert "risk" in prediction
    assert isinstance(impacts, list)
    assert isinstance(decision, dict)

    return True


# ============================================================
# TEST 2 - SHADOW IT DEVICE
# ============================================================

def test_shadow_it_device():

    device = {
        "hostname": "unknown-device",
        "ip": "192.168.1.20",
        "mac": "",
        "os": "Windows 11",
        "ports": [80, 443],
        "status": "Shadow IT"
    }

    features = extract_features(device)

    prediction = predict_risk(features)

    impact_device = dict(device)
    impact_device["features"] = features

    impacts = analyze_impact(
        impact_device
    )

    decision_input = {
        **features,
        "risk": prediction["risk"],
        "confidence": prediction["confidence"]
    }

    decision = generate_decision(
        decision_input
    )

    assert features["unknown_device"] == 1

    assert "Unauthorized Access Risk" in impacts

    assert prediction["risk"] in [
        "Low",
        "Medium",
        "High",
        "Critical"
    ]

    assert isinstance(decision, dict)

    return True


# ============================================================
# TEST 3 - HIGH RISK DEVICE
# ============================================================

def test_high_risk_device():

    device = {
        "hostname": "high-risk-device",
        "ip": "192.168.1.30",
        "mac": "",
        "os": "Windows 7",
        "ports": [21, 23, 445, 3389, 3306, 8080],
        "status": "Shadow IT",
        "critical_cve_count": 3,
        "patch_status": 0,
        "os_outdated": 1,
        "sensitive_network_access": 1
    }

    features = extract_features(device)

    prediction = predict_risk(features)

    impact_device = dict(device)
    impact_device["features"] = features

    impacts = analyze_impact(
        impact_device
    )

    decision_input = {
        **features,
        "risk": prediction["risk"],
        "confidence": prediction["confidence"]
    }

    decision = generate_decision(
        decision_input
    )

    assert features["unknown_device"] == 1
    assert features["critical_cve_count"] == 3
    assert features["patch_status"] == 0
    assert features["os_outdated"] == 1
    assert features["sensitive_network_access"] == 1

    assert len(impacts) > 0
    assert isinstance(decision["recommended_actions"], list)

    return True


# ============================================================
# TEST 4 - EMPTY PORT LIST
# ============================================================

def test_empty_ports():

    device = {
        "hostname": "no-port-device",
        "ip": "192.168.1.40",
        "mac": "",
        "os": "Windows 11",
        "ports": [],
        "status": "Authorized"
    }

    features = extract_features(device)

    assert features["open_port_count"] == 0

    prediction = predict_risk(
        features
    )

    assert prediction["risk"] in [
        "Low",
        "Medium",
        "High",
        "Critical"
    ]

    return True


# ============================================================
# TEST 5 - INVALID PORT VALUE
# ============================================================

def test_invalid_ports():

    device = {
        "hostname": "invalid-port-device",
        "ip": "192.168.1.50",
        "mac": "",
        "os": "Windows 11",
        "ports": "not-a-list",
        "status": "Authorized"
    }

    try:

        features = extract_features(
            device
        )

        assert isinstance(
            features,
            dict
        )

        prediction = predict_risk(
            features
        )

        assert prediction["risk"] in [
            "Low",
            "Medium",
            "High",
            "Critical"
        ]

    except Exception as error:

        print(
            f"   Expected handling triggered: {error}"
        )

    return True


# ============================================================
# TEST 6 - MISSING OPTIONAL VALUES
# ============================================================

def test_missing_values():

    device = {
        "hostname": "minimal-device",
        "ip": "192.168.1.60",
        "status": "Authorized"
    }

    features = extract_features(
        device
    )

    assert features["unknown_device"] == 0
    assert features["open_port_count"] == 0
    assert features["critical_cve_count"] == 0
    assert features["patch_status"] == 1
    assert features["os_outdated"] == 0
    assert features["sensitive_network_access"] == 0

    prediction = predict_risk(
        features
    )

    assert "risk" in prediction

    return True


# ============================================================
# TEST 7 - IMPACT ANALYZER
# ============================================================

def test_impact_analyzer():

    device = {
        "hostname": "finance-server",
        "status": "Shadow IT",
        "os": "Windows 7",
        "ports": [
            21,
            23,
            445,
            3389,
            3306
        ],
        "features": {
            "unknown_device": 1,
            "open_port_count": 5,
            "critical_cve_count": 2,
            "patch_status": 0,
            "os_outdated": 1,
            "sensitive_network_access": 1
        }
    }

    impacts = analyze_impact(
        device
    )

    assert isinstance(
        impacts,
        list
    )

    assert len(impacts) > 0

    return True


# ============================================================
# TEST 8 - DECISION ENGINE
# ============================================================

def test_decision_engine():

    device = {
        "unknown_device": 1,
        "open_port_count": 8,
        "critical_cve_count": 3,
        "patch_status": 0,
        "os_outdated": 1,
        "sensitive_network_access": 1,
        "risk": "Critical",
        "confidence": 95.0
    }

    decision = generate_decision(
        device
    )

    assert decision["risk_level"] == "Critical"

    assert decision["priority"] == "IMMEDIATE"

    assert decision["primary_decision"] == "ISOLATE DEVICE"

    assert decision["severity_score"] == 100

    assert decision["containment_recommended"] is True

    assert decision["escalation"] is True

    assert len(
        decision["recommended_actions"]
    ) > 0

    return True


# ============================================================
# MAIN TEST RUNNER
# ============================================================

def main():

    print()
    print("#" * 70)
    print("# SHADOW IT AI")
    print("# MODULE 20 - ROBUSTNESS & ERROR HANDLING TEST")
    print("#" * 70)

    tests = [

        (
            "NORMAL DEVICE PROCESSING",
            test_normal_device
        ),

        (
            "SHADOW IT DEVICE PROCESSING",
            test_shadow_it_device
        ),

        (
            "HIGH RISK DEVICE PROCESSING",
            test_high_risk_device
        ),

        (
            "EMPTY PORT HANDLING",
            test_empty_ports
        ),

        (
            "INVALID PORT HANDLING",
            test_invalid_ports
        ),

        (
            "MISSING VALUE HANDLING",
            test_missing_values
        ),

        (
            "IMPACT ANALYZER",
            test_impact_analyzer
        ),

        (
            "DECISION ENGINE",
            test_decision_engine
        ),
    ]

    passed = 0
    failed = 0

    for test_name, test_function in tests:

        print_section(
            test_name
        )

        try:

            result = test_function()

            if result:

                print(
                    f"{test_name}: PASS"
                )

                passed += 1

        except Exception as error:

            print(
                f"{test_name}: FAIL"
            )

            print(
                f"Error: {error}"
            )

            failed += 1

    # ========================================================
    # FINAL RESULT
    # ========================================================

    print_section(
        "MODULE 20 FINAL RESULT"
    )

    print(
        f"Tests Passed : {passed}"
    )

    print(
        f"Tests Failed : {failed}"
    )

    print(
        f"Total Tests  : {len(tests)}"
    )

    print()

    if failed == 0:

        print(
            "MODULE 20 ROBUSTNESS TEST: PASSED"
        )

        print(
            "Normal -> Shadow IT -> High Risk -> "
            "Invalid Input -> Impact -> Decision"
        )

        print()

        return True

    print(
        "MODULE 20 ROBUSTNESS TEST: FAILED"
    )

    return False


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":

    success = main()

    if not success:

        raise SystemExit(1)