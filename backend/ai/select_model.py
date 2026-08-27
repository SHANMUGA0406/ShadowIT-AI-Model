import pandas as pd
import joblib

from pathlib import Path

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)


# ============================================================
# MODULE 8
# SHADOW IT AI MODEL SELECTION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent


# ============================================================
# PATH CONFIGURATION
# ============================================================

SPLIT_DIR = (
    BASE_DIR
    / "dataset"
    / "split"
)

MODEL_DIR = (
    BASE_DIR
    / "ai"
    / "models"
)


X_TEST_PATH = (
    SPLIT_DIR
    / "X_test.csv"
)

Y_TEST_PATH = (
    SPLIT_DIR
    / "y_test.csv"
)


RANDOM_FOREST_PATH = (
    MODEL_DIR
    / "random_forest_model.pkl"
)

XGBOOST_PATH = (
    MODEL_DIR
    / "xgboost_model.pkl"
)


# ============================================================
# FEATURE CONFIGURATION
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
# MODEL NAMES
# ============================================================

RANDOM_FOREST = "Random Forest"

XGBOOST = "XGBoost"


# ============================================================
# RISK LABELS
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
        "1. LOADING TEST DATA"
    )

    if not X_TEST_PATH.exists():

        print(
            "ERROR: X_test.csv not found."
        )

        print(
            X_TEST_PATH
        )

        return None, None

    if not Y_TEST_PATH.exists():

        print(
            "ERROR: y_test.csv not found."
        )

        print(
            Y_TEST_PATH
        )

        return None, None

    try:

        X_test = pd.read_csv(
            X_TEST_PATH
        )

        y_test = pd.read_csv(
            Y_TEST_PATH
        )

    except Exception as error:

        print(
            "ERROR: Failed to load test data."
        )

        print(
            f"Error: {error}"
        )

        return None, None

    # --------------------------------------------------------
    # Convert y_test to Series
    # --------------------------------------------------------

    if TARGET_COLUMN in y_test.columns:

        y_test = y_test[
            TARGET_COLUMN
        ]

    else:

        y_test = y_test.iloc[:, 0]

    print(
        "Test dataset loaded successfully."
    )

    print()
    print(
        f"X_test : {X_test.shape}"
    )

    print(
        f"y_test : {y_test.shape}"
    )

    return X_test, y_test


# ============================================================
# VALIDATE TEST DATA
# ============================================================

def validate_test_data(
    X_test,
    y_test
):

    print_section(
        "2. TEST DATA VALIDATION"
    )

    # --------------------------------------------------------
    # Feature order
    # --------------------------------------------------------

    if list(X_test.columns) != FEATURE_COLUMNS:

        print(
            "ERROR: Feature order mismatch."
        )

        print()
        print(
            "Expected:"
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
            "Received:"
        )

        for index, feature in enumerate(
            X_test.columns,
            start=1
        ):

            print(
                f"   {index}. {feature}"
            )

        return False

    print(
        "Feature order: PASS"
    )

    # --------------------------------------------------------
    # Shape
    # --------------------------------------------------------

    if len(X_test) != len(y_test):

        print(
            "ERROR: X_test and y_test size mismatch."
        )

        return False

    print(
        "Test shape: PASS"
    )

    # --------------------------------------------------------
    # Missing values
    # --------------------------------------------------------

    if X_test.isnull().any().any():

        print(
            "ERROR: Missing values found in X_test."
        )

        return False

    if y_test.isnull().any():

        print(
            "ERROR: Missing values found in y_test."
        )

        return False

    print(
        "Missing values: PASS"
    )

    # --------------------------------------------------------
    # Numeric features
    # --------------------------------------------------------

    for feature in FEATURE_COLUMNS:

        if not pd.api.types.is_numeric_dtype(
            X_test[feature]
        ):

            print(
                f"ERROR: Feature is not numeric: {feature}"
            )

            return False

    print(
        "Numeric features: PASS"
    )

    # --------------------------------------------------------
    # Target values
    # --------------------------------------------------------

    valid_targets = {
        0,
        1,
        2,
        3
    }

    actual_targets = set(
        y_test.unique()
    )

    if not actual_targets.issubset(
        valid_targets
    ):

        print(
            "ERROR: Invalid target values."
        )

        print(
            actual_targets
        )

        return False

    print(
        "Target values: PASS"
    )

    print()
    print(
        "All test data validation checks passed."
    )

    return True


