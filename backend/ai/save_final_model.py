import json
import shutil
from pathlib import Path

import joblib


# ============================================================
# SHADOW IT AI
# MODULE 9 - FINAL MODEL CREATION
# ============================================================


# ============================================================
# PATH CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_DIR = (
    BASE_DIR
    / "ai"
    / "models"
)

SOURCE_MODEL_PATH = (
    MODEL_DIR
    / "xgboost_model.pkl"
)

FINAL_MODEL_PATH = (
    MODEL_DIR
    / "risk_model.pkl"
)

LABEL_MAPPING_PATH = (
    MODEL_DIR
    / "label_mapping.json"
)

FEATURE_CONFIG_PATH = (
    MODEL_DIR
    / "feature_config.json"
)


# ============================================================
# AUTHORITATIVE FEATURE CONFIGURATION
# ============================================================

FEATURE_COLUMNS = [
    "unknown_device",
    "open_port_count",
    "critical_cve_count",
    "patch_status",
    "os_outdated",
    "sensitive_network_access",
]


TARGET_COLUMN = "risk"


# ============================================================
# AUTHORITATIVE RISK MAPPING
# ============================================================

LABEL_MAPPING = {
    "Low": 0,
    "Medium": 1,
    "High": 2,
    "Critical": 3,
}


# ============================================================
# HELPER
# ============================================================

def print_section(title):

    print()
    print("=" * 70)
    print(title)
    print("=" * 70)


# ============================================================
# CHECK SOURCE MODEL
# ============================================================

def check_source_model():

    print_section(
        "1. CHECKING SELECTED XGBOOST MODEL"
    )

    print(
        "Selected model: XGBoost"
    )

    print()
    print(
        "Source model:"
    )

    print(
        SOURCE_MODEL_PATH
    )

    if not SOURCE_MODEL_PATH.exists():

        print()
        print(
            "ERROR: XGBoost model not found."
        )

        print(
            "Run Module 6 first:"
        )

        print(
            "python ai\\train_xgboost.py"
        )

        return False

    print()
    print(
        "XGBoost model found successfully."
    )

    return True


# ============================================================
# LOAD AND VALIDATE MODEL
# ============================================================

def load_model():

    print_section(
        "2. LOADING SELECTED MODEL"
    )

    try:

        model = joblib.load(
            SOURCE_MODEL_PATH
        )

    except Exception as error:

        print()
        print(
            "ERROR: Failed to load XGBoost model."
        )

        print(
            f"Error: {error}"
        )

        return None

    print(
        "XGBoost model loaded successfully."
    )

    # --------------------------------------------------------
    # Validate predict method
    # --------------------------------------------------------

    if not hasattr(model, "predict"):

        print()
        print(
            "ERROR: Loaded object does not "
            "have a predict() method."
        )

        return None

    # --------------------------------------------------------
    # Validate predict_proba
    # --------------------------------------------------------

    if not hasattr(model, "predict_proba"):

        print()
        print(
            "ERROR: Selected model does not "
            "support predict_proba()."
        )

        return None

    print(
        "Prediction capability: PASS"
    )

    print(
        "Probability capability: PASS"
    )

    return model


# ============================================================
# VALIDATE MODEL CLASSES
# ============================================================

def validate_model_classes(model):

    print_section(
        "3. VALIDATING MODEL CLASSES"
    )

    expected_classes = [
        0,
        1,
        2,
        3,
    ]

    if not hasattr(model, "classes_"):

        print(
            "ERROR: Model does not expose classes_."
        )

        return False

    actual_classes = list(
        model.classes_
    )

    print(
        f"Model classes   : {actual_classes}"
    )

    print(
        f"Expected classes: {expected_classes}"
    )

    if actual_classes != expected_classes:

        print()
        print(
            "ERROR: Model class mapping mismatch."
        )

        return False

    print()
    print(
        "Model class mapping: PASS"
    )

    print()
    print(
        "Authoritative risk mapping:"
    )

    for risk, value in LABEL_MAPPING.items():

        print(
            f"   {risk:<10} -> {value}"
        )

    return True


# ============================================================
# SAVE FINAL MODEL
# ============================================================

def save_final_model(model):

    print_section(
        "4. SAVING FINAL MODEL"
    )

    MODEL_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    try:

        joblib.dump(
            model,
            FINAL_MODEL_PATH
        )

    except Exception as error:

        print()
        print(
            "ERROR: Failed to save final model."
        )

        print(
            f"Error: {error}"
        )

        return False

    print(
        "Final model saved successfully."
    )

    print()
    print(
        "Final model path:"
    )

    print(
        FINAL_MODEL_PATH
    )

    return True


# ============================================================
# SAVE LABEL MAPPING
# ============================================================

