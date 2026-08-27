# ============================================================
# SHADOW IT AI
# MODULE 25 - APPLICATION READINESS TEST
# ============================================================

import sys
import os
import time
import requests


# ============================================================
# PROJECT ROOT
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)


# ============================================================
# CONFIGURATION
# ============================================================

API_BASE_URL = "http://127.0.0.1:8000"


# ============================================================
# TEST HELPERS
# ============================================================

passed = 0
failed = 0


def print_section(title):

    print()
    print("=" * 70)
    print(title)
    print("=" * 70)


def test_pass(message):

    global passed

    passed += 1

    print(
        f"{message}: PASS"
    )


def test_fail(message, error=None):

    global failed

    failed += 1

    print(
        f"{message}: FAIL"
    )

    if error:

        print(
            f"   Error: {error}"
        )


# ============================================================
# MODULE HEADER
# ============================================================

print()
print("#" * 70)
print("# SHADOW IT AI")
print("# MODULE 25 - APPLICATION READINESS TEST")
print("#" * 70)


# ============================================================
# 1. API SERVER AVAILABILITY
# ============================================================

print_section(
    "1. API SERVER AVAILABILITY"
)

try:

    response = requests.get(
        f"{API_BASE_URL}/api/status",
        timeout=10
    )

    print(
        f"HTTP Status: {response.status_code}"
    )

    if response.status_code == 200:

        data = response.json()

        print(
            f"Service: {data.get('service')}"
        )

        print(
            f"Version: {data.get('version')}"
        )

        test_pass(
            "API server availability"
        )

    else:

        test_fail(
            "API server availability"
        )

except Exception as error:

    test_fail(
        "API server availability",
        error
    )


# ============================================================
# 2. API STATUS RESPONSE
# ============================================================

print_section(
    "2. API STATUS VALIDATION"
)

try:

    response = requests.get(
        f"{API_BASE_URL}/api/status",
        timeout=10
    )

    data = response.json()

    required_fields = [
        "status",
        "service",
        "version"
    ]

    missing = [
        field
        for field in required_fields
        if field not in data
    ]

    if (
        response.status_code == 200
        and not missing
        and data.get("status") == "running"
    ):

        print(
            f"Status: {data.get('status')}"
        )

        print(
            f"Service: {data.get('service')}"
        )

        test_pass(
            "API status validation"
        )

    else:

        test_fail(
            "API status validation",
            f"Missing fields: {missing}"
        )

except Exception as error:

    test_fail(
        "API status validation",
        error
    )


# ============================================================
# 3. SCAN ENDPOINT
# ============================================================

print_section(
    "3. SCAN ENDPOINT"
)

try:

    start_time = time.perf_counter()

    response = requests.post(
        f"{API_BASE_URL}/scan",
        timeout=60
    )

    elapsed = (
        time.perf_counter()
        - start_time
    )

    print(
        f"HTTP Status: {response.status_code}"
    )

    print(
        f"Processing Time: "
        f"{elapsed:.4f} seconds"
    )

    if response.status_code != 200:

        raise RuntimeError(
            response.text
        )

    data = response.json()

    device_count = data.get(
        "device_count",
        0
    )

    devices = data.get(
        "devices",
        []
    )

    print(
        f"Device Count: {device_count}"
    )

    if device_count > 0:

        for device in devices:

            print(
                f"   {device.get('hostname')} "
                f"-> {device.get('risk')}"
            )

        test_pass(
            "Scan endpoint"
        )

    else:

        test_fail(
            "Scan endpoint",
            "No devices returned"
        )

except Exception as error:

    test_fail(
        "Scan endpoint",
        error
    )


# ============================================================
# 4. DEVICES ENDPOINT
# ============================================================

print_section(
    "4. DEVICES ENDPOINT"
)

try:

    response = requests.get(
        f"{API_BASE_URL}/devices",
        timeout=10
    )

    print(
        f"HTTP Status: {response.status_code}"
    )

    if response.status_code != 200:

        raise RuntimeError(
            response.text
        )

    data = response.json()

    device_count = data.get(
        "device_count",
        0
    )

    print(
        f"Stored Devices: {device_count}"
    )

    if device_count > 0:

        test_pass(
            "Devices endpoint"
        )

    else:

        test_fail(
            "Devices endpoint",
            "No stored devices"
        )

except Exception as error:

    test_fail(
        "Devices endpoint",
        error
    )


# ============================================================
# 5. DASHBOARD ENDPOINT
# ============================================================

print_section(
    "5. DASHBOARD ENDPOINT"
)

try:

    response = requests.get(
        f"{API_BASE_URL}/dashboard",
        timeout=10
    )

    print(
        f"HTTP Status: {response.status_code}"
    )

    if response.status_code != 200:

        raise RuntimeError(
            response.text
        )

    data = response.json()

    total_devices = data.get(
        "total_devices",
        0
    )

    risk_distribution = data.get(
        "risk_distribution",
        {}
    )

    print(
        f"Total Devices: {total_devices}"
    )

    print(
        f"Risk Distribution: "
        f"{risk_distribution}"
    )

    if total_devices >= 0:

        test_pass(
            "Dashboard endpoint"
        )

    else:

        test_fail(
            "Dashboard endpoint"
        )

