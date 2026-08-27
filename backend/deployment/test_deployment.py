# ============================================================
# SHADOW IT AI
# MODULE 27 - DEPLOYMENT VALIDATION
# ============================================================

import os
import sys
import json
import joblib

# Make backend root available
BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)


# ============================================================
# HEADER
# ============================================================

print()
print("#" * 70)
print("# SHADOW IT AI")
print("# MODULE 27 - DEPLOYMENT VALIDATION")
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
# 1. BACKEND DIRECTORY
# ============================================================

print()
print("=" * 70)
print("1. BACKEND DIRECTORY")
print("=" * 70)

check(
    "Backend directory",
    os.path.isdir(BASE_DIR)
)


# ============================================================
# 2. DEPLOYMENT DIRECTORY
# ============================================================

print()
print("=" * 70)
print("2. DEPLOYMENT DIRECTORY")
print("=" * 70)

deployment_dir = os.path.join(
    BASE_DIR,
    "deployment"
)

check(
    "Deployment directory",
    os.path.isdir(deployment_dir)
)


# ============================================================
# 3. PRODUCTION CONFIGURATION
# ============================================================

print()
print("=" * 70)
print("3. PRODUCTION CONFIGURATION")
print("=" * 70)

config_file = os.path.join(
    deployment_dir,
    "production_config.py"
)

check(
    "production_config.py",
    os.path.isfile(config_file)
)


# ============================================================
# 4. FINAL MODEL
# ============================================================

print()
print("=" * 70)
print("4. FINAL MODEL")
print("=" * 70)

model_file = os.path.join(
    BASE_DIR,
    "ai",
    "models",
    "risk_model.pkl"
)

check(
    "risk_model.pkl",
    os.path.isfile(model_file)
)


# ============================================================
# 5. LOAD MODEL
# ============================================================

print()
print("=" * 70)
print("5. MODEL LOADING")
print("=" * 70)

model_loaded = False

try:

    model = joblib.load(model_file)

    model_loaded = model is not None

except Exception as error:

    print("   Model loading error:", error)


check(
    "Risk model loads successfully",
    model_loaded
)


# ============================================================
# 6. LABEL MAPPING
# ============================================================

print()
print("=" * 70)
print("6. LABEL MAPPING")
print("=" * 70)

label_file = os.path.join(
    BASE_DIR,
    "ai",
    "models",
    "label_mapping.json"
)

label_valid = False

try:

    with open(
        label_file,
        "r",
        encoding="utf-8"
    ) as file:

        mapping = json.load(file)

    expected_labels = {
        "Low": 0,
        "Medium": 1,
        "High": 2,
        "Critical": 3
    }

    label_valid = mapping == expected_labels

except Exception as error:

    print("   Label mapping error:", error)


check(
    "Label mapping is correct",
    label_valid
)


# ============================================================
# 7. FEATURE CONFIGURATION
# ============================================================

print()
print("=" * 70)
print("7. FEATURE CONFIGURATION")
print("=" * 70)

feature_file = os.path.join(
    BASE_DIR,
    "ai",
    "models",
    "feature_config.json"
)

feature_valid = False

try:

    with open(
        feature_file,
        "r",
        encoding="utf-8"
    ) as file:

        feature_config = json.load(file)

    required_features = [
        "unknown_device",
        "open_port_count",
        "critical_cve_count",
        "patch_status",
        "os_outdated",
        "sensitive_network_access"
    ]

    feature_text = json.dumps(
        feature_config
    )

    feature_valid = all(
        feature in feature_text
        for feature in required_features
    )

except Exception as error:

    print(
        "   Feature configuration error:",
        error
    )


check(
    "All required features configured",
    feature_valid
)


# ============================================================
# 8. DATASET
# ============================================================

print()
print("=" * 70)
print("8. DATASET")
print("=" * 70)

dataset_file = os.path.join(
    BASE_DIR,
    "dataset",
    "devices.csv"
)

check(
    "Training dataset exists",
    os.path.isfile(dataset_file)
)


# ============================================================
# 9. API ROUTES
# ============================================================

print()
print("=" * 70)
print("9. API ROUTES")
print("=" * 70)

routes_file = os.path.join(
    BASE_DIR,
    "api",
    "routes.py"
)

check(
    "API routes exist",
    os.path.isfile(routes_file)
)


# ============================================================
# 10. DEPLOYMENT COMPONENTS
# ============================================================

print()
print("=" * 70)
print("10. DEPLOYMENT COMPONENTS")
print("=" * 70)

required_components = [

    os.path.join(BASE_DIR, "scanner"),
    os.path.join(BASE_DIR, "shadow_it"),
    os.path.join(BASE_DIR, "ai"),
    os.path.join(BASE_DIR, "impact"),
    os.path.join(BASE_DIR, "decision"),
    os.path.join(BASE_DIR, "api"),
    os.path.join(BASE_DIR, "integration"),
    os.path.join(BASE_DIR, "deployment")
]

components_valid = all(
    os.path.isdir(path)
    for path in required_components
)

check(
    "All deployment components present",
    components_valid
)


# ============================================================
# FINAL RESULT
# ============================================================

print()
print("=" * 70)
print("MODULE 27 FINAL RESULT")
print("=" * 70)

print(f"Tests Passed : {passed}")
print(f"Tests Failed : {failed}")
print(f"Total Tests  : {passed + failed}")

print()

if failed == 0:

    print(
        "MODULE 27 DEPLOYMENT VALIDATION: PASSED"
    )

    print()
    print(
        "Project Structure -> Configuration -> Model"
    )

    print(
        "Dataset -> Features -> API -> Deployment"
    )

else:

    print(
        "MODULE 27 DEPLOYMENT VALIDATION: FAILED"
    )

print("=" * 70)