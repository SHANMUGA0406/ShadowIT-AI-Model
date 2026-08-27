# ============================================================
# SHADOW IT AI
# MODULE 30 - FINAL RELEASE & PROJECT HANDOVER
# ============================================================

import os
import json


print("\n" + "=" * 70)
print("# SHADOW IT AI")
print("# MODULE 30 - FINAL RELEASE & PROJECT HANDOVER")
print("=" * 70)


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

paths = {
    "Scanner": os.path.join(BASE_DIR, "scanner"),
    "Shadow IT": os.path.join(BASE_DIR, "shadow_it"),
    "AI": os.path.join(BASE_DIR, "ai"),
    "Impact": os.path.join(BASE_DIR, "impact"),
    "Decision": os.path.join(BASE_DIR, "decision"),
    "API": os.path.join(BASE_DIR, "api"),
    "Dataset": os.path.join(BASE_DIR, "dataset"),
    "Deployment": os.path.join(BASE_DIR, "deployment"),
    "Models": os.path.join(BASE_DIR, "ai", "models"),
}


required_files = {
    "Dataset": os.path.join(
        BASE_DIR,
        "dataset",
        "devices.csv"
    ),

    "Risk Model": os.path.join(
        BASE_DIR,
        "ai",
        "models",
        "risk_model.pkl"
    ),

    "Label Mapping": os.path.join(
        BASE_DIR,
        "ai",
        "models",
        "label_mapping.json"
    ),

    "Feature Configuration": os.path.join(
        BASE_DIR,
        "ai",
        "models",
        "feature_config.json"
    ),

    "API Routes": os.path.join(
        BASE_DIR,
        "api",
        "routes.py"
    ),

    "Production Configuration": os.path.join(
        BASE_DIR,
        "deployment",
        "production_config.py"
    ),
}


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
# 1. PROJECT COMPONENTS
# ============================================================

print("\n" + "=" * 70)
print("1. FINAL PROJECT COMPONENTS")
print("=" * 70)

for name, path in paths.items():

    check(
        f"{name} component",
        os.path.isdir(path)
    )


# ============================================================
# 2. FINAL FILES
# ============================================================

print("\n" + "=" * 70)
print("2. FINAL RELEASE FILES")
print("=" * 70)

for name, path in required_files.items():

    check(
        name,
        os.path.isfile(path)
    )


# ============================================================
# 3. DATASET CHECK
# ============================================================

print("\n" + "=" * 70)
print("3. DATASET RELEASE CHECK")
print("=" * 70)

dataset_path = required_files["Dataset"]

if os.path.isfile(dataset_path):

    dataset_size = os.path.getsize(
        dataset_path
    )

    print(
        "   Dataset size:",
        dataset_size,
        "bytes"
    )

    check(
        "Dataset is available",
        dataset_size > 0
    )

else:

    check(
        "Dataset is available",
        False
    )


# ============================================================
# 4. MODEL CHECK
# ============================================================

print("\n" + "=" * 70)
print("4. FINAL AI MODEL CHECK")
print("=" * 70)

model_path = required_files["Risk Model"]

if os.path.isfile(model_path):

    model_size = os.path.getsize(
        model_path
    )

    print(
        "   Model size:",
        model_size,
        "bytes"
    )

    check(
        "Final risk model available",
        model_size > 0
    )

else:

    check(
        "Final risk model available",
        False
    )


# ============================================================
# 5. LABEL MAPPING CHECK
# ============================================================

print("\n" + "=" * 70)
print("5. LABEL MAPPING RELEASE CHECK")
print("=" * 70)

mapping_path = required_files["Label Mapping"]

try:

    with open(
        mapping_path,
        "r",
        encoding="utf-8"
    ) as file:

        mapping = json.load(file)

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
        "Final label mapping correct",
        mapping == expected_mapping
    )

except Exception as error:

    print(
        "   Mapping error:",
        error
    )

    check(
        "Final label mapping correct",
        False
    )


# ============================================================
# 6. FEATURE CONFIGURATION CHECK
# ============================================================

print("\n" + "=" * 70)
print("6. FEATURE CONFIGURATION RELEASE CHECK")
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

        config = json.load(file)

    if isinstance(config, list):

        configured_features = config

    elif isinstance(config, dict):

        configured_features = config.get(
            "features",
            []
        )

    else:

        configured_features = []

    print(
        "   Required features:",
        required_features
    )

    check(
        "All final features configured",
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
        "All final features configured",
        False
    )


# ============================================================
# 7. API RELEASE CHECK
# ============================================================

print("\n" + "=" * 70)
print("7. API RELEASE CHECK")
print("=" * 70)

api_routes = required_files["API Routes"]

check(
    "FastAPI routes available",
    os.path.isfile(api_routes)
)


# ============================================================
# 8. DEPLOYMENT CHECK
# ============================================================

print("\n" + "=" * 70)
print("8. DEPLOYMENT RELEASE CHECK")
print("=" * 70)

deployment_files = [
    "production_config.py",
    "test_deployment.py",
    "test_smoke.py",
    "final_deployment_verification.py"
]

for filename in deployment_files:

    path = os.path.join(
        BASE_DIR,
        "deployment",
        filename
    )

    check(
        filename,
        os.path.isfile(path)
    )


# ============================================================
# 9. RELEASE STATUS
# ============================================================

print("\n" + "=" * 70)
print("9. RELEASE STATUS")
print("=" * 70)

release_ready = (
    failed == 0
)

check(
    "System ready for final handover",
    release_ready
)


# ============================================================
# FINAL RESULT
# ============================================================

print("\n" + "=" * 70)
print("MODULE 30 FINAL RESULT")
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
        "MODULE 30 FINAL RELEASE VALIDATION: PASSED"
    )

    print()
    print(
        "Shadow IT AI PROJECT: RELEASE READY"
    )

    print()
    print(
        "Scanner -> Shadow IT -> Features -> AI"
    )

    print(
        "Impact -> Decision -> API -> Deployment"
    )

    print()
    print(
        "FINAL PROJECT HANDOVER VALIDATION COMPLETE"
    )

else:

    print(
        "MODULE 30 FINAL RELEASE VALIDATION: FAILED"
    )

    print(
        "Fix the failed checks before release."
    )

print("=" * 70)