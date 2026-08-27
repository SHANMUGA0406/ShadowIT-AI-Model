# ============================================================
# SHADOW IT AI
# MODULE 27 - PRODUCTION SERVER STARTUP & DEPLOYMENT VALIDATION
# ============================================================

import sys
import time
import subprocess
from pathlib import Path

import requests


# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

HOST = "127.0.0.1"
PORT = 8001

BASE_URL = f"http://{HOST}:{PORT}"


# ============================================================
# HELPER
# ============================================================

def print_section(title):

    print()
    print("=" * 70)
    print(title)
    print("=" * 70)


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print("#" * 70)
    print("# SHADOW IT AI")
    print("# MODULE 27 - PRODUCTION SERVER STARTUP & DEPLOYMENT VALIDATION")
    print("#" * 70)

    passed = 0
    failed = 0

    server_process = None

    try:

        # ====================================================
        # 1. PROJECT DIRECTORY
        # ====================================================

        print_section(
            "1. PROJECT DIRECTORY VALIDATION"
        )

        print(
            f"Backend Directory: {BASE_DIR}"
        )

        if BASE_DIR.exists():

            print(
                "Project directory: PASS"
            )

            passed += 1

        else:

            print(
                "Project directory: FAIL"
            )

            failed += 1

            return False

        # ====================================================
        # 2. FASTAPI APPLICATION
        # ====================================================

        print_section(
            "2. FASTAPI APPLICATION VALIDATION"
        )

        app_file = BASE_DIR / "app.py"

        if app_file.exists():

            print(
                f"Application: {app_file}"
            )

            print(
                "FastAPI application: PASS"
            )

            passed += 1

        else:

            print(
                "app.py not found."
            )

            print(
                "FastAPI application: FAIL"
            )

            failed += 1

            return False

        # ====================================================
        # 3. PRODUCTION SERVER STARTUP
        # ====================================================

        print_section(
            "3. PRODUCTION SERVER STARTUP"
        )

        command = [

            sys.executable,

            "-m",
            "uvicorn",

            "app:app",

            "--host",
            HOST,

            "--port",
            str(PORT)
        ]

        print(
            "Starting production server..."
        )

        print(
            f"Server URL: {BASE_URL}"
        )

        server_process = subprocess.Popen(

            command,

            cwd=str(BASE_DIR),

            stdout=subprocess.PIPE,

            stderr=subprocess.STDOUT,

            text=True,

            encoding="utf-8",

            errors="replace"
        )

        # ----------------------------------------------------
        # Wait for server
        # ----------------------------------------------------

        server_ready = False

        for _ in range(10):

            time.sleep(1)

            if server_process.poll() is not None:

                print()
                print(
                    "SERVER STARTUP ERROR:"
                )

                output = server_process.stdout.read()

                if output:

                    print(output)

                print(
                    "Production server startup: FAIL"
                )

                failed += 1

                return False

            try:

                response = requests.get(

                    f"{BASE_URL}/api/status",

                    timeout=2
                )

                if response.status_code == 200:

                    server_ready = True

                    break

            except requests.RequestException:

                continue

        if server_ready:

            print(
                "Production server started successfully."
            )

            print(
                "Production server startup: PASS"
            )

            passed += 1

        else:

            print(
                "Server did not become ready."
            )

            print(
                "Production server startup: FAIL"
            )

            failed += 1

            return False

        # ====================================================
        # 4. API STATUS
        # ====================================================

        print_section(
            "4. PRODUCTION API STATUS"
        )

        response = requests.get(

            f"{BASE_URL}/api/status",

            timeout=10
        )

        data = response.json()

        print(
            f"HTTP Status: {response.status_code}"
        )

        print(
            f"Status : {data.get('status')}"
        )

        print(
            f"Service: {data.get('service')}"
        )

        if response.status_code == 200:

            print(
                "Production API status: PASS"
            )

            passed += 1

        else:

            print(
                "Production API status: FAIL"
            )

            failed += 1

        # ====================================================
        # 5. DEVICES
        # ====================================================

        print_section(
            "5. DEVICES ENDPOINT"
        )

        response = requests.get(

            f"{BASE_URL}/devices",

            timeout=10
        )

        data = response.json()

        print(
            f"HTTP Status: {response.status_code}"
        )

        print(
            f"Device Count: "
            f"{data.get('device_count')}"
        )

        if response.status_code == 200:

            print(
                "Devices endpoint: PASS"
            )

            passed += 1

        else:

            print(
                "Devices endpoint: FAIL"
            )

            failed += 1

        # ====================================================
        # 6. DASHBOARD
        # ====================================================

        print_section(
            "6. DASHBOARD ENDPOINT"
        )

        response = requests.get(

            f"{BASE_URL}/dashboard",

            timeout=10
        )

        data = response.json()

        print(
            f"HTTP Status: {response.status_code}"
        )

        print(
            f"Total Devices: "
            f"{data.get('total_devices')}"
        )

        print(
            f"Risk Distribution: "
            f"{data.get('risk_distribution')}"
        )

        if response.status_code == 200:

            print(
                "Dashboard endpoint: PASS"
            )

            passed += 1

        else:

            print(
                "Dashboard endpoint: FAIL"
            )

            failed += 1

        # ====================================================
        # 7. SCAN
        # ====================================================

        print_section(
            "7. PRODUCTION SCAN ENDPOINT"
        )

        print(
            "Running network scan..."
        )

        start_time = time.perf_counter()

        response = requests.post(

            f"{BASE_URL}/scan",

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

        if response.status_code == 200:

            data = response.json()

            print(
                f"Device Count: "
                f"{data.get('device_count')}"
            )

            for device in data.get(
                "devices",
                []
            ):

                print(
                    f"   {device.get('hostname')} "
                    f"-> "
                    f"{device.get('risk')}"
                )

            print(
                "Production scan endpoint: PASS"
            )

            passed += 1

        else:

            print(
                "Production scan endpoint: FAIL"
            )

            print(
                response.text
            )

            failed += 1

        # ====================================================
        # 8. DEVICE DETAIL
        # ====================================================

        print_section(
            "8. DEVICE DETAIL ENDPOINT"
        )

        response = requests.get(

            f"{BASE_URL}/device/0",

            timeout=10
        )

        print(
            f"HTTP Status: {response.status_code}"
        )

        if response.status_code == 200:

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

            print(
                "Device detail endpoint: PASS"
            )

            passed += 1

        else:

            print(
                "Device detail endpoint: FAIL"
            )

            failed += 1

        # ====================================================
        # 9. DECISION
        # ====================================================

        print_section(
            "9. DECISION ENDPOINT"
        )

        response = requests.get(

            f"{BASE_URL}/device/0/decision",

            timeout=10
        )

        print(
            f"HTTP Status: {response.status_code}"
        )

        if response.status_code == 200:

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

            print(
                "Decision endpoint: PASS"
            )

            passed += 1

        else:

            print(
                "Decision endpoint: FAIL"
            )

            failed += 1

        # ====================================================
        # 10. FINAL RESULT
        # ====================================================

        print_section(
            "10. FINAL DEPLOYMENT VALIDATION"
        )

        print(
            f"Tests Passed : {passed}"
        )

        print(
            f"Tests Failed : {failed}"
        )

        print(
            f"Total Tests  : {passed + failed}"
        )

        if failed == 0:

            print()
            print(
                "MODULE 27 PRODUCTION SERVER TEST: PASSED"
            )

            print()
            print(
                "Production Configuration -> "
                "FastAPI Startup -> "
                "API Status -> "
                "Scan -> "
                "Devices -> "
                "Dashboard -> "
                "Decision"
            )

            print()
            print(
                "PRODUCTION SERVER VALIDATION COMPLETED"
            )

            return True

        print()
        print(
            "MODULE 27 PRODUCTION SERVER TEST: FAILED"
        )

        return False

    except Exception as error:

        print()
        print(
            f"UNEXPECTED ERROR: {error}"
        )

        print()
        print(
            "MODULE 27 PRODUCTION SERVER TEST: FAILED"
        )

        return False

    finally:

        # ====================================================
        # STOP TEST SERVER
        # ====================================================

        if server_process is not None:

            print()
            print(
                "Stopping test production server..."
            )

            try:

                server_process.terminate()

                server_process.wait(
                    timeout=5
                )

            except subprocess.TimeoutExpired:

                server_process.kill()

                server_process.wait()

            print(
                "Test production server stopped."
            )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    success = main()

    raise SystemExit(
        0 if success else 1
    )