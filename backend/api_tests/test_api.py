# ============================================================
# SHADOW IT AI
# MODULE 19 - API END-TO-END VALIDATION
# ============================================================

import json
import sys
from pathlib import Path
from urllib.request import (
    Request,
    urlopen
)
from urllib.error import HTTPError


# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

API_BASE_URL = "http://127.0.0.1:8000"


# ============================================================
# DISPLAY
# ============================================================

def print_section(title):

    print()
    print("=" * 70)
    print(title)
    print("=" * 70)


# ============================================================
# HTTP REQUEST
# ============================================================

def request_api(
    method,
    endpoint,
    data=None
):

    url = (
        API_BASE_URL
        + endpoint
    )

    headers = {
        "Accept": "application/json"
    }

    body = None

    if data is not None:

        headers[
            "Content-Type"
        ] = "application/json"

        body = json.dumps(
            data
        ).encode("utf-8")

    request = Request(
        url,
        data=body,
        headers=headers,
        method=method
    )

    try:

        with urlopen(
            request,
            timeout=60
        ) as response:

            status_code = (
                response.status
            )

            response_body = (
                response.read()
                .decode("utf-8")
            )

            if response_body:

                result = json.loads(
                    response_body
                )

            else:

                result = {}

            return (
                status_code,
                result
            )

    except HTTPError as error:

        error_body = (
            error.read()
            .decode("utf-8")
        )

        try:

            error_data = json.loads(
                error_body
            )

        except Exception:

            error_data = {
                "detail": error_body
            }

        raise RuntimeError(
            f"HTTP {error.code}: "
            f"{error_data}"
        )


# ============================================================
# 1. API STATUS
# ============================================================

def test_api_status():

    print_section(
        "1. API STATUS"
    )

    status_code, result = request_api(
        "GET",
        "/api/status"
    )

    print(
        f"HTTP Status: {status_code}"
    )

    print(
        f"Response: {result}"
    )

    if status_code != 200:

        raise AssertionError(
            "API status endpoint failed."
        )

    if result.get("status") != "running":

        raise AssertionError(
            "API is not reporting running status."
        )

    print(
        "API status: PASS"
    )


# ============================================================
# 2. SCAN API
# ============================================================

def test_scan():

    print_section(
        "2. SCAN API"
    )

    status_code, result = request_api(
        "POST",
        "/scan"
    )

    print(
        f"HTTP Status: {status_code}"
    )

    if status_code != 200:

        raise AssertionError(
            "Scan API failed."
        )

    if result.get("status") != "success":

        raise AssertionError(
            "Scan API did not return success."
        )

    device_count = result.get(
        "device_count",
        0
    )

    devices = result.get(
        "devices",
        []
    )

    print(
        f"Device Count: {device_count}"
    )

    if not isinstance(
        devices,
        list
    ):

        raise AssertionError(
            "Devices response is not a list."
        )

    if device_count != len(devices):

        raise AssertionError(
            "Device count does not match device list."
        )

    for device in devices:

        print(
            f"   {device.get('hostname', '')}"
            f" -> "
            f"{device.get('risk', '')}"
        )

    print(
        "Scan API: PASS"
    )

    return devices


# ============================================================
# 3. DEVICES API
# ============================================================

def test_devices():

    print_section(
        "3. DEVICES API"
    )

    status_code, result = request_api(
        "GET",
        "/devices"
    )

    print(
        f"HTTP Status: {status_code}"
    )

    if status_code != 200:

        raise AssertionError(
            "Devices API failed."
        )

    if result.get("status") != "success":

        raise AssertionError(
            "Devices API did not return success."
        )

    devices = result.get(
        "devices",
        []
    )

    device_count = result.get(
        "device_count",
        0
    )

    print(
        f"Stored Devices: {device_count}"
    )

    if device_count != len(devices):

        raise AssertionError(
            "Stored device count mismatch."
        )

    print(
        "Devices API: PASS"
    )

    return devices


# ============================================================
# 4. DASHBOARD API
# ============================================================

def test_dashboard():

    print_section(
        "4. DASHBOARD API"
    )

    status_code, result = request_api(
        "GET",
        "/dashboard"
    )

    print(
        f"HTTP Status: {status_code}"
    )

    if status_code != 200:

        raise AssertionError(
            "Dashboard API failed."
        )

    if result.get("status") != "success":

        raise AssertionError(
            "Dashboard API did not return success."
        )

    required_fields = [
        "total_devices",
        "shadow_it_devices",
        "authorized_devices",
        "risk_distribution"
    ]

    for field in required_fields:

        if field not in result:

            raise AssertionError(
                f"Dashboard field missing: {field}"
            )

    print(
        f"Total Devices       : "
        f"{result['total_devices']}"
    )

    print(
        f"Shadow IT Devices   : "
        f"{result['shadow_it_devices']}"
    )

    print(
        f"Authorized Devices  : "
        f"{result['authorized_devices']}"
    )

    print(
        f"Risk Distribution   : "
        f"{result['risk_distribution']}"
    )

    print(
        "Dashboard API: PASS"
    )


# ============================================================
# 5. DEVICE DETAIL API
# ============================================================

def test_device_detail():

    print_section(
        "5. DEVICE DETAIL API"
    )

    status_code, result = request_api(
        "GET",
        "/device/0"
    )

    print(
        f"HTTP Status: {status_code}"
    )

    if status_code != 200:

        raise AssertionError(
            "Device detail API failed."
        )

    if result.get("status") != "success":

        raise AssertionError(
            "Device detail API did not return success."
        )

    device = result.get(
        "device"
    )

    if not isinstance(
        device,
        dict
    ):

        raise AssertionError(
            "Device detail is not an object."
        )

    print(
        f"Hostname : "
        f"{device.get('hostname', '')}"
    )

    print(
        f"Risk     : "
        f"{device.get('risk', '')}"
    )

    print(
        "Device detail API: PASS"
    )


