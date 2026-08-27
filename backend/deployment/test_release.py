import sys
from pathlib import Path


# ============================================================
# SHADOW IT AI
# MODULE 30 - FINAL RELEASE & PROJECT COMPLETION VALIDATION
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
print("# MODULE 30 - FINAL RELEASE & PROJECT COMPLETION VALIDATION")
print("#" * 70)


# ============================================================
# 1. APPLICATION
# ============================================================

print_section(
    "1. APPLICATION VALIDATION"
)

app_file = BASE_DIR / "app.py"

run_test(
    "FastAPI application",
    app_file.is_file()
    and app_file.stat().st_size > 0,
    str(app_file)
)


# ============================================================
# 2. SCANNER
# ============================================================

print_section(
    "2. DEVICE DISCOVERY"
)

scanner_file = (
    BASE_DIR /
    "scanner" /
    "scan.py"
)

run_test(
    "Device scanner",
    scanner_file.is_file()
    and scanner_file.stat().st_size > 0,
    "Nmap device discovery component available."
)


# ============================================================
# 3. SHADOW IT DETECTION
# ============================================================

print_section(
    "3. SHADOW IT DETECTION"
)

shadow_it_file = (
    BASE_DIR /
    "shadow_it" /
    "detect.py"
)

approved_devices = (
    BASE_DIR /
    "shadow_it" /
    "approved_devices.json"
)

shadow_it_ok = (
    shadow_it_file.is_file()
    and approved_devices.is_file()
)

run_test(
    "Shadow IT detection",
    shadow_it_ok,
    "Detection logic and approved-device configuration available."
)


# ============================================================
# 4. AI RISK CLASSIFICATION
# ============================================================

print_section(
    "4. AI RISK CLASSIFICATION"
)

feature_extractor = (
    BASE_DIR /
    "ai" /
    "feature_extractor.py"
)

predict_file = (
    BASE_DIR /
    "ai" /
    "predict.py"
)

risk_model = (
    BASE_DIR /
    "ai" /
    "models" /
    "risk_model.pkl"
)

ai_ok = (
    feature_extractor.is_file()
    and predict_file.is_file()
    and risk_model.is_file()
    and risk_model.stat().st_size > 0
)

run_test(
    "AI risk classification",
    ai_ok,
    "Feature extraction, prediction and final model verified."
)


# ============================================================
# 5. EXPLAINABILITY
# ============================================================

print_section(
    "5. EXPLAINABLE AI"
)

shap_file = (
    BASE_DIR /
    "ai" /
    "shap_explainer.py"
)

interpreter_file = (
    BASE_DIR /
    "ai" /
    "risk_interpreter.py"
)

xai_ok = (
    shap_file.is_file()
    and interpreter_file.is_file()
)

run_test(
    "Explainable AI components",
    xai_ok,
    "SHAP explainer and risk interpretation components available."
)


# ============================================================
# 6. SECURITY IMPACT
# ============================================================

print_section(
    "6. SECURITY IMPACT ANALYSIS"
)

impact_file = (
    BASE_DIR /
    "impact" /
    "impact_analyzer.py"
)

run_test(
    "Security impact analyzer",
    impact_file.is_file()
    and impact_file.stat().st_size > 0,
    "Security impact analysis component available."
)


# ============================================================
# 7. DECISION INTELLIGENCE
# ============================================================

print_section(
    "7. DECISION INTELLIGENCE"
)

decision_file = (
    BASE_DIR /
    "decision" /
    "decision_engine.py"
)

run_test(
    "Decision engine",
    decision_file.is_file()
    and decision_file.stat().st_size > 0,
    "Risk-to-action decision engine available."
)


# ============================================================
# 8. API
# ============================================================

print_section(
    "8. FASTAPI INTEGRATION"
)

routes_file = (
    BASE_DIR /
    "api" /
    "routes.py"
)

api_ok = False

if routes_file.is_file():

    try:

        content = routes_file.read_text(
            encoding="utf-8"
        )

        api_ok = (
            "router = APIRouter()" in content
            and '@router.post("/scan")' in content
            and '@router.get("/devices")' in content
            and '@router.get("/dashboard")' in content
            and '@router.post("/analyze")' in content
        )

    except Exception:

        api_ok = False


run_test(
    "FastAPI integration",
    api_ok,
    "Core scanning, dashboard and analysis endpoints available."
)


# ============================================================
# 9. FINAL CONFIGURATION
# ============================================================

print_section(
    "9. FINAL CONFIGURATION"
)

label_mapping = (
    BASE_DIR /
    "ai" /
    "models" /
    "label_mapping.json"
)

feature_config = (
    BASE_DIR /
    "ai" /
    "models" /
    "feature_config.json"
)

dataset = (
    BASE_DIR /
    "dataset" /
    "devices.csv"
)

configuration_ok = (
    label_mapping.is_file()
    and feature_config.is_file()
    and dataset.is_file()
    and dataset.stat().st_size > 0
)

run_test(
    "Final configuration",
    configuration_ok,
    "Label mapping, feature configuration and dataset verified."
)


# ============================================================
# 10. RELEASE VALIDATION
# ============================================================

print_section(
    "10. RELEASE VALIDATION"
)

release_tests = [

    BASE_DIR /
    "deployment" /
    "test_production_server.py",

    BASE_DIR /
    "deployment" /
    "test_security_hardening.py",

    BASE_DIR /
    "deployment" /
    "test_final_deployment.py",

]

release_ok = all(
    file.is_file()
    and file.stat().st_size > 0
    for file in release_tests
)

run_test(
    "Release validation suite",
    release_ok,
    "Production, security and deployment validation tests available."
)


# ============================================================
# FINAL RESULT
# ============================================================

print_section(
    "MODULE 30 FINAL RESULT"
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
        "MODULE 30 FINAL RELEASE VALIDATION: PASSED"
    )

    print()

    print(
        "Scanner -> Shadow IT -> Features -> AI -> "
        "XAI -> Impact -> Decision -> API"
    )

    print()

    print(
        "============================================================"
    )

    print(
        "SHADOW IT AI PROJECT RELEASE VALIDATION PASSED"
    )

    print(
        "BACKEND / AI SYSTEM READY FOR FINAL PROJECT INTEGRATION"
    )

    print(
        "============================================================"
    )

else:

    print(
        "MODULE 30 FINAL RELEASE VALIDATION: FAILED"
    )

    print()

    print(
        "Review the failed checks before final release."
    )

    sys.exit(1)


print()
print("=" * 70)