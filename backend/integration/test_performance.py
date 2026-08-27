# ============================================================
# SHADOW IT AI
# MODULE 21 - PERFORMANCE & STABILITY TEST
# ============================================================

import sys
import time
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

from ai.feature_extractor import extract_features
from ai.predict import predict_risk
from impact.impact_analyzer import analyze_impact
from decision.decision_engine import generate_decision


# ============================================================
# CONFIGURATION
# ============================================================

NUMBER_OF_DEVICES = 100
NUMBER_OF_RUNS = 5


# ============================================================
# TEST DEVICE GENERATOR
# ============================================================

def generate_test_devices(count):

    devices = []

    for i in range(count):

        device = {

            "hostname":
                f"test-device-{i}",

            "ip":
                f"192.168.1.{(i % 250) + 1}",

            "mac":
                "",

            "os":
                "Windows 11",

            "ports":
                [80, 443],

            "status":
                "Authorized",

            "critical_cve_count":
                0,

            "patch_status":
                1,

            "os_outdated":
                0,

            "sensitive_network_access":
                0
        }

        devices.append(device)

    return devices


# ============================================================
# PROCESS ONE DEVICE
# ============================================================

def process_device(device):

    # --------------------------------------------------------
    # FEATURE EXTRACTION
    # --------------------------------------------------------

    features = extract_features(
        device
    )

    # --------------------------------------------------------
    # AI PREDICTION
    # --------------------------------------------------------

    prediction = predict_risk(
        features
    )

    # --------------------------------------------------------
    # IMPACT ANALYSIS
    # --------------------------------------------------------

    impact_device = dict(device)

    impact_device["features"] = features

    impacts = analyze_impact(
        impact_device
    )

    # --------------------------------------------------------
    # DECISION ENGINE
    # --------------------------------------------------------

    decision_input = {

        **features,

        "risk":
            prediction["risk"],

        "confidence":
            prediction["confidence"]
    }

    decision = generate_decision(
        decision_input
    )

    return {

        "features":
            features,

        "prediction":
            prediction,

        "impacts":
            impacts,

        "decision":
            decision
    }


# ============================================================
# TEST 1 - SINGLE DEVICE PERFORMANCE
# ============================================================

def test_single_device():

    device = generate_test_devices(1)[0]

    start_time = time.perf_counter()

    result = process_device(
        device
    )

    elapsed = (
        time.perf_counter()
        - start_time
    )

    assert result is not None
    assert "prediction" in result
    assert "decision" in result

    return elapsed


# ============================================================
# TEST 2 - MULTIPLE DEVICE PROCESSING
# ============================================================

def test_multiple_devices():

    devices = generate_test_devices(
        NUMBER_OF_DEVICES
    )

    start_time = time.perf_counter()

    results = []

    for device in devices:

        result = process_device(
            device
        )

        results.append(
            result
        )

    elapsed = (
        time.perf_counter()
        - start_time
    )

    assert len(results) == NUMBER_OF_DEVICES

    for result in results:

        assert "prediction" in result
        assert "decision" in result

    return elapsed


# ============================================================
# TEST 3 - REPEATED PROCESSING
# ============================================================

def test_repeated_processing():

    devices = generate_test_devices(
        20
    )

    start_time = time.perf_counter()

    total_processed = 0

    for _ in range(NUMBER_OF_RUNS):

        for device in devices:

            result = process_device(
                device
            )

            assert result is not None

            total_processed += 1

    elapsed = (
        time.perf_counter()
        - start_time
    )

    expected = (
        20 * NUMBER_OF_RUNS
    )

    assert total_processed == expected

    return elapsed, total_processed


# ============================================================
# TEST 4 - RISK DISTRIBUTION
# ============================================================

def test_risk_distribution():

    devices = [

        {
            "hostname": "low-device",
            "status": "Authorized",
            "os": "Windows 11",
            "ports": [80, 443],
            "critical_cve_count": 0,
            "patch_status": 1,
            "os_outdated": 0,
            "sensitive_network_access": 0
        },

        {
            "hostname": "shadow-device",
            "status": "Shadow IT",
            "os": "Windows 11",
            "ports": [80, 443],
            "critical_cve_count": 0,
            "patch_status": 1,
            "os_outdated": 0,
            "sensitive_network_access": 0
        },

        {
            "hostname": "high-risk-device",
            "status": "Shadow IT",
            "os": "Windows 7",
            "ports": [
                21,
                23,
                445,
                3389,
                3306,
                8080
            ],
            "critical_cve_count": 3,
            "patch_status": 0,
            "os_outdated": 1,
            "sensitive_network_access": 1
        }
    ]

    risks = []

    for device in devices:

        result = process_device(
            device
        )

        risk = result[
            "prediction"
        ]["risk"]

        risks.append(
            risk
        )

    assert len(risks) == 3

    for risk in risks:

        assert risk in [
            "Low",
            "Medium",
            "High",
            "Critical"
        ]

    return risks