except Exception as error:

    test_fail(
        "Dashboard endpoint",
        error
    )


# ============================================================
# 6. DEVICE DETAIL ENDPOINT
# ============================================================

print_section(
    "6. DEVICE DETAIL ENDPOINT"
)

try:

    response = requests.get(
        f"{API_BASE_URL}/device/0",
        timeout=10
    )

    print(
        f"HTTP Status: {response.status_code}"
    )

    if response.status_code != 200:

        raise RuntimeError(
            response.text
        )

    data = response.json()

    device = data.get(
        "device",
        {}
    )

    print(
        f"Hostname: "
        f"{device.get('hostname')}"
    )

    print(
        f"Risk: "
        f"{device.get('risk')}"
    )

    if device:

        test_pass(
            "Device detail endpoint"
        )

    else:

        test_fail(
            "Device detail endpoint",
            "Empty device response"
        )

except Exception as error:

    test_fail(
        "Device detail endpoint",
        error
    )


# ============================================================
# 7. IMPACT ENDPOINT
# ============================================================

print_section(
    "7. IMPACT ENDPOINT"
)

try:

    response = requests.get(
        f"{API_BASE_URL}/device/0/impact",
        timeout=10
    )

    print(
        f"HTTP Status: {response.status_code}"
    )

    if response.status_code != 200:

        raise RuntimeError(
            response.text
        )

    data = response.json()

    impacts = data.get(
        "security_impacts",
        []
    )

    print(
        f"Security Impacts: {impacts}"
    )

    if isinstance(
        impacts,
        list
    ):

        test_pass(
            "Impact endpoint"
        )

    else:

        test_fail(
            "Impact endpoint",
            "Invalid impact response"
        )

except Exception as error:

    test_fail(
        "Impact endpoint",
        error
    )


# ============================================================
# 8. DECISION ENDPOINT
# ============================================================

print_section(
    "8. DECISION ENDPOINT"
)

try:

    response = requests.get(
        f"{API_BASE_URL}/device/0/decision",
        timeout=10
    )

    print(
        f"HTTP Status: {response.status_code}"
    )

    if response.status_code != 200:

        raise RuntimeError(
            response.text
        )

    data = response.json()

    decision = data.get(
        "decision",
        {}
    )

    print(
        f"Risk: "
        f"{decision.get('risk_level')}"
    )

    print(
        f"Priority: "
        f"{decision.get('priority')}"
    )

    print(
        f"Decision: "
        f"{decision.get('primary_decision')}"
    )

    if decision:

        test_pass(
            "Decision endpoint"
        )

    else:

        test_fail(
            "Decision endpoint",
            "Empty decision response"
        )

except Exception as error:

    test_fail(
        "Decision endpoint",
        error
    )


# ============================================================
# 9. APPLICATION COMPONENT CONSISTENCY
# ============================================================

print_section(
    "9. APPLICATION COMPONENT CONSISTENCY"
)

try:

    response = requests.get(
        f"{API_BASE_URL}/device/0",
        timeout=10
    )

    data = response.json()

    device = data.get(
        "device",
        {}
    )

    features = device.get(
        "features",
        {}
    )

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

    checks = [

        bool(features),

        risk in [
            "Low",
            "Medium",
            "High",
            "Critical"
        ],

        decision_risk == risk,

        bool(decision),
    ]

    print(
        f"Features available : "
        f"{bool(features)}"
    )

    print(
        f"Risk valid         : "
        f"{risk in ['Low', 'Medium', 'High', 'Critical']}"
    )

    print(
        f"Risk consistency    : "
        f"{decision_risk == risk}"
    )

    print(
        f"Decision available  : "
        f"{bool(decision)}"
    )

    if all(checks):

        test_pass(
            "Application component consistency"
        )

    else:

        test_fail(
            "Application component consistency"
        )

except Exception as error:

    test_fail(
        "Application component consistency",
        error
    )


# ============================================================
# 10. FINAL APPLICATION READINESS
# ============================================================

print_section(
    "10. FINAL APPLICATION READINESS"
)

if failed == 0:

    print(
        "All application readiness checks passed."
    )

    test_pass(
        "Application readiness"
    )

else:

    test_fail(
        "Application readiness",
        f"{failed} previous test(s) failed"
    )


# ============================================================
# FINAL RESULT
# ============================================================

print_section(
    "MODULE 25 FINAL RESULT"
)

total = passed + failed

print(
    f"Tests Passed : {passed}"
)

print(
    f"Tests Failed : {failed}"
)

print(
    f"Total Tests  : {total}"
)

print()

if failed == 0:

    print(
        "MODULE 25 APPLICATION READINESS TEST: PASSED"
    )

    print()

    print(
        "FastAPI -> Scan -> Devices -> Dashboard "
        "-> Impact -> Decision"
    )

    print()

    print(
        "APPLICATION READY FOR FINAL DEPLOYMENT"
    )

else:

    print(
        "MODULE 25 APPLICATION READINESS TEST: FAILED"
    )

    print()

    print(
        "Fix the failed checks before proceeding."
    )

    sys.exit(1)

print(
    "=" * 70
)