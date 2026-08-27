import pandas as pd
import joblib

from pathlib import Path

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)


# ============================================================
# MODULE 7
# SHADOW IT AI MODEL EVALUATION
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

        print(
            "\nRun:"
        )

        print(
            "python ai\\split_data.py"
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
    # Convert y_test DataFrame to Series
    # --------------------------------------------------------

    if TARGET_COLUMN in y_test.columns:

        y_test = y_test[
            TARGET_COLUMN
        ]

    else:

        y_test = y_test.iloc[:, 0]

    print(
        "Test data loaded successfully."
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

        print(
            "\nExpected:"
        )

        for index, feature in enumerate(
            FEATURE_COLUMNS,
            start=1
        ):

            print(
                f"   {index}. {feature}"
            )

        print(
            "\nReceived:"
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

    if not all(
        pd.api.types.is_numeric_dtype(
            X_test[column]
        )
        for column in FEATURE_COLUMNS
    ):

        print(
            "ERROR: Non-numeric feature detected."
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
            f"ERROR: {model_name} model not found:"
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
            f"ERROR: Failed to load {model_name}."
        )

        print(
            f"Error: {error}"
        )

        return None

    print(
        f"{model_name} loaded successfully."
    )

    print(
        f"Model path: {model_path}"
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
        f"3. {model_name.upper()} EVALUATION"
    )

    print(
        f"Evaluating {model_name} "
        f"using {len(X_test)} unseen test records..."
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

    critical_recall = recall_score(
        y_test,
        y_pred,
        labels=[3],
        average=None,
        zero_division=0
    )[0]

    # --------------------------------------------------------
    # Display metrics
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

    # --------------------------------------------------------
    # Confusion matrix
    # --------------------------------------------------------

    cm = confusion_matrix(
        y_test,
        y_pred,
        labels=[
            0,
            1,
            2,
            3
        ]
    )

    print_section(
        f"{model_name.upper()} CONFUSION MATRIX"
    )

    print(
        "Rows    = Actual"
    )

    print(
        "Columns = Predicted"
    )

    print()

    print(
        "             Low  Med  High  Crit"
    )

    for index, row in enumerate(cm):

        print(
            f"{RISK_NAMES[index]:<10}"
            f"{row[0]:>5}"
            f"{row[1]:>5}"
            f"{row[2]:>6}"
            f"{row[3]:>6}"
        )

    # --------------------------------------------------------
    # Classification report
    # --------------------------------------------------------

    print_section(
        f"{model_name.upper()} CLASSIFICATION REPORT"
    )

    report = classification_report(
        y_test,
        y_pred,
        labels=[
            0,
            1,
            2,
            3
        ],
        target_names=[
            "Low",
            "Medium",
            "High",
            "Critical"
        ],
        zero_division=0
    )

    print(
        report
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
# COMPARE MODELS
# ============================================================

def compare_models(
    rf_results,
    xgb_results
):

    print_section(
        "4. MODEL PERFORMANCE COMPARISON"
    )

    print(
        f"{'Metric':<20}"
        f"{'Random Forest':>18}"
        f"{'XGBoost':>15}"
    )

    print(
        "-" * 53
    )

    print(
        f"{'Accuracy':<20}"
        f"{rf_results['accuracy']:>18.4f}"
        f"{xgb_results['accuracy']:>15.4f}"
    )

    print(
        f"{'Precision':<20}"
        f"{rf_results['precision']:>18.4f}"
        f"{xgb_results['precision']:>15.4f}"
    )

    print(
        f"{'Recall':<20}"
        f"{rf_results['recall']:>18.4f}"
        f"{xgb_results['recall']:>15.4f}"
    )

    print(
        f"{'F1 Score':<20}"
        f"{rf_results['f1']:>18.4f}"
        f"{xgb_results['f1']:>15.4f}"
    )

    print(
        f"{'Critical Recall':<20}"
        f"{rf_results['critical_recall']:>18.4f}"
        f"{xgb_results['critical_recall']:>15.4f}"
    )

    # --------------------------------------------------------
    # Best model by Critical Recall
    # --------------------------------------------------------

    print()
    print(
        "Primary metric: Critical Recall"
    )

    if (
        xgb_results["critical_recall"]
        >
        rf_results["critical_recall"]
    ):

        print(
            "Current best model by Critical Recall: XGBoost"
        )

    elif (
        rf_results["critical_recall"]
        >
        xgb_results["critical_recall"]
    ):

        print(
            "Current best model by Critical Recall: Random Forest"
        )

    else:

        print(
            "Critical Recall is equal for both models."
        )

    # --------------------------------------------------------
    # Best F1
    # --------------------------------------------------------

    if (
        xgb_results["f1"]
        >
        rf_results["f1"]
    ):

        print(
            "Best F1 Score: XGBoost"
        )

    elif (
        rf_results["f1"]
        >
        xgb_results["f1"]
    ):

        print(
            "Best F1 Score: Random Forest"
        )

    else:

        print(
            "F1 Score is equal for both models."
        )


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print("#" * 70)
    print("# SHADOW IT AI")
    print("# MODULE 7 - MODEL EVALUATION")
    print("#" * 70)

    # --------------------------------------------------------
    # Load test data
    # --------------------------------------------------------

    X_test, y_test = load_test_data()

    if X_test is None:

        return False

    # --------------------------------------------------------
    # Validate test data
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
        "Random Forest"
    )

    if random_forest is None:

        return False

    # --------------------------------------------------------
    # Load XGBoost
    # --------------------------------------------------------

    xgboost = load_model(
        XGBOOST_PATH,
        "XGBoost"
    )

    if xgboost is None:

        return False

    # --------------------------------------------------------
    # Evaluate Random Forest
    # --------------------------------------------------------

    rf_results = evaluate_model(
        random_forest,
        "Random Forest",
        X_test,
        y_test
    )

    # --------------------------------------------------------
    # Evaluate XGBoost
    # --------------------------------------------------------

    xgb_results = evaluate_model(
        xgboost,
        "XGBoost",
        X_test,
        y_test
    )

    # --------------------------------------------------------
    # Compare
    # --------------------------------------------------------

    compare_models(
        rf_results,
        xgb_results
    )

    # --------------------------------------------------------
    # Final result
    # --------------------------------------------------------

    print_section(
        "FINAL MODULE 7 RESULT"
    )

    print(
        "MODULE 7 MODEL EVALUATION COMPLETED SUCCESSFULLY"
    )

    print()
    print(
        "Both models were evaluated using the same"
    )

    print(
        "unseen test dataset."
    )

    print()
    print(
        "Random Forest:"
    )

    print(
        f"   Accuracy        : "
        f"{rf_results['accuracy']:.4f}"
    )

    print(
        f"   F1 Score        : "
        f"{rf_results['f1']:.4f}"
    )

    print(
        f"   Critical Recall : "
        f"{rf_results['critical_recall']:.4f}"
    )

    print()
    print(
        "XGBoost:"
    )

    print(
        f"   Accuracy        : "
        f"{xgb_results['accuracy']:.4f}"
    )

    print(
        f"   F1 Score        : "
        f"{xgb_results['f1']:.4f}"
    )

    print(
        f"   Critical Recall : "
        f"{xgb_results['critical_recall']:.4f}"
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
        "Module 8 - Model Selection"
    )

    return True


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":

    success = main()

    if not success:

        raise SystemExit(1)