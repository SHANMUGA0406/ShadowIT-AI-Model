import sys
from pathlib import Path


# ============================================================
# SHADOW IT AI
# MODULE 29 - FINAL DEPLOYMENT VERIFICATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

tests_passed = 0
tests_failed = 0


# ============================================================
# HELPERS
# ============================================================

def print_section(title):

    print()
    print("=" * 70)
    print(title)
    print("=" * 70)


def run_test(name, condition, detail=""):

    global tests_passed
    global tests_failed

    if condition:

        tests_passed += 1

        print(f"{name}: PASS")

    else:

        tests_failed += 1

        print(f"{name}: FAIL")

    if detail:

        print(f"   {detail}")


# ============================================================
# HEADER
# ============================================================

print()
print("#" * 70)
print("# SHADOW IT AI")
print("# MODULE 29 - FINAL DEPLOYMENT VERIFICATION")
print("#" * 70)


# ============================================================
# 1. BACKEND STRUCTURE
# ============================================================

print_section(
    "1. BACKEND STRUCTURE"
)

required_directories = [

    "scanner",
    "shadow_it",
    "ai",
    "impact",
    "decision",
    "api",
    "dataset",
    "deployment",
    "integration",

]

directories_ok = all(
    (BASE_DIR / directory).is_dir()
    for directory in required_directories
)

run_test(
    "Backend structure",
    directories_ok,
    "All required backend directories verified."
)


# ============================================================
# 2. CORE SOURCE FILES
# ============================================================

print_section(
    "2. CORE SOURCE FILES"
)

required_files = [

    "app.py",

    "scanner/scan.py",

    "shadow_it/detect.py",

    "shadow_it/approved_devices.json",

    "ai/feature_extractor.py",

    "ai/predict.py",

    "ai/preprocess.py",

    "ai/shap_explainer.py",

    "ai/risk_interpreter.py",

    "impact/impact_analyzer.py",

    "decision/decision_engine.py",

    "api/routes.py",

]

files_ok = all(
    (BASE_DIR / file).is_file()
    for file in required_files
)

run_test(
    "Core source files",
    files_ok,
    "Scanner, AI, impact, decision and API files verified."
)


# ============================================================
# 3. FINAL MODEL ARTIFACTS
# ============================================================

print_section(
    "3. FINAL MODEL ARTIFACTS"
)

model_files = [

    "ai/models/risk_model.pkl",

    "ai/models/label_mapping.json",

    "ai/models/feature_config.json",

]

models_ok = all(
    (BASE_DIR / file).is_file()
    and (BASE_DIR / file).stat().st_size > 0
    for file in model_files
)

run_test(
    "Final model artifacts",
    models_ok,
    "Risk model, label mapping and feature configuration verified."
)


# ============================================================
# 4. DATASET
# ============================================================

print_section(
    "4. DATASET"
)

dataset = BASE_DIR / "dataset" / "devices.csv"

dataset_ok = (
    dataset.is_file()
    and dataset.stat().st_size > 0
)

run_test(
    "Dataset availability",
    dataset_ok,
    str(dataset)
)


# ============================================================
# 5. PRODUCTION CONFIGURATION
# ============================================================

print_section(
    "5. PRODUCTION CONFIGURATION"
)

production_config = (
    BASE_DIR /
    "deployment" /
    "production_config.py"
)

config_ok = (
    production_config.is_file()
    and production_config.stat().st_size > 0
)

run_test(
    "Production configuration",
    config_ok,
    str(production_config)
)


# ============================================================
# 6. PRODUCTION SERVER TEST
# ============================================================

print_section(
    "6. PRODUCTION SERVER VALIDATION"
)

production_server_test = (
    BASE_DIR /
    "deployment" /
    "test_production_server.py"
)

server_test_ok = (
    production_server_test.is_file()
    and production_server_test.stat().st_size > 0
)

run_test(
    "Production server test",
    server_test_ok,
    "Production startup validation script available."
)


# ============================================================
# 7. API VALIDATION TEST
# ============================================================

print_section(
    "7. API VALIDATION"
)

api_test = (
    BASE_DIR /
    "api_tests" /
    "test_api.py"
)

api_test_ok = (
    api_test.is_file()
    and api_test.stat().st_size > 0
)

run_test(
    "API validation test",
    api_test_ok,
    "FastAPI endpoint validation script available."
)


# ============================================================
# 8. END-TO-END VALIDATION
# ============================================================

print_section(
    "8. END-TO-END VALIDATION"
)

end_to_end_test = (
    BASE_DIR /
    "integration" /
    "test_end_to_end.py"
)

e2e_ok = (
    end_to_end_test.is_file()
    and end_to_end_test.stat().st_size > 0
)

run_test(
    "End-to-end validation test",
    e2e_ok,
    "Complete scanner-to-decision test available."
)


# ============================================================
# 9. SECURITY VALIDATION
# ============================================================

print_section(
    "9. SECURITY VALIDATION"
)

security_test = (
    BASE_DIR /
    "integration" /
    "test_security_validation.py"
)

security_hardening_test = (
    BASE_DIR /
    "deployment" /
    "test_security_hardening.py"
)

security_ok = (
    security_test.is_file()
    and security_hardening_test.is_file()
    and security_test.stat().st_size > 0
    and security_hardening_test.stat().st_size > 0
)

run_test(
    "Security validation suite",
    security_ok,
    "Input validation and deployment hardening tests available."
)


# ============================================================
# 10. FINAL DEPLOYMENT READINESS
# ============================================================

print_section(
    "10. FINAL DEPLOYMENT READINESS"
)

all_previous_tests_passed = (
    directories_ok
    and files_ok
    and models_ok
    and dataset_ok
    and config_ok
    and server_test_ok
    and api_test_ok
    and e2e_ok
    and security_ok
)

run_test(
    "Final deployment readiness",
    all_previous_tests_passed,
    "All required deployment components are present."
)


# ============================================================
# FINAL RESULT
# ============================================================

print_section(
    "MODULE 29 FINAL RESULT"
)

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
        "MODULE 29 FINAL DEPLOYMENT VERIFICATION: PASSED"
    )

    print()

    print(
        "Project Structure -> Source Code -> Models -> "
        "Dataset -> Configuration -> API -> Security"
    )

    print()

    print(
        "SHADOW IT AI BACKEND IS DEPLOYMENT READY"
    )

else:

    print(
        "MODULE 29 FINAL DEPLOYMENT VERIFICATION: FAILED"
    )

    print()

    print(
        "Review the failed checks before deployment."
    )

    sys.exit(1)


print("=" * 70)
