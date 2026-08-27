# ============================================================
# SHADOW IT AI
# MODULE 29 - FINAL DEPLOYMENT VERIFICATION
# ============================================================

import os
import sys
import json
import joblib


# ============================================================
# HEADER
# ============================================================

print("\n" + "=" * 70)
print("# SHADOW IT AI")
print("# MODULE 29 - FINAL DEPLOYMENT VERIFICATION")
print("=" * 70)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

AI_DIR = os.path.join(
    BASE_DIR,
    "ai"
)

MODEL_DIR = os.path.join(
    AI_DIR,
    "models"
)

DATASET_DIR = os.path.join(
    BASE_DIR,
    "dataset"
)

DEPLOYMENT_DIR = os.path.join(
    BASE_DIR,
    "deployment"
)

API_DIR = os.path.join(
    BASE_DIR,
    "api"
)


# ============================================================
# REQUIRED FILES
# ============================================================

required_files = {

    "Risk Model":
        os.path.join(
            MODEL_DIR,
            "risk_model.pkl"
        ),

    "Label Mapping":
        os.path.join(
            MODEL_DIR,
            "label_mapping.json"
        ),

    "Feature Configuration":
        os.path.join(
            MODEL_DIR,
            "feature_config.json"
        ),

    "Dataset":
        os.path.join(
            DATASET_DIR,
            "devices.csv"
        ),

    "API Routes":
        os.path.join(
            API_DIR,
            "routes.py"
        ),

    "Production Configuration":
        os.path.join(
            DEPLOYMENT_DIR,
            "production_config.py"
        ),

    "Deployment Validation":
        os.path.join(
            DEPLOYMENT_DIR,
            "test_deployment.py"
        ),

    "Deployment Smoke Test":
        os.path.join(
            DEPLOYMENT_DIR,
            "test_smoke.py"
        )
}


# ============================================================
# TEST COUNTERS
# ============================================================

passed = 0
failed = 0


def check(name, condition):

    global passed
    global failed

    if condition:

        print(
            f"   {name:<45}: PASS"
        )

        passed += 1

    else:

        print(
            f"   {name:<45}: FAIL"
        )

        failed += 1


# ============================================================
# 1. PROJECT ROOT
# ============================================================

print("\n" + "=" * 70)
print("1. PROJECT ROOT")
print("=" * 70)

check(
    "Backend directory",
    os.path.isdir(BASE_DIR)
)


# ============================================================
# 2. REQUIRED DIRECTORIES
# ============================================================

print("\n" + "=" * 70)
print("2. REQUIRED DIRECTORIES")
print("=" * 70)

directories = {

    "AI directory":
        AI_DIR,

    "Model directory":
        MODEL_DIR,

    "Dataset directory":
        DATASET_DIR,

    "API directory":
        API_DIR,

    "Deployment directory":
        DEPLOYMENT_DIR
}

for name, path in directories.items():

    check(
        name,
        os.path.isdir(path)
    )


# ============================================================
# 3. REQUIRED FILES
# ============================================================

print("\n" + "=" * 70)
print("3. REQUIRED DEPLOYMENT FILES")
print("=" * 70)

for name, path in required_files.items():

    check(
        name,
        os.path.isfile(path)
    )


# ============================================================
# 4. MODEL LOADING
# ============================================================

print("\n" + "=" * 70)
print("4. FINAL MODEL VALIDATION")
print("=" * 70)

model_path = required_files["Risk Model"]

model = None

try:

    model = joblib.load(
        model_path
    )

    check(
        "Risk model loads successfully",
        model is not None
    )

except Exception as error:

    print(
        "   Model loading error:",
        error
    )

    check(
        "Risk model loads successfully",
        False
    )


# ============================================================
# 5. LABEL MAPPING
# ============================================================

print("\n" + "=" * 70)
print("5. LABEL MAPPING VALIDATION")
print("=" * 70)

mapping_path = required_files[
    "Label Mapping"
]

try:

    with open(
        mapping_path,
        "r",
        encoding="utf-8"
    ) as file:

        mapping = json.load(
            file
        )

    expected_mapping = {

        "Low": 0,
        "Medium": 1,
        "High": 2,
        "Critical": 3
    }

    print(
        "   Mapping:",
        mapping
    )

    check(
        "Label mapping is correct",
        mapping == expected_mapping
    )

except Exception as error:

    print(
        "   Mapping error:",
        error
    )

    check(
        "Label mapping is correct",
        False
    )