# ============================================================
# LOAD MODEL
# ============================================================

def load_model(
    model_path,
    model_name
):

    print()
    print(
        f"Loading {model_name}..."
    )

    if not model_path.exists():

        print(
            f"ERROR: {model_name} model not found."
        )

        print(
            model_path
        )

        return None

    try:

        model = joblib.load(
            model_path
        )

    except Exception as error:

        print(
            f"ERROR: Could not load {model_name}."
        )

        print(
            f"Error: {error}"
        )

        return None

    print(
        f"{model_name} loaded successfully."
    )

    return model


# ============================================================
# EVALUATE MODEL
# ============================================================

def evaluate_model(
    model,
    model_name,
    X_test,
    y_test
):

    print_section(
        f"3. EVALUATING {model_name.upper()}"
    )

    print(
        f"Running predictions for "
        f"{len(X_test)} test records..."
    )

    # --------------------------------------------------------
    # Predictions
    # --------------------------------------------------------

    y_pred = model.predict(
        X_test
    )

    # --------------------------------------------------------
    # Metrics
    # --------------------------------------------------------

    accuracy = accuracy_score(
        y_test,
        y_pred
    )

    precision = precision_score(
        y_test,
        y_pred,
        average="weighted",
        zero_division=0
    )

    recall = recall_score(
        y_test,
        y_pred,
        average="weighted",
        zero_division=0
    )

    f1 = f1_score(
        y_test,
        y_pred,
        average="weighted",
        zero_division=0
    )

    # --------------------------------------------------------
    # Critical Recall
    # --------------------------------------------------------

    critical_recall_values = recall_score(
        y_test,
        y_pred,
        labels=[3],
        average=None,
        zero_division=0
    )

    if len(critical_recall_values) > 0:

        critical_recall = (
            critical_recall_values[0]
        )

    else:

        critical_recall = 0.0

    # --------------------------------------------------------
    # Display
    # --------------------------------------------------------

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
    }


# ============================================================
# MODEL SELECTION
# ============================================================

def select_best_model(
    rf_results,
    xgb_results
):

    print_section(
        "4. MODEL SELECTION"
    )

    print(
        "Selection priority:"
    )

    print(
        "   1. Critical Recall"
    )

    print(
        "   2. F1 Score"
    )

    print(
        "   3. Recall"
    )

    print(
        "   4. Accuracy"
    )

    print()
    print(
        "Comparing models..."
    )

    # --------------------------------------------------------
    # Create comparable tuples
    # --------------------------------------------------------

    rf_score = (
        rf_results["critical_recall"],
        rf_results["f1"],
        rf_results["recall"],
        rf_results["accuracy"],
    )

    xgb_score = (
        xgb_results["critical_recall"],
        xgb_results["f1"],
        xgb_results["recall"],
        xgb_results["accuracy"],
    )

    print()
    print(
        "Random Forest selection score:"
    )

    print(
        f"   Critical Recall : "
        f"{rf_score[0]:.4f}"
    )

    print(
        f"   F1 Score        : "
        f"{rf_score[1]:.4f}"
    )

    print(
        f"   Recall          : "
        f"{rf_score[2]:.4f}"
    )

    print(
        f"   Accuracy        : "
        f"{rf_score[3]:.4f}"
    )

    print()
    print(
        "XGBoost selection score:"
    )

    print(
        f"   Critical Recall : "
        f"{xgb_score[0]:.4f}"
    )

    print(
        f"   F1 Score        : "
        f"{xgb_score[1]:.4f}"
    )

    print(
        f"   Recall          : "
        f"{xgb_score[2]:.4f}"
    )

    print(
        f"   Accuracy        : "
        f"{xgb_score[3]:.4f}"
    )

    # --------------------------------------------------------
    # Select winner
    # --------------------------------------------------------

    if xgb_score > rf_score:

        selected_model = XGBOOST

    elif rf_score > xgb_score:

        selected_model = RANDOM_FOREST

    else:

        # Complete tie
        selected_model = XGBOOST

    print_section(
        "🏆 SELECTED FINAL MODEL"
    )

    print(
        f"Selected model: {selected_model}"
    )

    if selected_model == XGBOOST:

        print()
        print(
            "XGBoost was selected because it achieved "
            "the stronger overall priority score."
        )

    else:

        print()
        print(
            "Random Forest was selected because it achieved "
            "the stronger overall priority score."
        )

    return selected_model


