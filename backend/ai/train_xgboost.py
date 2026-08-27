import pandas as pd
import joblib

from pathlib import Path

from xgboost import XGBClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
)


# ============================================================
# SHADOW IT AI
# MODULE 6 - XGBOOST TRAINING
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

MODEL_PATH = (
    MODEL_DIR
    / "xgboost_model.pkl"
)


# ============================================================
# DATASET FILES
# ============================================================

X_TRAIN_PATH = (
    SPLIT_DATASET_DIR
    / "X_train.csv"
)

X_TEST_PATH = (
    SPLIT_DATASET_DIR
    / "X_test.csv"
)

Y_TRAIN_PATH = (
    SPLIT_DATASET_DIR
    / "y_train.csv"
)

Y_TEST_PATH = (
    SPLIT_DATASET_DIR
    / "y_test.csv"
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
# RISK MAPPING
# ============================================================

RISK_NAMES = {
    0: "Low",
    1: "Medium",
    2: "High",
    3: "Critical",
}


# ============================================================
# XGBOOST CONFIGURATION
# ============================================================

RANDOM_STATE = 42

N_ESTIMATORS = 300

MAX_DEPTH = 6

LEARNING_RATE = 0.05

SUBSAMPLE = 0.9

COLSAMPLE_BYTREE = 0.9


# ============================================================
# HELPER
# ============================================================

def print_section(title):

    print()
    print("=" * 70)
    print(title)
    print("=" * 70)


# ============================================================
# LOAD DATA
# ============================================================

def load_data():

    print_section(
        "1. LOADING TRAINING AND TEST DATA"
    )

    required_files = [
        X_TRAIN_PATH,
        X_TEST_PATH,
        Y_TRAIN_PATH,
        Y_TEST_PATH,
    ]

    for file_path in required_files:

        if not file_path.exists():

            print(
                "ERROR: Required file not found:"
            )

            print(file_path)

            print()
            print(
                "Run Module 4 first:"
            )

            print(
                "python ai\\split_data.py"
            )

            return None

    try:

        X_train = pd.read_csv(
            X_TRAIN_PATH
        )

        X_test = pd.read_csv(
            X_TEST_PATH
        )

        y_train = pd.read_csv(
            Y_TRAIN_PATH
        )

        y_test = pd.read_csv(
            Y_TEST_PATH
        )

    except Exception as error:

        print(
            "ERROR: Failed to load datasets."
        )

        print(
            f"Error: {error}"
        )

        return None

    # --------------------------------------------------------
    # Convert target DataFrames to Series
    # --------------------------------------------------------

    if TARGET_COLUMN in y_train.columns:

        y_train = y_train[
            TARGET_COLUMN
        ]

    else:

        y_train = y_train.iloc[:, 0]

    if TARGET_COLUMN in y_test.columns:

        y_test = y_test[
            TARGET_COLUMN
        ]

    else:

        y_test = y_test.iloc[:, 0]

    print(
        "Training and test datasets loaded successfully."
    )

    print()
    print(
        f"X_train : {X_train.shape}"
    )

    print(
        f"X_test  : {X_test.shape}"
    )

    print(
        f"y_train : {y_train.shape}"
    )

    print(
        f"y_test  : {y_test.shape}"
    )

    return (
        X_train,
        X_test,
        y_train,
        y_test
    )


# ============================================================
# VALIDATE DATA
# ============================================================

def validate_data(
    X_train,
    X_test,
    y_train,
    y_test
):

    print_section(
        "2. DATA VALIDATION"
    )

    # --------------------------------------------------------
    # Feature order
    # --------------------------------------------------------

    expected_columns = FEATURE_COLUMNS

    if list(X_train.columns) != expected_columns:

        print(
            "ERROR: X_train feature order is incorrect."
        )

        print(
            "Expected:"
        )

        print(
            expected_columns
        )

        print(
            "Received:"
        )

        print(
            list(X_train.columns)
        )

        return False

    if list(X_test.columns) != expected_columns:

        print(
            "ERROR: X_test feature order is incorrect."
        )

        return False

    print(
        "Feature order: PASS"
    )

    # --------------------------------------------------------
    # Shapes
    # --------------------------------------------------------

    if len(X_train) != len(y_train):

        print(
            "ERROR: Training feature/target size mismatch."
        )

        return False

    if len(X_test) != len(y_test):

        print(
            "ERROR: Testing feature/target size mismatch."
        )

        return False

    print(
        "Training shape: PASS"
    )

    print(
        "Testing shape: PASS"
    )

    # --------------------------------------------------------
    # Numeric validation
    # --------------------------------------------------------

    if not all(
        pd.api.types.is_numeric_dtype(
            X_train[column]
        )
        for column in FEATURE_COLUMNS
    ):

        print(
            "ERROR: Non-numeric feature found."
        )

        return False

    print(
        "Numeric features: PASS"
    )

    # --------------------------------------------------------
    # Missing values
    # --------------------------------------------------------

    if X_train.isna().any().any():

        print(
            "ERROR: Missing values in X_train."
        )

        return False

    if X_test.isna().any().any():

        print(
            "ERROR: Missing values in X_test."
        )

        return False

    if y_train.isna().any():

        print(
            "ERROR: Missing values in y_train."
        )

        return False

    if y_test.isna().any():

        print(
            "ERROR: Missing values in y_test."
        )

        return False

    print(
        "Missing values: PASS"
    )

    # --------------------------------------------------------
    # Target validation
    # --------------------------------------------------------

    valid_targets = {
        0,
        1,
        2,
        3,
    }

    train_targets = set(
        y_train.unique()
    )

    test_targets = set(
        y_test.unique()
    )

    if not train_targets.issubset(
        valid_targets
    ):

        print(
            "ERROR: Invalid training target values."
        )

        print(
            train_targets
        )

        return False

    if not test_targets.issubset(
        valid_targets
    ):

        print(
            "ERROR: Invalid testing target values."
        )

        print(
            test_targets
        )

        return False

    print(
        "Target values: PASS"
    )

    print()
    print(
        "All data validation checks passed."
    )

    return True


# ============================================================
# CLASS DISTRIBUTION
# ============================================================

def display_class_distribution(
    y,
    title
):

    print_section(title)

    distribution = (
        y.value_counts()
        .sort_index()
    )

    for risk_value in [
        0,
        1,
        2,
        3,
    ]:

        count = distribution.get(
            risk_value,
            0
        )

        risk_name = RISK_NAMES[
            risk_value
        ]

        print(
            f"{risk_value} "
            f"({risk_name:<8}) : "
            f"{count}"
        )


# ============================================================
# CREATE XGBOOST MODEL
# ============================================================

def create_model():

    print_section(
        "3. XGBOOST CONFIGURATION"
    )

    print(
        "Algorithm         : XGBoost"
    )

    print(
        f"Number of trees   : {N_ESTIMATORS}"
    )

    print(
        f"Max depth         : {MAX_DEPTH}"
    )

    print(
        f"Learning rate     : {LEARNING_RATE}"
    )

    print(
        f"Subsample         : {SUBSAMPLE}"
    )

    print(
        f"Column sampling   : {COLSAMPLE_BYTREE}"
    )

    print(
        f"Random state      : {RANDOM_STATE}"
    )

    model = XGBClassifier(
        n_estimators=N_ESTIMATORS,
        max_depth=MAX_DEPTH,
        learning_rate=LEARNING_RATE,
        subsample=SUBSAMPLE,
        colsample_bytree=COLSAMPLE_BYTREE,
        objective="multi:softprob",
        num_class=4,
        eval_metric="mlogloss",
        random_state=RANDOM_STATE,
        n_jobs=-1,
        tree_method="hist",
    )

    return model


# ============================================================
# TRAIN MODEL
# ============================================================

def train_model(
    model,
    X_train,
    y_train
):

    print_section(
        "4. TRAINING XGBOOST"
    )

    print(
        f"Training using {len(X_train)} "
        "training records..."
    )

    model.fit(
        X_train,
        y_train
    )

    print(
        "XGBoost training completed."
    )

    return model


# ============================================================
# EVALUATE MODEL
# ============================================================

def evaluate_model(
    model,
    X_test,
    y_test
):

    print_section(
        "5. XGBOOST TEST SET EVALUATION"
    )

    print(
        f"Evaluating using {len(X_test)} "
        "unseen test records..."
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

    return (
        predictions,
        accuracy,
        precision,
        recall,
        f1,
        critical_recall
    )


# ============================================================
# CONFUSION MATRIX
# ============================================================

def display_confusion_matrix(
    y_test,
    predictions
):

    print_section(
        "6. CONFUSION MATRIX"
    )

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
            f"{RISK_NAMES[index]:<10} "
            f"{row[0]:>3}  "
            f"{row[1]:>3}  "
            f"{row[2]:>4}  "
            f"{row[3]:>4}"
        )


# ============================================================
# FEATURE IMPORTANCE
# ============================================================

def display_feature_importance(
    model
):

    print_section(
        "7. XGBOOST FEATURE IMPORTANCE"
    )

    importance_df = pd.DataFrame(
        {
            "feature": FEATURE_COLUMNS,
            "importance": (
                model.feature_importances_
            )
        }
    )

    importance_df = (
        importance_df
        .sort_values(
            by="importance",
            ascending=False
        )
        .reset_index(drop=True)
    )

    print(
        importance_df.to_string(
            index=False
        )
    )

    print()
    print(
        "Feature importance shows how "
        "useful each feature was to the "
        "trained XGBoost model."
    )

    return importance_df


# ============================================================
# SAVE MODEL
# ============================================================

def save_model(model):

    print_section(
        "8. SAVING XGBOOST MODEL"
    )

    MODEL_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    try:

        joblib.dump(
            model,
            MODEL_PATH
        )

    except Exception as error:

        print(
            "ERROR: Failed to save XGBoost model."
        )

        print(
            f"Error: {error}"
        )

        return False

    print(
        "XGBoost model saved successfully."
    )

    print()
    print(
        "Model path:"
    )

    print(
        MODEL_PATH
    )

    return True


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print("#" * 70)
    print("# SHADOW IT AI")
    print("# MODULE 6 - XGBOOST TRAINING")
    print("#" * 70)

    # --------------------------------------------------------
    # Load data
    # --------------------------------------------------------

    data = load_data()

    if data is None:

        return False

    (
        X_train,
        X_test,
        y_train,
        y_test
    ) = data

    # --------------------------------------------------------
    # Validate
    # --------------------------------------------------------

    if not validate_data(
        X_train,
        X_test,
        y_train,
        y_test
    ):

        return False

    # --------------------------------------------------------
    # Display distributions
    # --------------------------------------------------------

    display_class_distribution(
        y_train,
        "TRAINING CLASS DISTRIBUTION"
    )

    display_class_distribution(
        y_test,
        "TESTING CLASS DISTRIBUTION"
    )

    # --------------------------------------------------------
    # Create model
    # --------------------------------------------------------

    model = create_model()

    # --------------------------------------------------------
    # Train
    # --------------------------------------------------------

    model = train_model(
        model,
        X_train,
        y_train
    )

    # --------------------------------------------------------
    # Evaluate
    # --------------------------------------------------------

    (
        predictions,
        accuracy,
        precision,
        recall,
        f1,
        critical_recall
    ) = evaluate_model(
        model,
        X_test,
        y_test
    )

    # --------------------------------------------------------
    # Confusion matrix
    # --------------------------------------------------------

    display_confusion_matrix(
        y_test,
        predictions
    )

    # --------------------------------------------------------
    # Feature importance
    # --------------------------------------------------------

    display_feature_importance(
        model
    )

    # --------------------------------------------------------
    # Save model
    # --------------------------------------------------------

    if not save_model(
        model
    ):

        return False

    # --------------------------------------------------------
    # Final result
    # --------------------------------------------------------

    print_section(
        "FINAL MODULE 6 RESULT"
    )

    print(
        "MODULE 6 XGBOOST COMPLETED SUCCESSFULLY"
    )

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

    print()

    print(
        "Saved model:"
    )

    print(
        MODEL_PATH
    )

    print()
    print(
        "STATUS: PASS"
    )

    return True


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":

    success = main()

    if not success:

        raise SystemExit(1)