# ============================================================
# 6. FEATURE CONFIGURATION
# ============================================================

print("\n" + "=" * 70)
print("6. FEATURE CONFIGURATION")
print("=" * 70)

feature_path = required_files[
    "Feature Configuration"
]

required_features = [

    "unknown_device",
    "open_port_count",
    "critical_cve_count",
    "patch_status",
    "os_outdated",
    "sensitive_network_access"
]

try:

    with open(
        feature_path,
        "r",
        encoding="utf-8"
    ) as file:

        feature_config = json.load(
            file
        )

    print(
        "   Feature configuration loaded."
    )

    # Support either a direct list or
    # a dictionary containing features.

    if isinstance(
        feature_config,
        list
    ):

        configured_features = feature_config

    elif isinstance(
        feature_config,
        dict
    ):

        configured_features = (
            feature_config.get(
                "features",
                []
            )
        )

    else:

        configured_features = []

    check(
        "All required features configured",
        all(
            feature in configured_features
            for feature in required_features
        )
    )

except Exception as error:

    print(
        "   Feature configuration error:",
        error
    )

    check(
        "All required features configured",
        False
    )


# ============================================================
# 7. DATASET VALIDATION
# ============================================================

print("\n" + "=" * 70)
print("7. DATASET VALIDATION")
print("=" * 70)

dataset_path = required_files[
    "Dataset"
]

try:

    dataset_exists = os.path.isfile(
        dataset_path
    )

    dataset_size = (
        os.path.getsize(
            dataset_path
        )
        if dataset_exists
        else 0
    )

    print(
        "   Dataset size:",
        dataset_size,
        "bytes"
    )

    check(
        "Training dataset available",
        dataset_exists and dataset_size > 0
    )

except Exception:

    check(
        "Training dataset available",
        False
    )


# ============================================================
# 8. PYTHON IMPORT VALIDATION
# ============================================================

print("\n" + "=" * 70)
print("8. CORE MODULE IMPORT VALIDATION")
print("=" * 70)

try:

    sys.path.insert(
        0,
        BASE_DIR
    )

    from scanner.scan import scan_network
    from shadow_it.detect import detect_shadow_it
    from ai.feature_extractor import extract_features
    from ai.predict import predict_risk
    from impact.impact_analyzer import analyze_impact
    from decision.decision_engine import generate_decision
    from api.routes import router

    check(
        "Core modules import successfully",
        True
    )

except Exception as error:

    print(
        "   Import error:",
        error
    )

    check(
        "Core modules import successfully",
        False
    )


# ============================================================
# 9. MODEL PREDICTION SMOKE TEST
# ============================================================

print("\n" + "=" * 70)
print("9. MODEL PREDICTION VERIFICATION")
print("=" * 70)

try:

    test_features = {

        "unknown_device": 1,

        "open_port_count": 10,

        "critical_cve_count": 5,

        "patch_status": 0,

        "os_outdated": 1,

        "sensitive_network_access": 1
    }

    prediction = predict_risk(
        test_features
    )

    risk = prediction.get(
        "risk"
    )

    confidence = prediction.get(
        "confidence"
    )

    print(
        "   Test Risk       :",
        risk
    )

    print(
        "   Test Confidence :",
        confidence
    )

    valid_risks = {

        "Low",
        "Medium",
        "High",
        "Critical"
    }

    check(
        "Prediction returns valid risk",
        risk in valid_risks
    )

except Exception as error:

    print(
        "   Prediction error:",
        error
    )

    check(
        "Prediction returns valid risk",
        False
    )


# ============================================================
# 10. FINAL DEPLOYMENT STATUS
# ============================================================

print("\n" + "=" * 70)
print("MODULE 29 FINAL RESULT")
print("=" * 70)

print(
    "Tests Passed :",
    passed
)

print(
    "Tests Failed :",
    failed
)

print(
    "Total Tests  :",
    passed + failed
)

print("=" * 70)

if failed == 0:

    print(
        "MODULE 29 FINAL DEPLOYMENT VERIFICATION: PASSED"
    )

    print()

    print(
        "Project Structure -> Model -> Dataset"
    )

    print(
        "Configuration -> API -> Prediction"
    )

    print()

    print(
        "FINAL DEPLOYMENT VERIFICATION COMPLETE"
    )

else:

    print(
        "MODULE 29 FINAL DEPLOYMENT VERIFICATION: FAILED"
    )

    print(
        "Please fix the failed checks before deployment."
    )

print("=" * 70)