# ============================================================
# SAVE SELECTION INFORMATION
# ============================================================

def save_selection_info(
    selected_model,
    rf_results,
    xgb_results
):

    print_section(
        "5. SAVING MODEL SELECTION RESULT"
    )

    MODEL_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    selection_data = {
        "selected_model": selected_model,
        "selection_priority": [
            "critical_recall",
            "f1",
            "recall",
            "accuracy"
        ],
        "random_forest": {
            "accuracy": rf_results["accuracy"],
            "precision": rf_results["precision"],
            "recall": rf_results["recall"],
            "f1": rf_results["f1"],
            "critical_recall":
                rf_results["critical_recall"],
        },
        "xgboost": {
            "accuracy": xgb_results["accuracy"],
            "precision": xgb_results["precision"],
            "recall": xgb_results["recall"],
            "f1": xgb_results["f1"],
            "critical_recall":
                xgb_results["critical_recall"],
        }
    }

    output_path = (
        MODEL_DIR
        / "model_selection.csv"
    )

    try:

        rows = []

        for result in [
            rf_results,
            xgb_results
        ]:

            rows.append({
                "model": result["model"],
                "accuracy": result["accuracy"],
                "precision": result["precision"],
                "recall": result["recall"],
                "f1": result["f1"],
                "critical_recall":
                    result["critical_recall"],
                "selected":
                    result["model"] == selected_model
            })

        df = pd.DataFrame(
            rows
        )

        df.to_csv(
            output_path,
            index=False
        )

    except Exception as error:

        print(
            "ERROR: Failed to save selection result."
        )

        print(
            f"Error: {error}"
        )

        return False

    print(
        "Model selection result saved."
    )

    print(
        f"Path: {output_path}"
    )

    return True


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print("#" * 70)
    print("# SHADOW IT AI")
    print("# MODULE 8 - MODEL SELECTION")
    print("#" * 70)

    # --------------------------------------------------------
    # Load test data
    # --------------------------------------------------------

    X_test, y_test = load_test_data()

    if X_test is None:

        return False

    # --------------------------------------------------------
    # Validate
    # --------------------------------------------------------

    if not validate_test_data(
        X_test,
        y_test
    ):

        return False

    # --------------------------------------------------------
    # Load Random Forest
    # --------------------------------------------------------

    random_forest = load_model(
        RANDOM_FOREST_PATH,
        RANDOM_FOREST
    )

    if random_forest is None:

        return False

    # --------------------------------------------------------
    # Load XGBoost
    # --------------------------------------------------------

    xgboost = load_model(
        XGBOOST_PATH,
        XGBOOST
    )

    if xgboost is None:

        return False

    # --------------------------------------------------------
    # Evaluate Random Forest
    # --------------------------------------------------------

    rf_results = evaluate_model(
        random_forest,
        RANDOM_FOREST,
        X_test,
        y_test
    )

    # --------------------------------------------------------
    # Evaluate XGBoost
    # --------------------------------------------------------

    xgb_results = evaluate_model(
        xgboost,
        XGBOOST,
        X_test,
        y_test
    )

    # --------------------------------------------------------
    # Select
    # --------------------------------------------------------

    selected_model = select_best_model(
        rf_results,
        xgb_results
    )

    # --------------------------------------------------------
    # Save selection
    # --------------------------------------------------------

    if not save_selection_info(
        selected_model,
        rf_results,
        xgb_results
    ):

        return False

    # --------------------------------------------------------
    # Final result
    # --------------------------------------------------------

    print_section(
        "FINAL MODULE 8 RESULT"
    )

    print(
        "MODULE 8 MODEL SELECTION COMPLETED SUCCESSFULLY"
    )

    print()
    print(
        f"FINAL SELECTED MODEL: {selected_model}"
    )

    print()
    print(
        "Selection priority:"
    )

    print(
        "   1. Critical Recall"
    )

    print(
        "   2. F1 Score"
    )

    print(
        "   3. Recall"
    )

    print(
        "   4. Accuracy"
    )

    print()
    print(
        "Model selection record:"
    )

    print(
        MODEL_DIR
        / "model_selection.csv"
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
        "Module 9 - Final Model Creation"
    )

    return True


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":

    success = main()

    if not success:

        raise SystemExit(1)