# ============================================================
# SHADOW IT AI
# MODULE 28 - DEPLOYMENT SMOKE TEST
# ============================================================

import requests
import time


BASE_URL = "http://127.0.0.1:8000"


print()
print("#" * 70)
print("# SHADOW IT AI")
print("# MODULE 28 - DEPLOYMENT SMOKE TEST")
print("#" * 70)


passed = 0
failed = 0


def check(name, condition):

    global passed, failed

    if condition:
        print(f"   {name:<45}: PASS")
        passed += 1
    else:
        print(f"   {name:<45}: FAIL")
        failed += 1


# ============================================================
# 1. SERVER CONNECTION
# ============================================================

print()
print("=" * 70)
print("1. SERVER CONNECTION")
print("=" * 70)

try:

    start = time.time()

    response = requests.get(
        f"{BASE_URL}/api/status",
        timeout=10
    )

    elapsed = time.time() - start

    print(f"   HTTP Status : {response.status_code}")
    print(f"   Response Time: {elapsed:.4f} seconds")

    check(
        "FastAPI server reachable",
        response.status_code == 200
    )

except Exception as error:

    print("   Server connection error:", error)

    check(
        "FastAPI server reachable",
        False
    )


# ============================================================
# 2. API STATUS
# ============================================================

print()
print("=" * 70)
print("2. API STATUS")
print("=" * 70)

try:

    data = response.json()

    print("   Status  :", data.get("status"))
    print("   Service :", data.get("service"))
    print("   Version :", data.get("version"))

    check(
        "API status is running",
        data.get("status") == "running"
    )

except Exception as error:

    print("   Status validation error:", error)

    check(
        "API status is running",
        False
    )


# ============================================================
# 3. ROOT ENDPOINT
# ============================================================

print()
print("=" * 70)
print("3. ROOT ENDPOINT")
print("=" * 70)

try:

    response = requests.get(
        f"{BASE_URL}/",
        timeout=10
    )

    print("   HTTP Status:", response.status_code)

    if response.status_code == 200:

        print(
            "   Response:",
            response.json()
        )

    check(
        "Root endpoint available",
        response.status_code == 200
    )

except Exception as error:

    print("   Root endpoint error:", error)

    check(
        "Root endpoint available",
        False
    )


# ============================================================
# 4. SCAN ENDPOINT
# ============================================================

print()
print("=" * 70)
print("4. SCAN ENDPOINT")
print("=" * 70)

scan_success = False
device_count = 0

try:

    start = time.time()

    response = requests.post(
        f"{BASE_URL}/scan",
        timeout=60
    )

    elapsed = time.time() - start

    print("   HTTP Status :", response.status_code)
    print(f"   Scan Time   : {elapsed:.4f} seconds")

    if response.status_code == 200:

        data = response.json()

        device_count = data.get(
            "device_count",
            0
        )

        print(
            "   Device Count:",
            device_count
        )

        scan_success = (
            data.get("status") == "success"
        )

    check(
        "Scan endpoint operational",
        scan_success
    )

except Exception as error:

    print("   Scan error:", error)

    check(
        "Scan endpoint operational",
        False
    )


# ============================================================
# 5. DEVICES ENDPOINT
# ============================================================

print()
print("=" * 70)
print("5. DEVICES ENDPOINT")
print("=" * 70)

try:

    response = requests.get(
        f"{BASE_URL}/devices",
        timeout=10
    )

    print("   HTTP Status:", response.status_code)

    if response.status_code == 200:

        data = response.json()

        print(
            "   Stored Devices:",
            data.get("device_count")
        )

    check(
        "Devices endpoint operational",
        response.status_code == 200
    )

except Exception as error:

    print("   Devices endpoint error:", error)

    check(
        "Devices endpoint operational",
        False
    )


# ============================================================
# 6. DASHBOARD ENDPOINT
# ============================================================

print()
print("=" * 70)
print("6. DASHBOARD ENDPOINT")
print("=" * 70)

