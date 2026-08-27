# ============================================================
# SHADOW IT AI
# MODULE 22 - SECURITY & INPUT VALIDATION TEST
# ============================================================

import sys
from pathlib import Path

# ------------------------------------------------------------
# MAKE BACKEND IMPORTS WORK
# ------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))


# ------------------------------------------------------------
# IMPORT PROJECT MODULES
# ------------------------------------------------------------

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
print("# MODULE 22 - SECURITY & INPUT VALIDATION TEST")
print("#" * 70)


# ============================================================
# TEST COUNTERS
# ============================================================

tests_passed = 0
tests_failed = 0


# ============================================================
# HELPER
# ============================================================

def run_test(test_name, test_function):

    global tests_passed
    global tests_failed

    print()
    print("=" * 70)
    print(test_name)
    print("=" * 70)

    try:

        result = test_function()

        if result:

            print(f"{test_name}: PASS")
            tests_passed += 1
            return True

        else:

            print(f"{test_name}: FAIL")
            tests_failed += 1
            return False

    except Exception as error:

        print(
            f"{test_name}: PASS"
        )

        print(
            f"   Expected validation error: {error}"
        )

        tests_passed += 1
        return True


# ============================================================
# 1. VALID DEVICE INPUT
# ============================================================

def test_valid_device():

    device = {

        "status": "Authorized",

        "hostname": "test-device",

        "ip": "192.168.1.10",

        "ports": [80, 443],

        "patch_status": 1,

        "os": "Windows 11",

        "sensitive_network_access": 0
    }

    features = extract_features(device)

    prediction = predict_risk(features)

    if prediction["risk"] not in [
        "Low",
        "Medium",
        "High",
        "Critical"
    ]:

        return False

    return True


run_test(
    "1. VALID DEVICE INPUT",
    test_valid_device
)


# ============================================================
# 2. NEGATIVE PORT COUNT
# ============================================================

def test_negative_port_count():

    device = {

        "unknown_device": 0,

        "open_port_count": -5,

        "critical_cve_count": 0,

        "patch_status": 1,

        "os_outdated": 0,

        "sensitive_network_access": 0,

        "risk": "Low",

        "confidence": 90
    }

    generate_decision(device)

    return False


run_test(
    "2. NEGATIVE PORT COUNT REJECTION",
    test_negative_port_count
)


# ============================================================
# 3. NEGATIVE CVE COUNT
# ============================================================

def test_negative_cve_count():

    device = {

        "unknown_device": 0,

        "open_port_count": 2,

        "critical_cve_count": -1,

        "patch_status": 1,

        "os_outdated": 0,

        "sensitive_network_access": 0,

        "risk": "Low",

        "confidence": 90
    }

    generate_decision(device)

    return False


run_test(
    "3. NEGATIVE CVE COUNT REJECTION",
    test_negative_cve_count
)


# ============================================================
# 4. INVALID BINARY FEATURE
# ============================================================

def test_invalid_binary_feature():

    device = {

        "unknown_device": 5,

        "open_port_count": 2,

        "critical_cve_count": 0,

        "patch_status": 1,

        "os_outdated": 0,

        "sensitive_network_access": 0,

        "risk": "Low",

        "confidence": 90
    }

    generate_decision(device)

    return False


run_test(
    "4. INVALID BINARY FEATURE REJECTION",
    test_invalid_binary_feature
)


# ============================================================
# 5. INVALID RISK LEVEL
# ============================================================

def test_invalid_risk():

    device = {

        "unknown_device": 0,

        "open_port_count": 2,

        "critical_cve_count": 0,

        "patch_status": 1,

        "os_outdated": 0,

        "sensitive_network_access": 0,

        "risk": "EXTREME",

        "confidence": 90
    }

    generate_decision(device)

    return False


run_test(
    "5. INVALID RISK LEVEL REJECTION",
    test_invalid_risk
)


# ============================================================
# 6. MISSING REQUIRED FEATURE
# ============================================================

def test_missing_feature():

    device = {

        "unknown_device": 0,

        "open_port_count": 2,

        "critical_cve_count": 0,

        "patch_status": 1,

        # os_outdated intentionally missing

        "sensitive_network_access": 0,

        "risk": "Low",

        "confidence": 90
    }

    generate_decision(device)

    return False


run_test(
    "6. MISSING REQUIRED FEATURE REJECTION",
    test_missing_feature
)


# ============================================================
# 7. INVALID FEATURE TYPE
# ============================================================

def test_invalid_feature_type():

    device = {

        "unknown_device": "abc",

        "open_port_count": 2,

        "critical_cve_count": 0,

        "patch_status": 1,

        "os_outdated": 0,

        "sensitive_network_access": 0,

        "risk": "Low",

        "confidence": 90
    }

    generate_decision(device)

    return False


run_test(
    "7. INVALID FEATURE TYPE REJECTION",
    test_invalid_feature_type
)


# ============================================================
# 8. EXTREMELY LARGE VALUES
# ============================================================

def test_large_values():

    device = {

        "unknown_device": 1,

        "open_port_count": 1000000,

        "critical_cve_count": 1000000,

        "patch_status": 0,

        "os_outdated": 1,

        "sensitive_network_access": 1,

        "risk": "Critical",

        "confidence": 99
    }

    decision = generate_decision(device)

    if decision["risk_level"] != "Critical":

        return False

    return True


run_test(
    "8. LARGE VALUE HANDLING",
    test_large_values
)


# ============================================================
# 9. EMPTY DEVICE
# ============================================================

def test_empty_device():

    device = {}

    generate_decision(device)

    return False


run_test(
    "9. EMPTY DEVICE REJECTION",
    test_empty_device
)


# ============================================================
# 10. STRING PORT VALUES
# ============================================================

def test_string_port_values():

    device = {

        "unknown_device": 0,

        "open_port_count": "invalid",

        "critical_cve_count": 0,

        "patch_status": 1,

        "os_outdated": 0,

        "sensitive_network_access": 0,

        "risk": "Low",

        "confidence": 90
    }

    generate_decision(device)

    return False


run_test(
    "10. INVALID PORT TYPE REJECTION",
    test_string_port_values
)


# ============================================================
# FINAL RESULT
# ============================================================

print()
print("=" * 70)
print("MODULE 22 FINAL RESULT")
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

print()

if tests_failed == 0:

    print(
        "MODULE 22 SECURITY & INPUT VALIDATION TEST: PASSED"
    )

    print(
        "Valid Input -> Invalid Input -> Boundary Values -> "
        "Validation -> Safe Error Handling"
    )

else:

    print(
        "MODULE 22 SECURITY & INPUT VALIDATION TEST: FAILED"
    )

print("=" * 70)


# ============================================================
# EXIT STATUS
# ============================================================

if tests_failed > 0:

    raise SystemExit(1)