def save_label_mapping():

    print_section(
        "5. SAVING LABEL MAPPING"
    )

    try:

        with open(
            LABEL_MAPPING_PATH,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                LABEL_MAPPING,
                file,
                indent=4
            )

    except Exception as error:

        print()
        print(
            "ERROR: Failed to save label mapping."
        )

        print(
            f"Error: {error}"
        )

        return False

    print(
        "Label mapping saved successfully."
    )

    print()
    print(
        "Mapping:"
    )

    for risk, value in LABEL_MAPPING.items():

        print(
            f"   {risk:<10} -> {value}"
        )

    print()
    print(
        "Path:"
    )

    print(
        LABEL_MAPPING_PATH
    )

    return True


# ============================================================
# SAVE FEATURE CONFIGURATION
# ============================================================

def save_feature_config():

    print_section(
        "6. SAVING FEATURE CONFIGURATION"
    )

    feature_config = {
        "features": FEATURE_COLUMNS,
        "target": TARGET_COLUMN,
        "feature_count": len(FEATURE_COLUMNS)
    }

    try:

        with open(
            FEATURE_CONFIG_PATH,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                feature_config,
                file,
                indent=4
            )

    except Exception as error:

        print()
        print(
            "ERROR: Failed to save feature configuration."
        )

        print(
            f"Error: {error}"
        )

        return False

    print(
        "Feature configuration saved successfully."
    )

    print()
    print(
        "Final feature order:"
    )

    for index, feature in enumerate(
        FEATURE_COLUMNS,
        start=1
    ):

        print(
            f"   {index}. {feature}"
        )

    print()
    print(
        "Path:"
    )

    print(
        FEATURE_CONFIG_PATH
    )

    return True


# ============================================================
# VERIFY FINAL FILES
# ============================================================

def verify_final_files():

    print_section(
        "7. FINAL FILE VERIFICATION"
    )

    files = {
        "Final model": FINAL_MODEL_PATH,
        "Label mapping": LABEL_MAPPING_PATH,
        "Feature config": FEATURE_CONFIG_PATH,
    }

    all_valid = True

    for name, path in files.items():

        if path.exists():

            print(
                f"PASS - {name}"
            )

            print(
                f"      {path}"
            )

        else:

            print(
                f"FAIL - {name}"
            )

            print(
                f"      {path}"
            )

            all_valid = False

    return all_valid


# ============================================================
# FINAL SUMMARY
# ============================================================

def final_summary():

    print_section(
        "FINAL MODULE 9 RESULT"
    )

    print(
        "MODULE 9 FINAL MODEL CREATION "
        "COMPLETED SUCCESSFULLY"
    )

    print()
    print(
        "FINAL SELECTED MODEL: XGBoost"
    )

    print()
    print(
        "Final model:"
    )

    print(
        FINAL_MODEL_PATH
    )

    print()
    print(
        "Label mapping:"
    )

    print(
        LABEL_MAPPING_PATH
    )

    print()
    print(
        "Feature configuration:"
    )

    print(
        FEATURE_CONFIG_PATH
    )

    print()
    print(
        "Authoritative feature order:"
    )

    for index, feature in enumerate(
        FEATURE_COLUMNS,
        start=1
    ):

        print(
            f"   {index}. {feature}"
        )

    print()
    print(
        "Authoritative risk mapping:"
    )

    for risk, value in LABEL_MAPPING.items():

        print(
            f"   {risk:<10} -> {value}"
        )

    print()
    print(
        "STATUS: PASS"
    )

    print()
    print(
        "Next module:"
    )

    print(
        "Module 10 - Final Prediction Pipeline"
    )


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print("#" * 70)
    print("# SHADOW IT AI")
    print("# MODULE 9 - FINAL MODEL CREATION")
    print("#" * 70)

    # --------------------------------------------------------
    # 1. Check selected model
    # --------------------------------------------------------

    if not check_source_model():

        return False

    # --------------------------------------------------------
    # 2. Load model
    # --------------------------------------------------------

    model = load_model()

    if model is None:

        return False

    # --------------------------------------------------------
    # 3. Validate model classes
    # --------------------------------------------------------

    if not validate_model_classes(
        model
    ):

        return False

    # --------------------------------------------------------
    # 4. Save final model
    # --------------------------------------------------------

    if not save_final_model(
        model
    ):

        return False

    # --------------------------------------------------------
    # 5. Save label mapping
    # --------------------------------------------------------

    if not save_label_mapping():

        return False

    # --------------------------------------------------------
    # 6. Save feature configuration
    # --------------------------------------------------------

    if not save_feature_config():

        return False

    # --------------------------------------------------------
    # 7. Verify
    # --------------------------------------------------------

    if not verify_final_files():

        print()
        print(
            "ERROR: Final file verification failed."
        )

        return False

    # --------------------------------------------------------
    # Final
    # --------------------------------------------------------

    final_summary()

    return True


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":

    success = main()

    if not success:

        raise SystemExit(1)