# ============================================================
# 6. IMPACT API
# ============================================================

def test_device_impact():

    print_section(
        "6. DEVICE IMPACT API"
    )

    status_code, result = request_api(
        "GET",
        "/device/0/impact"
    )

    print(
        f"HTTP Status: {status_code}"
    )

    if status_code != 200:

        raise AssertionError(
            "Device impact API failed."
        )

    if result.get("status") != "success":

        raise AssertionError(
            "Device impact API did not return success."
        )

    impacts = result.get(
        "security_impacts",
        []
    )

    if not isinstance(
        impacts,
        list
    ):

        raise AssertionError(
            "Security impacts are not a list."
        )

    print(
        f"Security Impacts: {impacts}"
    )

    print(
        "Device impact API: PASS"
    )


# ============================================================
# 7. DECISION API
# ============================================================

def test_device_decision():

    print_section(
        "7. DEVICE DECISION API"
    )

    status_code, result = request_api(
        "GET",
        "/device/0/decision"
    )

    print(
        f"HTTP Status: {status_code}"
    )

    if status_code != 200:

        raise AssertionError(
            "Device decision API failed."
        )

    if result.get("status") != "success":

        raise AssertionError(
            "Device decision API did not return success."
        )

    decision = result.get(
        "decision",
        {}
    )

    if not isinstance(
        decision,
        dict
    ):

        raise AssertionError(
            "Decision response is not an object."
        )

    required_fields = [
        "risk_level",
        "priority",
        "primary_decision",
        "severity_score",
        "recommendations"
    ]

    for field in required_fields:

        if field not in decision:

            raise AssertionError(
                f"Decision field missing: {field}"
            )

    print(
        f"Risk       : "
        f"{decision['risk_level']}"
    )

    print(
        f"Priority   : "
        f"{decision['priority']}"
    )

    print(
        f"Decision   : "
        f"{decision['primary_decision']}"
    )

    print(
        f"Severity   : "
        f"{decision['severity_score']}/100"
    )

    print(
        "Device decision API: PASS"
    )


# ============================================================
# 8. MANUAL ANALYZE API
# ============================================================

def test_analyze():

    print_section(
        "8. MANUAL ANALYZE API"
    )

    test_device = {

        "hostname": "test-device",

        "status": "Shadow IT",

        "os": "Windows 11",

        "ports": [
            80,
            443
        ]

    }

    status_code, result = request_api(
        "POST",
        "/analyze",
        test_device
    )

    print(
        f"HTTP Status: {status_code}"
    )

    if status_code != 200:

        raise AssertionError(
            "Analyze API failed."
        )

    if result.get("status") != "success":

        raise AssertionError(
            "Analyze API did not return success."
        )

    required_fields = [
        "features",
        "prediction",
        "security_impacts",
        "decision"
    ]

    for field in required_fields:

        if field not in result:

            raise AssertionError(
                f"Analyze response missing: {field}"
            )

    print(
        f"Features   : "
        f"{result['features']}"
    )

    print(
        f"Risk       : "
        f"{result['prediction']['risk']}"
    )

    print(
        f"Confidence : "
        f"{result['prediction']['confidence']:.2f}%"
    )

    print(
        f"Impacts    : "
        f"{result['security_impacts']}"
    )

    print(
        f"Decision   : "
        f"{result['decision']['primary_decision']}"
    )

    print(
        "Analyze API: PASS"
    )


# ============================================================
# FINAL RESULT
# ============================================================

def main():

    print()
    print("#" * 70)
    print("# SHADOW IT AI")
    print("# MODULE 19 - API END-TO-END VALIDATION")
    print("#" * 70)

    try:

        # ----------------------------------------------------
        # 1. API STATUS
        # ----------------------------------------------------

        test_api_status()

        # ----------------------------------------------------
        # 2. SCAN
        # ----------------------------------------------------

        test_scan()

        # ----------------------------------------------------
        # 3. DEVICES
        # ----------------------------------------------------

        test_devices()

        # ----------------------------------------------------
        # 4. DASHBOARD
        # ----------------------------------------------------

        test_dashboard()

        # ----------------------------------------------------
        # 5. DEVICE
        # ----------------------------------------------------

        test_device_detail()

        # ----------------------------------------------------
        # 6. IMPACT
        # ----------------------------------------------------

        test_device_impact()

        # ----------------------------------------------------
        # 7. DECISION
        # ----------------------------------------------------

        test_device_decision()

        # ----------------------------------------------------
        # 8. ANALYZE
        # ----------------------------------------------------

        test_analyze()

        # ----------------------------------------------------
        # SUCCESS
        # ----------------------------------------------------

        print()
        print("#" * 70)
        print(
            "# MODULE 19 API VALIDATION PASSED"
        )
        print("#" * 70)

        print()
        print(
            "FastAPI -> Scan -> AI -> Impact -> Decision -> API"
        )

        print()

        return True

    except Exception as error:

        print()
        print("=" * 70)

        print(
            "MODULE 19 API VALIDATION FAILED"
        )

        print(
            f"Error: {error}"
        )

        print("=" * 70)

        return False


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":

    success = main()

    if not success:

        raise SystemExit(1)