# ============================================================
# SHADOW IT AI
# MODULE 24 - PRODUCTION READINESS TEST
# ============================================================

import sys
from pathlib import Path


# ============================================================
# PROJECT PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))


# ============================================================
# HEADER
# ============================================================

print()
print("#" * 70)
print("# SHADOW IT AI")
print("# MODULE 24 - PRODUCTION READINESS TEST")
print("#" * 70)


# ============================================================
# COUNTERS
# ============================================================

tests_passed = 0
tests_failed = 0


# ============================================================
# HELPER
# ============================================================

def record_test(name, passed):

    global tests_passed
    global tests_failed

    if passed:

        print(f"{name}: PASS")
        tests_passed += 1

    else:

        print(f"{name}: FAIL")
        tests_failed += 1


# ============================================================
# 1. REQUIRED DIRECTORIES
# ============================================================

print()
print("=" * 70)
print("1. REQUIRED DIRECTORIES")
print("=" * 70)

required_directories = [

    "scanner",
    "shadow_it",
    "ai",
    "impact",
    "decision",
    "api",
    "integration",
]

directories_ok = True

for directory in required_directories:

    path = BASE_DIR / directory

    if path.exists() and path.is_dir():

        print(
            f"   {directory:<20} : EXISTS"
        )

    else:

        print(
            f"   {directory:<20} : MISSING"
        )

        directories_ok = False


record_test(
    "Required directories",
    directories_ok
)


# ============================================================
# 2. REQUIRED SOURCE FILES
# ============================================================

print()
print("=" * 70)
print("2. REQUIRED SOURCE FILES")
print("=" * 70)

required_files = [

    "scanner/scan.py",

    "shadow_it/detect.py",

    "shadow_it/approved_devices.json",

    "ai/feature_extractor.py",

    "ai/predict.py",

    "ai/preprocess.py",

    "ai/split_data.py",

    "ai/select_model.py",

    "ai/shap_explainer.py",

    "ai/risk_interpreter.py",

    "impact/impact_analyzer.py",

    "decision/decision_engine.py",

    "api/routes.py",
]

files_ok = True

for relative_path in required_files:

    path = BASE_DIR / relative_path

    if path.exists() and path.is_file():

        print(
            f"   {relative_path:<40} : EXISTS"
        )

    else:

        print(
            f"   {relative_path:<40} : MISSING"
        )

        files_ok = False


record_test(
    "Required source files",
    files_ok
)


# ============================================================
# 3. FINAL MODEL FILES
# ============================================================

print()
print("=" * 70)
print("3. FINAL MODEL FILES")
print("=" * 70)

model_files = [

    "ai/models/risk_model.pkl",

    "ai/models/label_mapping.json",

    "ai/models/feature_config.json",
]

model_files_ok = True

for relative_path in model_files:

    path = BASE_DIR / relative_path

    if path.exists() and path.is_file():

        size = path.stat().st_size

        print(
            f"   {relative_path:<40} : "
            f"EXISTS ({size} bytes)"
        )

        if size == 0:

            model_files_ok = False

    else:

        print(
            f"   {relative_path:<40} : MISSING"
        )

        model_files_ok = False


record_test(
    "Final model files",
    model_files_ok
)


# ============================================================
# 4. DATASET
# ============================================================

print()
print("=" * 70)
print("4. DATASET")
print("=" * 70)

dataset_path = BASE_DIR / "dataset" / "devices.csv"

if dataset_path.exists():

    print(
        f"   Dataset found: "
        f"{dataset_path}"
    )

    print(
        f"   Dataset size : "
        f"{dataset_path.stat().st_size} bytes"
    )

    record_test(
        "Dataset availability",
        dataset_path.stat().st_size > 0
    )

else:

    print(
        "   Dataset not found."
    )

    record_test(
        "Dataset availability",
        False
    )


# ============================================================
# 5. PYTHON IMPORT VALIDATION
# ============================================================

print()
print("=" * 70)
print("5. PYTHON MODULE IMPORT VALIDATION")
print("=" * 70)

imports_ok = True

modules = [

    ("Scanner", "scanner.scan"),
    ("Shadow IT", "shadow_it.detect"),
    ("Feature Extractor", "ai.feature_extractor"),
    ("Prediction", "ai.predict"),
    ("Impact Analyzer", "impact.impact_analyzer"),
    ("Decision Engine", "decision.decision_engine"),
    ("API Routes", "api.routes"),
]

import importlib

for module_name, module_path in modules:

    try:

        importlib.import_module(
            module_path
        )

        print(
            f"   {module_name:<25} : IMPORT OK"
        )

    except Exception as error:

        print(
            f"   {module_name:<25} : IMPORT FAILED"
        )

        print(
            f"      {error}"
        )

        imports_ok = False


record_test(
    "Python module imports",
    imports_ok
)


# ============================================================
# 6. FEATURE CONFIGURATION
# ============================================================

print()
print("=" * 70)
print("6. FEATURE CONFIGURATION")
print("=" * 70)

feature_config_path = (
    BASE_DIR
    / "ai"
    / "models"
    / "feature_config.json"
)

expected_features = [

    "unknown_device",
    "open_port_count",
    "critical_cve_count",
    "patch_status",
    "os_outdated",
    "sensitive_network_access",
]

feature_config_ok = False

