import pandas as pd
import joblib

from pathlib import Path

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
)


# ============================================================
# SHADOW IT AI
# CHANGE 3
# RANDOM FOREST vs XGBOOST
# FINAL MODEL SELECTION
# ============================================================


# ============================================================
# PATH CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

SPLIT_DATASET_DIR = (
    BASE_DIR
    / "dataset"
    / "split"
)

MODEL_DIR = (
    BASE_DIR
    / "ai"
    / "models"
)

RF_MODEL_PATH = (
    MODEL_DIR
    / "random_forest_model.pkl"
)

XGB_MODEL_PATH = (
    MODEL_DIR
    / "xgboost_model.pkl"
)


# ============================================================
# DATASET PATH
# ============================================================

X_TEST_PATH = (
    SPLIT_DATASET_DIR
    / "X_test.csv"
)

Y_TEST_PATH = (
    SPLIT_DATASET_DIR
    / "y_test.csv"
)


# ============================================================
# AUTHORITATIVE FEATURES
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
# RISK MAPPING
# ============================================================

RISK_NAMES = {
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
# LOAD TEST DATA
# ============================================================

def load_test_data():

    print_section(
        "1. LOADING COMMON TEST DATA"
    )

    if not X_TEST_PATH.exists():

        print(
            "ERROR: X_test.csv not found."
        )

        print(
            "Run:"
        )

        print(
            "python ai\\split_data.py"
        )

        return None

    if not Y_TEST_PATH.exists():

        print(
            "ERROR: y_test.csv not found."
        )

        print(
            "Run:"
        )

        print(
            "python ai\\split_data.py"
        )

        return None

    try:

        X_test = pd.read_csv(
            X_TEST_PATH
        )

        y_test_df = pd.read_csv(
            Y_TEST_PATH
        )

    except Exception as error:

        print(
            "ERROR: Failed to load test data."
        )

        print(
            f"Error: {error}"
        )

        return None

    if "risk" in y_test_df.columns:

        y_test = y_test_df[
            "risk"
        ]

    else:

        y_test = y_test_df.iloc[:, 0]

    # --------------------------------------------------------
    # Validate feature order
    # --------------------------------------------------------

    if list(X_test.columns) != FEATURE_COLUMNS:

        print(
            "ERROR: Test feature order is incorrect."
        )

        print()
        print(
            "Expected:"
        )

        print(
            FEATURE_COLUMNS
        )

        print()
        print(
            "Received:"
        )

        print(
            list(X_test.columns)
        )

        return None

    # --------------------------------------------------------
    # Validate shape
    # --------------------------------------------------------

    if len(X_test) != len(y_test):

        print(
            "ERROR: X_test and y_test size mismatch."
        )

        return None

    print(
        "Common test dataset loaded successfully."
    )

    print()
    print(
        f"X_test : {X_test.shape}"
    )

    print(
        f"y_test : {y_test.shape}"
    )

    print()
    print(
        "Test records used for BOTH models: "
        f"{len(X_test)}"
    )

    print(
        "Feature order: PASS"
    )

    return X_test, y_test


# ============================================================
# LOAD MODELS
# ============================================================

def load_models():

    print_section(
        "2. LOADING TRAINED MODELS"
    )

    if not RF_MODEL_PATH.exists():

        print(
            "ERROR: Random Forest model not found."
        )

        print(
            RF_MODEL_PATH
        )

        return None

    if not XGB_MODEL_PATH.exists():

        print(
            "ERROR: XGBoost model not found."
        )

        print(
            XGB_MODEL_PATH
        )

        return None

    try:

        random_forest = joblib.load(
            RF_MODEL_PATH
        )

        xgboost = joblib.load(
            XGB_MODEL_PATH
        )

    except Exception as error:

        print(
            "ERROR: Failed to load models."
        )

        print(
            f"Error: {error}"
        )

        return None

    print(
        "Random Forest loaded successfully."
    )

    print(
        "XGBoost loaded successfully."
    )

    return random_forest, xgboost


# ============================================================
# VALIDATE MODELS
# ============================================================

def validate_models(
    random_forest,
    xgboost
):

    print_section(
        "3. MODEL VALIDATION"
    )

    expected_classes = [
        0,
        1,
        2,
        3,
    ]

    # --------------------------------------------------------
    # Random Forest
    # --------------------------------------------------------

    if not hasattr(
        random_forest,
        "predict"
    ):

        print(
            "ERROR: Random Forest has no predict()."
        )

        return False

    if not hasattr(
        random_forest,
        "predict_proba"
    ):

        print(
            "ERROR: Random Forest has no predict_proba()."
        )

        return False

    if list(
        random_forest.classes_
    ) != expected_classes:

        print(
            "ERROR: Random Forest class mapping incorrect."
        )

        return False

    print(
        "Random Forest validation: PASS"
    )

    # --------------------------------------------------------
    # XGBoost
    # --------------------------------------------------------

    if not hasattr(
        xgboost,
        "predict"
    ):

        print(
            "ERROR: XGBoost has no predict()."
        )

        return False

    if not hasattr(
        xgboost,
        "predict_proba"
    ):

        print(
            "ERROR: XGBoost has no predict_proba()."
        )

        return False

    if list(
        xgboost.classes_
    ) != expected_classes:

        print(
            "ERROR: XGBoost class mapping incorrect."
        )

        return False

    print(
        "XGBoost validation: PASS"
    )

    print()
    print(
        "Both models use the same 4 risk classes:"
    )

    for value in expected_classes:

        print(
            f"   {value} -> {RISK_NAMES[value]}"
        )

    return True


# ============================================================
# EVALUATE MODEL
# ============================================================

def evaluate_model(
    model,
    X_test,
    y_test,
    model_name
):

    print_section(
        f"4. EVALUATING {model_name.upper()}"
    )

    predictions = model.predict(
        X_test
    )

    predictions = predictions.astype(
        int
    )

    accuracy = accuracy_score(
        y_test,
        predictions
    )

    precision = precision_score(
        y_test,
        predictions,
        average="weighted",
        zero_division=0
    )

    recall = recall_score(
        y_test,
        predictions,
        average="weighted",
        zero_division=0
    )

    f1 = f1_score(
        y_test,
        predictions,
        average="weighted",
        zero_division=0
    )

    # --------------------------------------------------------
    # Critical Recall
    # --------------------------------------------------------

    cm = confusion_matrix(
        y_test,
        predictions,
        labels=[
            0,
            1,
            2,
            3,
        ]
    )

    critical_actual = cm[3].sum()

    critical_correct = cm[3][3]

    if critical_actual > 0:

        critical_recall = (
            critical_correct
            / critical_actual
        )

    else:

        critical_recall = 0.0

    print()
    print(
        f"Accuracy        : {accuracy:.4f}"
    )

    print(
        f"Precision       : {precision:.4f}"
    )

    print(
        f"Recall          : {recall:.4f}"
    )

    print(
        f"F1 Score        : {f1:.4f}"
    )

    print(
        f"Critical Recall : {critical_recall:.4f}"
    )

    return {
        "model": model_name,
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "critical_recall": critical_recall,
        "predictions": predictions,
    }


# ============================================================
# DISPLAY COMPARISON
# ============================================================

def display_comparison(
    rf_results,
    xgb_results
):

    print_section(
        "5. RANDOM FOREST vs XGBOOST COMPARISON"
    )

    comparison = pd.DataFrame(
        [
            {
                "Model": "Random Forest",
                "Accuracy": rf_results["accuracy"],
                "Precision": rf_results["precision"],
                "Recall": rf_results["recall"],
                "F1 Score": rf_results["f1"],
                "Critical Recall": rf_results[
                    "critical_recall"
                ],
            },
            {
                "Model": "XGBoost",
                "Accuracy": xgb_results["accuracy"],
                "Precision": xgb_results["precision"],
                "Recall": xgb_results["recall"],
                "F1 Score": xgb_results["f1"],
                "Critical Recall": xgb_results[
                    "critical_recall"
                ],
            },
        ]
    )

    display_table = comparison.copy()

    metric_columns = [
        "Accuracy",
        "Precision",
        "Recall",
        "F1 Score",
        "Critical Recall",
    ]

    for column in metric_columns:

        display_table[column] = (
            display_table[column]
            .map(
                lambda value:
                f"{value:.4f}"
            )
        )

    print(
        display_table.to_string(
            index=False
        )
    )

    return comparison


# ============================================================
# SELECT FINAL MODEL
# ============================================================

def select_final_model(
    rf_results,
    xgb_results
):

    print_section(
        "6. FINAL MODEL SELECTION"
    )

    print(
        "Selection priority:"
    )

    print(
        "1. F1 Score"
    )

    print(
        "2. Critical Recall"
    )

    print(
        "3. Accuracy"
    )

    print()

    rf_score = (
        rf_results["f1"],
        rf_results["critical_recall"],
        rf_results["accuracy"],
    )

    xgb_score = (
        xgb_results["f1"],
        xgb_results["critical_recall"],
        xgb_results["accuracy"],
    )

    if xgb_score > rf_score:

        selected_model = "XGBoost"

    else:

        selected_model = "Random Forest"

    print(
        f"Random Forest score : {rf_score}"
    )

    print(
        f"XGBoost score       : {xgb_score}"
    )

    print()

    print(
        f"FINAL SELECTED MODEL: {selected_model}"
    )

    return selected_model


# ============================================================
# FINAL RESULT
# ============================================================

def final_result(
    selected_model
):

    print_section(
        "FINAL CHANGE 3 RESULT"
    )

    print(
        "CHANGE 3 - MODEL COMPARISON "
        "AND FINAL MODEL SELECTION COMPLETED"
    )

    print()
    print(
        f"Selected model: {selected_model}"
    )

    print()
    print(
        "The selected model will be used for:"
    )

    print(
        "   - Final prediction pipeline"
    )

    print(
        "   - SHAP explainability"
    )

    print(
        "   - Risk interpretation"
    )

    print(
        "   - Decision support"
    )

    print(
        "   - FastAPI integration"
    )

    print()
    print(
        "STATUS: PASS"
    )


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print("#" * 70)
    print("# SHADOW IT AI")
    print("# CHANGE 3 - MODEL COMPARISON")
    print("#" * 70)

    # --------------------------------------------------------
    # Load test data
    # --------------------------------------------------------

    data = load_test_data()

    if data is None:

        return False

    X_test, y_test = data

    # --------------------------------------------------------
    # Load models
    # --------------------------------------------------------

    models = load_models()

    if models is None:

        return False

    random_forest, xgboost = models

    # --------------------------------------------------------
    # Validate models
    # --------------------------------------------------------

    if not validate_models(
        random_forest,
        xgboost
    ):

        return False

    # --------------------------------------------------------
    # Evaluate Random Forest
    # --------------------------------------------------------

    rf_results = evaluate_model(
        random_forest,
        X_test,
        y_test,
        "Random Forest"
    )

    # --------------------------------------------------------
    # Evaluate XGBoost
    # --------------------------------------------------------

    xgb_results = evaluate_model(
        xgboost,
        X_test,
        y_test,
        "XGBoost"
    )

    # --------------------------------------------------------
    # Comparison
    # --------------------------------------------------------

    display_comparison(
        rf_results,
        xgb_results
    )

    # --------------------------------------------------------
    # Selection
    # --------------------------------------------------------

    selected_model = select_final_model(
        rf_results,
        xgb_results
    )

    # --------------------------------------------------------
    # Final
    # --------------------------------------------------------

    final_result(
        selected_model
    )

    return True


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":

    success = main()

    if not success:

        raise SystemExit(1)