try:

    response = requests.get(
        f"{BASE_URL}/dashboard",
        timeout=10
    )

    print("   HTTP Status:", response.status_code)

    if response.status_code == 200:

        data = response.json()

        print(
            "   Total Devices:",
            data.get("total_devices")
        )

        print(
            "   Risk Distribution:",
            data.get("risk_distribution")
        )

    check(
        "Dashboard endpoint operational",
        response.status_code == 200
    )

except Exception as error:

    print("   Dashboard endpoint error:", error)

    check(
        "Dashboard endpoint operational",
        False
    )


# ============================================================
# 7. DEVICE DETAIL
# ============================================================

print()
print("=" * 70)
print("7. DEVICE DETAIL ENDPOINT")
print("=" * 70)

if device_count > 0:

    try:

        response = requests.get(
            f"{BASE_URL}/device/0",
            timeout=10
        )

        print(
            "   HTTP Status:",
            response.status_code
        )

        if response.status_code == 200:

            data = response.json()
            device = data.get("device", {})

            print(
                "   Hostname:",
                device.get("hostname")
            )

            print(
                "   Risk:",
                device.get("risk")
            )

        check(
            "Device detail endpoint operational",
            response.status_code == 200
        )

    except Exception as error:

        print(
            "   Device detail error:",
            error
        )

        check(
            "Device detail endpoint operational",
            False
        )

else:

    print("   No devices available for detail test.")

    check(
        "Device detail endpoint operational",
        False
    )


# ============================================================
# 8. IMPACT ENDPOINT
# ============================================================

print()
print("=" * 70)
print("8. IMPACT ENDPOINT")
print("=" * 70)

if device_count > 0:

    try:

        response = requests.get(
            f"{BASE_URL}/device/0/impact",
            timeout=10
        )

        print(
            "   HTTP Status:",
            response.status_code
        )

        if response.status_code == 200:

            data = response.json()

            print(
                "   Security Impacts:",
                data.get("security_impacts")
            )

        check(
            "Impact endpoint operational",
            response.status_code == 200
        )

    except Exception as error:

        print(
            "   Impact endpoint error:",
            error
        )

        check(
            "Impact endpoint operational",
            False
        )

else:

    check(
        "Impact endpoint operational",
        False
    )


# ============================================================
# 9. DECISION ENDPOINT
# ============================================================

print()
print("=" * 70)
print("9. DECISION ENDPOINT")
print("=" * 70)

if device_count > 0:

    try:

        response = requests.get(
            f"{BASE_URL}/device/0/decision",
            timeout=10
        )

        print(
            "   HTTP Status:",
            response.status_code
        )

        if response.status_code == 200:

            data = response.json()
            decision = data.get(
                "decision",
                {}
            )

            print(
                "   Risk:",
                decision.get("risk_level")
            )

            print(
                "   Priority:",
                decision.get("priority")
            )

            print(
                "   Decision:",
                decision.get("primary_decision")
            )

        check(
            "Decision endpoint operational",
            response.status_code == 200
        )

    except Exception as error:

        print(
            "   Decision endpoint error:",
            error
        )

        check(
            "Decision endpoint operational",
            False
        )

else:

    check(
        "Decision endpoint operational",
        False
    )


# ============================================================
# 10. FINAL SMOKE TEST
# ============================================================

print()
print("=" * 70)
print("MODULE 28 FINAL RESULT")
print("=" * 70)

print(f"Tests Passed : {passed}")
print(f"Tests Failed : {failed}")
print(f"Total Tests  : {passed + failed}")

print()

if failed == 0:

    print(
        "MODULE 28 DEPLOYMENT SMOKE TEST: PASSED"
    )

    print()
    print(
        "Server -> API -> Scan -> Devices -> Dashboard"
    )

    print(
        "Device -> Impact -> Decision"
    )

else:

    print(
        "MODULE 28 DEPLOYMENT SMOKE TEST: FAILED"
    )

print("=" * 70)