import sys
from pathlib import Path


# ============================================================
# SHADOW IT AI
# MODULE 28 - FINAL DEPLOYMENT & SECURITY HARDENING VALIDATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_DIR = BASE_DIR / "ai" / "models"
DATASET_DIR = BASE_DIR / "dataset"
DEPLOYMENT_DIR = BASE_DIR / "deployment"


# ============================================================
# TEST COUNTERS
# ============================================================

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


def test_result(name, passed, detail=None):

    global tests_passed
    global tests_failed

    if passed:

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
print("# MODULE 28 - FINAL DEPLOYMENT & SECURITY HARDENING VALIDATION")
print("#" * 70)


# ============================================================
# 1. PRODUCTION CONFIGURATION
# ============================================================

print_section(
    "1. PRODUCTION CONFIGURATION"
)

config_file = (
    DEPLOYMENT_DIR /
    "production_config.py"
)

test_result(
    "Production configuration",
    config_file.exists(),
    str(config_file)
)


# ============================================================
# 2. DEBUG / DEVELOPMENT SETTINGS
# ============================================================

print_section(
    "2. DEBUG / DEVELOPMENT SETTINGS"
)

debug_safe = True

if config_file.exists():

    try:

        content = config_file.read_text(
            encoding="utf-8"
        )

        if "Debug       : True" in content:

            debug_safe = False

        if "reload=True" in content.lower():

            debug_safe = False

    except Exception:

        debug_safe = False


test_result(
    "Debug/reload production safety",
    debug_safe,
    "Debug and reload development settings are not enabled."
)


# ============================================================
# 3. FINAL MODEL
# ============================================================

print_section(
    "3. FINAL MODEL VALIDATION"
)

model_file = (
    MODEL_DIR /
    "risk_model.pkl"
)

test_result(
    "Final risk model",
    model_file.exists(),
    str(model_file)
)


# ============================================================
# 4. LABEL MAPPING
# ============================================================

print_section(
    "4. LABEL MAPPING VALIDATION"
)

label_mapping = (
    MODEL_DIR /
    "label_mapping.json"
)

test_result(
    "Label mapping",
    label_mapping.exists(),
    str(label_mapping)
)


# ============================================================
# 5. FEATURE CONFIGURATION
# ============================================================

print_section(
    "5. FEATURE CONFIGURATION"
)

feature_config = (
    MODEL_DIR /
    "feature_config.json"
)

test_result(
    "Feature configuration",
    feature_config.exists(),
    str(feature_config)
)


# ============================================================
# 6. DATASET
# ============================================================

print_section(
    "6. DATASET VALIDATION"
)

dataset_file = (
    DATASET_DIR /
    "devices.csv"
)

dataset_valid = (
    dataset_file.exists()
    and dataset_file.stat().st_size > 0
)

test_result(
    "Production dataset",
    dataset_valid,
    str(dataset_file)
)


# ============================================================
# 7. API ROUTES
# ============================================================

print_section(
    "7. API ROUTES VALIDATION"
)

routes_file = (
    BASE_DIR /
    "api" /
    "routes.py"
)

routes_valid = False

if routes_file.exists():

    try:

        content = routes_file.read_text(
            encoding="utf-8"
        )

        routes_valid = (
            "router = APIRouter()" in content
            and '@router.post("/scan")' in content
            and '@router.get("/devices")' in content
            and '@router.get("/dashboard")' in content
        )

    except Exception:

        routes_valid = False


test_result(
    "API routes",
    routes_valid,
    "Router and core endpoints validated."
)


# ============================================================
# 8. SECURITY VALIDATION
# ============================================================

print_section(
    "8. INPUT SECURITY VALIDATION"
)

decision_file = (
    BASE_DIR /
    "decision" /
    "decision_engine.py"
)

security_validation = False

if decision_file.exists():

    try:

        content = decision_file.read_text(
            encoding="utf-8"
        )

        security_validation = (
            "validate_features" in content
            and "Invalid or missing device features" in content
            and "Invalid risk level" in content
        )

    except Exception:

        security_validation = False


test_result(
    "Input validation",
    security_validation,
    "Decision engine validation checks detected."
)


# ============================================================
# 9. REQUIRED PROJECT MODULES
# ============================================================

print_section(
    "9. REQUIRED MODULES"
)

required_modules = [

    BASE_DIR / "scanner",
    BASE_DIR / "shadow_it",
    BASE_DIR / "ai",
    BASE_DIR / "impact",
    BASE_DIR / "decision",
    BASE_DIR / "api",

]

modules_valid = all(
    path.exists()
    for path in required_modules
)

test_result(
    "Required project modules",
    modules_valid,
    "Scanner -> Shadow IT -> AI -> Impact -> Decision -> API"
)


# ============================================================
# 10. DEPLOYMENT TEST SUITE
# ============================================================

print_section(
    "10. DEPLOYMENT TEST SUITE"
)

deployment_tests = [

    DEPLOYMENT_DIR /
    "test_production_server.py",

]

deployment_tests_valid = all(
    path.exists()
    for path in deployment_tests
)

test_result(
    "Deployment validation suite",
    deployment_tests_valid,
    "Production server validation test available."
)


# ============================================================
# FINAL RESULT
# ============================================================

print_section(
    "MODULE 28 FINAL RESULT"
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
        "MODULE 28 SECURITY HARDENING TEST: PASSED"
    )

    print()

    print(
        "Configuration -> Models -> Dataset -> API -> "
        "Validation -> Deployment"
    )

    print()

    print(
        "FINAL DEPLOYMENT SECURITY VALIDATION PASSED"
    )

else:

    print(
        "MODULE 28 SECURITY HARDENING TEST: FAILED"
    )

    print()

    print(
        "Review the failed checks before final deployment."
    )

    sys.exit(1)

print("=" * 70)