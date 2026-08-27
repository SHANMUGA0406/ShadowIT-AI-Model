import json
import joblib
import numpy as np
import pandas as pd
import shap

from pathlib import Path


# ============================================================
# SHADOW IT AI
# MODULE 11 - SHAP EXPLAINABILITY
# ============================================================


# ============================================================
# PATH CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_DIR = BASE_DIR / "ai" / "models"

MODEL_PATH = MODEL_DIR / "risk_model.pkl"

LABEL_MAPPING_PATH = (
    MODEL_DIR / "label_mapping.json"
)

FEATURE_CONFIG_PATH = (
    MODEL_DIR / "feature_config.json"
)


# ============================================================
# AUTHORITATIVE FEATURE ORDER
# ============================================================

FEATURE_COLUMNS = [
    "unknown_device",
    "open_port_count",
    "critical_cve_count",
    "patch_status",
    "os_outdated",
    "sensitive_network_access",
]


# ============================================================
# AUTHORITATIVE RISK MAPPING
# ============================================================

RISK_MAPPING = {
    0: "Low",
    1: "Medium",
    2: "High",
    3: "Critical",
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
# LOAD FINAL MODEL
# ============================================================

def load_model():

    print_section(
        "1. LOADING FINAL XGBOOST MODEL"
    )

    if not MODEL_PATH.exists():

        print(
            "ERROR: Final model not found."
        )

        print(
            MODEL_PATH
        )

        return None

    try:

        model = joblib.load(
            MODEL_PATH
        )

    except Exception as error:

        print(
            "ERROR: Failed to load model."
        )

        print(
            f"Error: {error}"
        )

        return None

    print(
        "Final XGBoost model loaded successfully."
    )

    print(
        f"Model path: {MODEL_PATH}"
    )

    return model


# ============================================================
# LOAD FEATURE CONFIGURATION
# ============================================================

def load_feature_config():

    print_section(
        "2. LOADING FEATURE CONFIGURATION"
    )

    if not FEATURE_CONFIG_PATH.exists():

        print(
            "ERROR: Feature configuration not found."
        )

        print(
            FEATURE_CONFIG_PATH
        )

        return None

    try:

        with open(
            FEATURE_CONFIG_PATH,
            "r",
            encoding="utf-8"
        ) as file:

            config = json.load(file)

    except Exception as error:

        print(
            "ERROR: Failed to load feature configuration."
        )

        print(
            f"Error: {error}"
        )

        return None

    print(
        "Feature configuration loaded successfully."
    )

    return config


# ============================================================
# VALIDATE FEATURE CONFIGURATION
# ============================================================

def validate_feature_config(config):

    print_section(
        "3. VALIDATING FEATURE CONFIGURATION"
    )

    configured_features = None

    if isinstance(config, list):

        configured_features = config

    elif isinstance(config, dict):

        if "features" in config:

            configured_features = (
                config["features"]
            )

        elif "feature_columns" in config:

            configured_features = (
                config["feature_columns"]
            )

    if configured_features is None:

        print(
            "ERROR: Feature list not found "
            "in feature_config.json."
        )

        return False

    if configured_features != FEATURE_COLUMNS:

        print(
            "ERROR: Feature order mismatch."
        )

        print()
        print("Expected:")

        for index, feature in enumerate(
            FEATURE_COLUMNS,
            start=1
        ):

            print(
                f"   {index}. {feature}"
            )

        print()
        print("Received:")

        for index, feature in enumerate(
            configured_features,
            start=1
        ):

            print(
                f"   {index}. {feature}"
            )

        return False

    print(
        "Feature configuration validation: PASS"
    )

    print()
    print("Authoritative feature order:")

    for index, feature in enumerate(
        FEATURE_COLUMNS,
        start=1
    ):

        print(
            f"   {index}. {feature}"
        )

    return True


# ============================================================
# VALIDATE MODEL
# ============================================================

def validate_model(model):

    print_section(
        "4. VALIDATING MODEL"
    )

    if not hasattr(
        model,
        "predict"
    ):

        print(
            "ERROR: Model does not support prediction."
        )

        return False

    if not hasattr(
        model,
        "predict_proba"
    ):

        print(
            "ERROR: Model does not support probabilities."
        )

        return False

    if not hasattr(
        model,
        "classes_"
    ):

        print(
            "ERROR: Model classes are unavailable."
        )

        return False

    model_classes = [
        int(value)
        for value in model.classes_
    ]

    expected_classes = [
        0,
        1,
        2,
        3,
    ]

    if model_classes != expected_classes:

        print(
            "ERROR: Model class mapping mismatch."
        )

        print(
            f"Model classes: {model_classes}"
        )

        print(
            f"Expected: {expected_classes}"
        )

        return False

    print(
        "Prediction capability: PASS"
    )

    print(
        "Probability capability: PASS"
    )

    print(
        "Model class mapping: PASS"
    )

    return True


# ============================================================
# CREATE TEST DEVICE
# ============================================================

def create_test_device():

    print_section(
        "5. CREATING TEST DEVICE"
    )

    test_device = pd.DataFrame(
        [
            {
                "unknown_device": 1,
                "open_port_count": 8,
                "critical_cve_count": 3,
                "patch_status": 0,
                "os_outdated": 1,
                "sensitive_network_access": 1,
            }
        ],
        columns=FEATURE_COLUMNS
    )

    print(
        "Test device features:"
    )

    print()

    print(
        test_device.to_string(
            index=False
        )
    )

    return test_device


# ============================================================
# VALIDATE TEST DEVICE
# ============================================================

def validate_test_device(
    test_device
):

    print_section(
        "6. VALIDATING TEST DEVICE"
    )

    if list(
        test_device.columns
    ) != FEATURE_COLUMNS:

        print(
            "ERROR: Feature order mismatch."
        )

        return False

    if test_device.isnull().any().any():

        print(
            "ERROR: Missing values found."
        )

        return False

    for column in FEATURE_COLUMNS:

        if not pd.api.types.is_numeric_dtype(
            test_device[column]
        ):

            print(
                f"ERROR: {column} "
                f"must be numeric."
            )

            return False

    binary_features = [
        "unknown_device",
        "patch_status",
        "os_outdated",
        "sensitive_network_access",
    ]

    for column in binary_features:

        values = set(
            test_device[column].astype(int)
        )

        if not values.issubset({0, 1}):

            print(
                f"ERROR: {column} "
                f"must contain only 0 or 1."
            )

            return False

    if (
        test_device["open_port_count"] < 0
    ).any():

        print(
            "ERROR: open_port_count cannot be negative."
        )

        return False

    if (
        test_device["critical_cve_count"] < 0
    ).any():

        print(
            "ERROR: critical_cve_count cannot be negative."
        )

        return False

    print(
        "Test device validation: PASS"
    )

    return True


# ============================================================
# PREDICT DEVICE RISK
# ============================================================

def predict_device_risk(
    model,
    test_device
):

    print_section(
        "7. PREDICTING DEVICE RISK"
    )

    prediction = model.predict(
        test_device
    )

    probabilities = model.predict_proba(
        test_device
    )

    predicted_class = int(
        prediction[0]
    )

    confidence = float(
        np.max(probabilities[0])
    )

    risk_name = RISK_MAPPING.get(
        predicted_class
    )

    if risk_name is None:

        print(
            "ERROR: Unknown risk class."
        )

        return None

    print(
        f"Predicted class : {predicted_class}"
    )

    print(
        f"Predicted risk  : {risk_name}"
    )

    print(
        f"Confidence      : "
        f"{confidence * 100:.2f}%"
    )

    return predicted_class


# ============================================================
# CREATE SHAP EXPLAINER
# ============================================================

def create_shap_explainer(
    model
):

    print_section(
        "8. CREATING SHAP EXPLAINER"
    )

    try:

        explainer = shap.TreeExplainer(
            model
        )

    except Exception as error:

        print(
            "ERROR: Failed to create SHAP TreeExplainer."
        )

        print(
            f"Error: {error}"
        )

        return None

    print(
        "SHAP TreeExplainer created successfully."
    )

    return explainer


# ============================================================
# CALCULATE SHAP VALUES
# ============================================================

def calculate_shap_values(
    explainer,
    test_device
):

    print_section(
        "9. CALCULATING SHAP VALUES"
    )

    try:

        shap_values = explainer.shap_values(
            test_device
        )

    except Exception as error:

        print(
            "ERROR: SHAP value calculation failed."
        )

        print(
            f"Error: {error}"
        )

        return None

    print(
        "SHAP values calculated successfully."
    )

    return shap_values


# ============================================================
# NORMALIZE SHAP OUTPUT
# ============================================================

def extract_class_shap_values(
    shap_values,
    predicted_class,
    feature_count
):

    """
    SHAP can return different structures depending
    on the installed SHAP version and XGBoost version.

    This function extracts the SHAP contribution vector
    corresponding to the predicted class when possible.
    """

    # --------------------------------------------------------
    # Newer SHAP versions may return an ndarray:
    #
    # (samples, features, classes)
    # --------------------------------------------------------

    if isinstance(
        shap_values,
        np.ndarray
    ):

        values = shap_values

        if values.ndim == 3:

            return values[
                0,
                :,
                predicted_class
            ]

        if values.ndim == 2:

            return values[0]

    # --------------------------------------------------------
    # Older SHAP versions may return:
    #
    # list[class] -> array(samples, features)
    # --------------------------------------------------------

    if isinstance(
        shap_values,
        list
    ):

        if (
            len(shap_values)
            > predicted_class
        ):

            class_values = np.asarray(
                shap_values[
                    predicted_class
                ]
            )

            if class_values.ndim == 2:

                return class_values[0]

            if class_values.ndim == 1:

                return class_values

    print(
        "WARNING: Unexpected SHAP output format."
    )

    print(
        f"SHAP type: {type(shap_values)}"
    )

    if isinstance(
        shap_values,
        np.ndarray
    ):

        print(
            f"SHAP shape: {shap_values.shape}"
        )

    return None


# ============================================================
# DISPLAY SHAP EXPLANATION
# ============================================================

def display_shap_explanation(
    shap_values,
    predicted_class
):

    print_section(
        "10. SHAP FEATURE CONTRIBUTIONS"
    )

    class_name = RISK_MAPPING[
        predicted_class
    ]

    print(
        f"Explanation for predicted risk: "
        f"{class_name}"
    )

    print()

    shap_vector = extract_class_shap_values(
        shap_values,
        predicted_class,
        len(FEATURE_COLUMNS)
    )

    if shap_vector is None:

        return None

    if len(shap_vector) != len(
        FEATURE_COLUMNS
    ):

        print(
            "ERROR: SHAP feature count mismatch."
        )

        print(
            f"Expected: {len(FEATURE_COLUMNS)}"
        )

        print(
            f"Received: {len(shap_vector)}"
        )

        return None

    explanation_df = pd.DataFrame(
        {
            "feature": FEATURE_COLUMNS,
            "shap_value": shap_vector,
        }
    )

    explanation_df[
        "absolute_shap"
    ] = explanation_df[
        "shap_value"
    ].abs()

    explanation_df[
        "effect"
    ] = np.where(
        explanation_df["shap_value"] >= 0,
        "Increases risk",
        "Decreases risk"
    )

    explanation_df = (
        explanation_df
        .sort_values(
            "absolute_shap",
            ascending=False
        )
        .reset_index(drop=True)
    )

    print(
        "Feature contribution ranking:"
    )

    print()

    for index, row in (
        explanation_df.iterrows()
    ):

        print(
            f"{index + 1}. "
            f"{row['feature']}"
        )

        print(
            f"   SHAP value : "
            f"{row['shap_value']:.6f}"
        )

        print(
            f"   Effect     : "
            f"{row['effect']}"
        )

        print()

    return explanation_df


# ============================================================
# DISPLAY HUMAN-READABLE EXPLANATION
# ============================================================

def display_human_explanation(
    explanation_df
):

    print_section(
        "11. HUMAN-READABLE XAI EXPLANATION"
    )

    print(
        "The model's prediction is influenced by:"
    )

    print()

    for index, row in (
        explanation_df.head(3).iterrows()
    ):

        feature = row["feature"]

        effect = row["effect"]

        shap_value = row["shap_value"]

        print(
            f"{index + 1}. {feature}"
        )

        print(
            f"   Contribution: "
            f"{shap_value:.6f}"
        )

        print(
            f"   Interpretation: "
            f"{effect}"
        )

        print()


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print("#" * 70)
    print("# SHADOW IT AI")
    print("# MODULE 11 - SHAP EXPLAINABILITY")
    print("#" * 70)

    # --------------------------------------------------------
    # Load model
    # --------------------------------------------------------

    model = load_model()

    if model is None:

        return False

    # --------------------------------------------------------
    # Load feature configuration
    # --------------------------------------------------------

    feature_config = (
        load_feature_config()
    )

    if feature_config is None:

        return False

    # --------------------------------------------------------
    # Validate configuration
    # --------------------------------------------------------

    if not validate_feature_config(
        feature_config
    ):

        return False

    # --------------------------------------------------------
    # Validate model
    # --------------------------------------------------------

    if not validate_model(
        model
    ):

        return False

    # --------------------------------------------------------
    # Create test device
    # --------------------------------------------------------

    test_device = create_test_device()

    # --------------------------------------------------------
    # Validate test device
    # --------------------------------------------------------

    if not validate_test_device(
        test_device
    ):

        return False

    # --------------------------------------------------------
    # Predict
    # --------------------------------------------------------

    predicted_class = (
        predict_device_risk(
            model,
            test_device
        )
    )

    if predicted_class is None:

        return False

    # --------------------------------------------------------
    # Create SHAP explainer
    # --------------------------------------------------------

    explainer = (
        create_shap_explainer(
            model
        )
    )

    if explainer is None:

        return False

    # --------------------------------------------------------
    # Calculate SHAP
    # --------------------------------------------------------

    shap_values = (
        calculate_shap_values(
            explainer,
            test_device
        )
    )

    if shap_values is None:

        return False

    # --------------------------------------------------------
    # Display explanation
    # --------------------------------------------------------

    explanation_df = (
        display_shap_explanation(
            shap_values,
            predicted_class
        )
    )

    if explanation_df is None:

        return False

    # --------------------------------------------------------
    # Human explanation
    # --------------------------------------------------------

    display_human_explanation(
        explanation_df
    )

    # --------------------------------------------------------
    # Final result
    # --------------------------------------------------------

    print_section(
        "FINAL MODULE 11 RESULT"
    )

    print(
        "MODULE 11 SHAP EXPLAINABILITY "
        "COMPLETED SUCCESSFULLY"
    )

    print()
    print(
        f"Predicted risk: "
        f"{RISK_MAPPING[predicted_class]}"
    )

    print()
    print(
        "Top contributing features:"
    )

    for index, row in (
        explanation_df.head(3).iterrows()
    ):

        print(
            f"   {index + 1}. "
            f"{row['feature']} "
            f"({row['effect']})"
        )

    print()
    print("=" * 70)
    print("STATUS: PASS")
    print("=" * 70)

    return True


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":

    success = main()

    if not success:

        raise SystemExit(1)