try:

    import json

    with open(
        feature_config_path,
        "r",
        encoding="utf-8"
    ) as file:

        config = json.load(file)

    if isinstance(config, dict):

        actual_features = config.get(
            "features",
            []
        )

    elif isinstance(config, list):

        actual_features = config

    else:

        actual_features = []

    print(
        "   Configured features:"
    )

    for feature in actual_features:

        print(
            f"      - {feature}"
        )

    feature_config_ok = (
        actual_features == expected_features
    )

except Exception as error:

    print(
        f"   Configuration error: {error}"
    )


record_test(
    "Feature configuration",
    feature_config_ok
)


# ============================================================
# 7. LABEL MAPPING
# ============================================================

print()
print("=" * 70)
print("7. LABEL MAPPING")
print("=" * 70)

label_mapping_path = (
    BASE_DIR
    / "ai"
    / "models"
    / "label_mapping.json"
)

expected_mapping = {

    "Low": 0,
    "Medium": 1,
    "High": 2,
    "Critical": 3,
}

label_mapping_ok = False

try:

    with open(
        label_mapping_path,
        "r",
        encoding="utf-8"
    ) as file:

        mapping = json.load(file)

    print(
        f"   Mapping: {mapping}"
    )

    label_mapping_ok = (
        mapping == expected_mapping
        or
        mapping == {
            "0": "Low",
            "1": "Medium",
            "2": "High",
            "3": "Critical",
        }
    )

except Exception as error:

    print(
        f"   Mapping error: {error}"
    )


record_test(
    "Label mapping",
    label_mapping_ok
)


# ============================================================
# 8. PREDICTION SMOKE TEST
# ============================================================

print()
print("=" * 70)
print("8. PREDICTION SMOKE TEST")
print("=" * 70)

prediction_ok = False

try:

    from ai.predict import predict_risk

    test_features = {

        "unknown_device": 1,

        "open_port_count": 8,

        "critical_cve_count": 3,

        "patch_status": 0,

        "os_outdated": 1,

        "sensitive_network_access": 1,
    }

    result = predict_risk(
        test_features
    )

    print(
        f"   Risk       : "
        f"{result['risk']}"
    )

    print(
        f"   Confidence : "
        f"{result['confidence']}%"
    )

    valid_risks = [
        "Low",
        "Medium",
        "High",
        "Critical",
    ]

    prediction_ok = (
        result["risk"] in valid_risks
        and
        isinstance(
            result["confidence"],
            (int, float)
        )
    )

except Exception as error:

    print(
        f"   Prediction error: {error}"
    )


record_test(
    "Prediction smoke test",
    prediction_ok
)


# ============================================================
# 9. DECISION ENGINE SMOKE TEST
# ============================================================

print()
print("=" * 70)
print("9. DECISION ENGINE SMOKE TEST")
print("=" * 70)

decision_ok = False

try:

    from decision.decision_engine import (
        generate_decision
    )

    decision_input = {

        "unknown_device": 1,

        "open_port_count": 8,

        "critical_cve_count": 3,

        "patch_status": 0,

        "os_outdated": 1,

        "sensitive_network_access": 1,

        "risk": "Critical",

        "confidence": 95.0,
    }

    decision = generate_decision(
        decision_input
    )

    print(
        f"   Risk     : "
        f"{decision['risk_level']}"
    )

    print(
        f"   Priority : "
        f"{decision['priority']}"
    )

    print(
        f"   Decision : "
        f"{decision['primary_decision']}"
    )

    decision_ok = (
        decision["risk_level"] == "Critical"
        and
        decision["priority"] == "IMMEDIATE"
        and
        decision["primary_decision"]
        == "ISOLATE DEVICE"
    )

except Exception as error:

    print(
        f"   Decision error: {error}"
    )


record_test(
    "Decision engine smoke test",
    decision_ok
)


# ============================================================
# 10. PROJECT STRUCTURE CHECK
# ============================================================

print()
print("=" * 70)
print("10. PROJECT STRUCTURE CHECK")
print("=" * 70)

structure_ok = True

important_directories = [

    BASE_DIR / "ai" / "models",

    BASE_DIR / "ai" / "evaluation",

    BASE_DIR / "integration",

]

for path in important_directories:

    if path.exists() and path.is_dir():

        print(
            f"   {path.relative_to(BASE_DIR)}"
            " -> OK"
        )

    else:

        print(
            f"   {path.relative_to(BASE_DIR)}"
            " -> MISSING"
        )

        structure_ok = False


record_test(
    "Project structure",
    structure_ok
)


# ============================================================
# FINAL RESULT
# ============================================================

print()
print("=" * 70)
print("MODULE 24 FINAL RESULT")
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
        "MODULE 24 PRODUCTION READINESS TEST: PASSED"
    )

    print()

    print(
        "Project Structure -> Models -> Configuration -> "
        "Imports -> Prediction -> Decision"
    )

else:

    print(
        "MODULE 24 PRODUCTION READINESS TEST: "
        "REQUIRES ATTENTION"
    )

    print()

    print(
        "Do NOT delete or replace files yet."
    )

    print(
        "Review the failed checks before making changes."
    )

print("=" * 70)


# ============================================================
# EXIT STATUS
# ============================================================

if tests_failed > 0:

    raise SystemExit(1)