# ============================================================
# TEST 5 - MEMORY / RESULT STABILITY
# ============================================================

def test_result_stability():

    device = generate_test_devices(
        1
    )[0]

    results = []

    for _ in range(10):

        result = process_device(
            device
        )

        results.append(
            result
        )

    first_risk = results[0][
        "prediction"
    ]["risk"]

    first_confidence = results[0][
        "prediction"
    ]["confidence"]

    for result in results:

        assert result[
            "prediction"
        ]["risk"] == first_risk

        assert result[
            "prediction"
        ]["confidence"] == first_confidence

    return True


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print("#" * 70)
    print("# SHADOW IT AI")
    print("# MODULE 21 - PERFORMANCE & STABILITY TEST")
    print("#" * 70)

    passed = 0
    failed = 0

    # ========================================================
    # TEST 1
    # ========================================================

    print()
    print("=" * 70)
    print("1. SINGLE DEVICE PERFORMANCE")
    print("=" * 70)

    try:

        elapsed = test_single_device()

        print(
            f"Processing Time : "
            f"{elapsed:.6f} seconds"
        )

        print(
            "Single device processing: PASS"
        )

        passed += 1

    except Exception as error:

        print(
            "Single device processing: FAIL"
        )

        print(
            f"Error: {error}"
        )

        failed += 1

    # ========================================================
    # TEST 2
    # ========================================================

    print()
    print("=" * 70)
    print(
        f"2. MULTIPLE DEVICE PERFORMANCE "
        f"({NUMBER_OF_DEVICES} DEVICES)"
    )
    print("=" * 70)

    try:

        elapsed = test_multiple_devices()

        average = (
            elapsed
            / NUMBER_OF_DEVICES
        )

        print(
            f"Devices Processed : "
            f"{NUMBER_OF_DEVICES}"
        )

        print(
            f"Total Time        : "
            f"{elapsed:.6f} seconds"
        )

        print(
            f"Average / Device  : "
            f"{average:.6f} seconds"
        )

        print(
            "Multiple device processing: PASS"
        )

        passed += 1

    except Exception as error:

        print(
            "Multiple device processing: FAIL"
        )

        print(
            f"Error: {error}"
        )

        failed += 1

    # ========================================================
    # TEST 3
    # ========================================================

    print()
    print("=" * 70)
    print(
        f"3. REPEATED PROCESSING "
        f"({NUMBER_OF_RUNS} RUNS)"
    )
    print("=" * 70)

    try:

        elapsed, total_processed = (
            test_repeated_processing()
        )

        print(
            f"Total Devices Processed : "
            f"{total_processed}"
        )

        print(
            f"Total Time              : "
            f"{elapsed:.6f} seconds"
        )

        print(
            "Repeated processing: PASS"
        )

        passed += 1

    except Exception as error:

        print(
            "Repeated processing: FAIL"
        )

        print(
            f"Error: {error}"
        )

        failed += 1

    # ========================================================
    # TEST 4
    # ========================================================

    print()
    print("=" * 70)
    print("4. RISK DISTRIBUTION STABILITY")
    print("=" * 70)

    try:

        risks = test_risk_distribution()

        print(
            f"Risk Results : {risks}"
        )

        print(
            "Risk distribution: PASS"
        )

        passed += 1

    except Exception as error:

        print(
            "Risk distribution: FAIL"
        )

        print(
            f"Error: {error}"
        )

        failed += 1

    # ========================================================
    # TEST 5
    # ========================================================

    print()
    print("=" * 70)
    print("5. RESULT STABILITY")
    print("=" * 70)

    try:

        test_result_stability()

        print(
            "Repeated predictions remained stable."
        )

        print(
            "Result stability: PASS"
        )

        passed += 1

    except Exception as error:

        print(
            "Result stability: FAIL"
        )

        print(
            f"Error: {error}"
        )

        failed += 1

    # ========================================================
    # FINAL RESULT
    # ========================================================

    print()
    print("=" * 70)
    print("MODULE 21 FINAL RESULT")
    print("=" * 70)

    print(
        f"Tests Passed : {passed}"
    )

    print(
        f"Tests Failed : {failed}"
    )

    print(
        f"Total Tests  : 5"
    )

    print()

    if failed == 0:

        print(
            "MODULE 21 PERFORMANCE & STABILITY TEST: PASSED"
        )

        print(
            "Performance -> Repeated Processing -> "
            "Risk Stability -> Result Stability"
        )

        return True

    print(
        "MODULE 21 PERFORMANCE & STABILITY TEST: FAILED"
    )

    return False


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":

    success = main()

    if not success:

        raise SystemExit(1)