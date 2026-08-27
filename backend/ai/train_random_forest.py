import pandas as pd
import joblib

from pathlib import Path

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
)


# ============================================================
# MODULE 5
# RANDOM FOREST TRAINING
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

SPLIT_DATASET_DIR = BASE_DIR / "dataset" / "split"

MODEL_DIR = BASE_DIR / "ai" / "models"

MODEL_PATH = MODEL_DIR / "random_forest_model.pkl"


# ============================================================
# DATA FILES
# ============================================================

X_TRAIN_PATH = SPLIT_DATASET_DIR / "X_train.csv"
X_TEST_PATH = SPLIT_DATASET_DIR / "X_test.csv"

Y_TRAIN_PATH = SPLIT_DATASET_DIR / "y_train.csv"
Y_TEST_PATH = SPLIT_DATASET_DIR / "y_test.csv"


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
# RANDOM FOREST CONFIGURATION
# ============================================================

RANDOM_STATE = 42
N_ESTIMATORS = 300
MAX_DEPTH = None
MIN_SAMPLES_SPLIT = 2
MIN_SAMPLES_LEAF = 1
CLASS_WEIGHT = "balanced"


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

        y_train_df = pd.read_csv(
            Y_TRAIN_PATH
        )

        y_test_df = pd.read_csv(
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

    # y_train.csv

    if TARGET_COLUMN in y_train_df.columns:

        y_train = y_train_df[
            TARGET_COLUMN
        ]

    else:

        y_train = y_train_df.iloc[:, 0]

    # y_test.csv

    if TARGET_COLUMN in y_test_df.columns:

        y_test = y_test_df[
            TARGET_COLUMN
        ]

    else:

        y_test = y_test_df.iloc[:, 0]

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

    if list(X_train.columns) != FEATURE_COLUMNS:

        print(
            "ERROR: X_train feature order is incorrect."
        )

        print()
        print(
            "Expected:"
        )

        for feature in FEATURE_COLUMNS:

            print(
                f"   - {feature}"
            )

        print()
        print(
            "Received:"
        )

        for feature in X_train.columns:

            print(
                f"   - {feature}"
            )

        return False

    if list(X_test.columns) != FEATURE_COLUMNS:

        print(
            "ERROR: X_test feature order is incorrect."
        )

        print()
        print(
            "Expected:"
        )

        for feature in FEATURE_COLUMNS:

            print(
                f"   - {feature}"
            )

        print()
        print(
            "Received:"
        )

        for feature in X_test.columns:

            print(
                f"   - {feature}"
            )

        return False

    print(
        "Feature order: PASS"
    )

    # --------------------------------------------------------
    # Shape validation
    # --------------------------------------------------------

    if len(X_train) != len(y_train):

        print(
            "ERROR: X_train and y_train sizes do not match."
        )

        return False

    if len(X_test) != len(y_test):

        print(
            "ERROR: X_test and y_test sizes do not match."
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

    for column in FEATURE_COLUMNS:

        if not pd.api.types.is_numeric_dtype(
            X_train[column]
        ):

            print(
                f"ERROR: Training feature "
                f"'{column}' is not numeric."
            )

            return False

        if not pd.api.types.is_numeric_dtype(
            X_test[column]
        ):

            print(
                f"ERROR: Testing feature "
                f"'{column}' is not numeric."
            )

            return False

    print(
        "Numeric features: PASS"
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

    # --------------------------------------------------------
    # Missing values
    # --------------------------------------------------------

    if X_train.isna().sum().sum() > 0:

        print(
            "ERROR: Missing values found in X_train."
        )

        return False

    if X_test.isna().sum().sum() > 0:

        print(
            "ERROR: Missing values found in X_test."
        )

        return False

    if y_train.isna().sum() > 0:

        print(
            "ERROR: Missing values found in y_train."
        )

        return False

    if y_test.isna().sum() > 0:

        print(
            "ERROR: Missing values found in y_test."
        )

        return False

    print(
        "Missing values: PASS"
    )

    print()
    print(
        "All data validation checks passed."
    )

    return True


# ============================================================
# DISPLAY CLASS DISTRIBUTION
# ============================================================

def display_distribution(
    y,
    title
):

    print_section(title)

    distribution = (
        y.value_counts()
        .sort_index()
    )

    for class_value in [
        0,
        1,
        2,
        3,
    ]:

        count = distribution.get(
            class_value,
            0
        )

        print(
            f"{class_value} "
            f"({RISK_NAMES[class_value]})"
            f" : {count}"
        )


# ============================================================
# CREATE RANDOM FOREST
# ============================================================

def create_model():

    print_section(
        "3. RANDOM FOREST CONFIGURATION"
    )

    print(
        "Algorithm         : Random Forest"
    )

    print(
        f"Number of trees   : {N_ESTIMATORS}"
    )

    print(
        f"Max depth         : {MAX_DEPTH}"
    )

    print(
        f"Min samples split : {MIN_SAMPLES_SPLIT}"
    )

    print(
        f"Min samples leaf  : {MIN_SAMPLES_LEAF}"
    )

    print(
        f"Class weight      : {CLASS_WEIGHT}"
    )

    print(
        f"Random state      : {RANDOM_STATE}"
    )

    model = RandomForestClassifier(
        n_estimators=N_ESTIMATORS,
        max_depth=MAX_DEPTH,
        min_samples_split=MIN_SAMPLES_SPLIT,
        min_samples_leaf=MIN_SAMPLES_LEAF,
        class_weight=CLASS_WEIGHT,
        random_state=RANDOM_STATE,
        n_jobs=-1,
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
        "4. TRAINING RANDOM FOREST"
    )

    print(
        "Training using 800 training records..."
    )

    model.fit(
        X_train,
        y_train
    )

    print(
        "Random Forest training completed."
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
        "5. RANDOM FOREST TEST SET EVALUATION"
    )

    print(
        "Evaluating using 200 unseen test records..."
    )

    y_pred = model.predict(
        X_test
    )

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

    critical_recall = recall_score(
        y_test,
        y_pred,
        labels=[3],
        average=None,
        zero_division=0
    )[0]

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
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "critical_recall": critical_recall,
    }


# ============================================================
# CONFUSION MATRIX
# ============================================================

def display_confusion_matrix(
    model,
    X_test,
    y_test
):

    print_section(
        "6. CONFUSION MATRIX"
    )

    y_pred = model.predict(
        X_test
    )

    matrix = confusion_matrix(
        y_test,
        y_pred,
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

    for index, row in enumerate(
        matrix
    ):

        print(
            f"{RISK_NAMES[index]:<10}"
            f"{row[0]:>5}"
            f"{row[1]:>5}"
            f"{row[2]:>6}"
            f"{row[3]:>6}"
        )


# ============================================================
# FEATURE IMPORTANCE
# ============================================================

def display_feature_importance(
    model
):

    print_section(
        "7. RANDOM FOREST FEATURE IMPORTANCE"
    )

    importance_df = pd.DataFrame(
        {
            "feature": FEATURE_COLUMNS,
            "importance": (
                model.feature_importances_
            ),
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
        "Feature importance shows how useful "
        "each feature was for Random Forest splits."
    )


# ============================================================
# SAVE MODEL
# ============================================================

def save_model(
    model
):

    print_section(
        "8. SAVING RANDOM FOREST MODEL"
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
            "ERROR: Failed to save model."
        )

        print(
            f"Error: {error}"
        )

        return False

    print(
        "Random Forest model saved successfully."
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
    print("# MODULE 5 - RANDOM FOREST TRAINING")
    print("#" * 70)

    # --------------------------------------------------------
    # Load
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
    # Distribution
    # --------------------------------------------------------

    display_distribution(
        y_train,
        "TRAINING CLASS DISTRIBUTION"
    )

    display_distribution(
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
    # Model information
    # --------------------------------------------------------

    print_section(
        "TRAINED MODEL INFORMATION"
    )

    print(
        f"Number of trees : {model.n_estimators}"
    )

    print(
        f"Number of classes : {len(model.classes_)}"
    )

    print()
    print(
        "Classes:"
    )

    for class_value in model.classes_:

        print(
            f"   {class_value} "
            f"-> {RISK_NAMES[class_value]}"
        )

    # --------------------------------------------------------
    # Evaluation
    # --------------------------------------------------------

    metrics = evaluate_model(
        model,
        X_test,
        y_test
    )

    # --------------------------------------------------------
    # Confusion matrix
    # --------------------------------------------------------

    display_confusion_matrix(
        model,
        X_test,
        y_test
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
        "FINAL MODULE 5 RESULT"
    )

    print(
        "MODULE 5 RANDOM FOREST COMPLETED SUCCESSFULLY"
    )

    print()
    print(
        f"Accuracy        : "
        f"{metrics['accuracy']:.4f}"
    )

    print(
        f"Precision       : "
        f"{metrics['precision']:.4f}"
    )

    print(
        f"Recall          : "
        f"{metrics['recall']:.4f}"
    )

    print(
        f"F1 Score        : "
        f"{metrics['f1']:.4f}"
    )

    print(
        f"Critical Recall : "
        f"{metrics['critical_recall']:.4f}"
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