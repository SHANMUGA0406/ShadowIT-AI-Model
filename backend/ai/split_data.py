import pandas as pd
from pathlib import Path

from sklearn.model_selection import train_test_split


# ============================================================
# MODULE 4
# SHADOW IT AI - TRAIN / TEST SPLIT
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_PATH = (
    BASE_DIR
    / "dataset"
    / "processed_devices.csv"
)

OUTPUT_DIR = (
    BASE_DIR
    / "dataset"
    / "split"
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

TARGET_COLUMN = "risk"


# ============================================================
# SPLIT CONFIGURATION
# ============================================================

TEST_SIZE = 0.20

RANDOM_STATE = 42


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
# LOAD DATASET
# ============================================================

def load_dataset():

    print_section("1. LOADING PROCESSED DATASET")

    if not INPUT_PATH.exists():

        print()
        print("ERROR: Processed dataset not found:")
        print(INPUT_PATH)

        print()
        print("Run Module 3 first:")
        print("python ai\\preprocess.py")

        return None

    try:

        df = pd.read_csv(INPUT_PATH)

    except Exception as error:

        print()
        print("ERROR: Failed to load dataset.")
        print(f"Error: {error}")

        return None

    print()
    print("Processed dataset loaded successfully.")

    print()
    print(f"Dataset path : {INPUT_PATH}")
    print(f"Rows         : {len(df)}")
    print(f"Columns      : {len(df.columns)}")

    return df


# ============================================================
# VALIDATE DATASET
# ============================================================

def validate_dataset(df):

    print_section("2. DATASET VALIDATION")

    required_columns = (
        FEATURE_COLUMNS
        + [TARGET_COLUMN]
    )

    # --------------------------------------------------------
    # Column validation
    # --------------------------------------------------------

    if list(df.columns) != required_columns:

        print()
        print("ERROR: Column order does not match.")

        print()
        print("Expected:")

        for index, column in enumerate(
            required_columns,
            start=1
        ):

            print(
                f"   {index}. {column}"
            )

        print()
        print("Actual:")

        for index, column in enumerate(
            df.columns,
            start=1
        ):

            print(
                f"   {index}. {column}"
            )

        return False

    print()
    print("Column order is correct.")

    # --------------------------------------------------------
    # Row count
    # --------------------------------------------------------

    if len(df) != 1000:

        print()
        print(
            f"ERROR: Expected 1000 rows, found {len(df)}."
        )

        return False

    print("Row count: 1000")

    # --------------------------------------------------------
    # Missing values
    # --------------------------------------------------------

    if df.isna().any().any():

        print()
        print("ERROR: Missing values found.")

        print(
            df.isna().sum()
        )

        return False

    print("Missing values: 0")

    # --------------------------------------------------------
    # Duplicate rows
    # --------------------------------------------------------

    duplicate_count = int(
        df.duplicated().sum()
    )

    if duplicate_count != 0:

        print()
        print(
            f"ERROR: {duplicate_count} duplicate rows found."
        )

        return False

    print("Duplicate rows: 0")

    # --------------------------------------------------------
    # Target validation
    # --------------------------------------------------------

    valid_risk_values = {
        0,
        1,
        2,
        3,
    }

    actual_risk_values = set(
        df[TARGET_COLUMN].unique()
    )

    if actual_risk_values != valid_risk_values:

        print()
        print(
            "ERROR: Invalid risk values found."
        )

        print(
            f"Expected: {sorted(valid_risk_values)}"
        )

        print(
            f"Actual: {sorted(actual_risk_values)}"
        )

        return False

    print("Risk values: 0, 1, 2, 3")

    # --------------------------------------------------------
    # Feature numeric validation
    # --------------------------------------------------------

    for column in FEATURE_COLUMNS:

        if not pd.api.types.is_numeric_dtype(
            df[column]
        ):

            print()
            print(
                f"ERROR: Feature '{column}' is not numeric."
            )

            return False

    print("All features are numeric.")

    print()
    print("Dataset validation passed.")

    return True


# ============================================================
# DISPLAY DISTRIBUTION
# ============================================================

def display_distribution(y, title):

    print_section(title)

    counts = (
        y.value_counts()
        .sort_index()
    )

    total = len(y)

    for risk_value in [
        0,
        1,
        2,
        3,
    ]:

        count = int(
            counts.get(
                risk_value,
                0
            )
        )

        percentage = (
            count / total * 100
            if total > 0
            else 0
        )

        print(
            f"{RISK_NAMES[risk_value]:<10}: "
            f"{count:>3} records "
            f"({percentage:>6.2f}%)"
        )


# ============================================================
# CREATE OUTPUT DIRECTORY
# ============================================================

def create_output_directory():

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    print()
    print(
        "Split output directory:"
    )

    print(
        OUTPUT_DIR
    )


# ============================================================
# SAVE DATASETS
# ============================================================

def save_datasets(
    X_train,
    X_test,
    y_train,
    y_test
):

    print_section("6. SAVING TRAIN / TEST DATA")

    try:

        X_train.to_csv(
            OUTPUT_DIR / "X_train.csv",
            index=False
        )

        X_test.to_csv(
            OUTPUT_DIR / "X_test.csv",
            index=False
        )

        y_train.to_csv(
            OUTPUT_DIR / "y_train.csv",
            index=False
        )

        y_test.to_csv(
            OUTPUT_DIR / "y_test.csv",
            index=False
        )

    except Exception as error:

        print()
        print("ERROR: Failed to save split datasets.")
        print(f"Error: {error}")

        return False

    print()
    print("X_train.csv saved.")
    print("X_test.csv saved.")
    print("y_train.csv saved.")
    print("y_test.csv saved.")

    return True


# ============================================================
# FINAL SPLIT VERIFICATION
# ============================================================

def verify_split(
    X_train,
    X_test,
    y_train,
    y_test
):

    print_section("9. FINAL SPLIT VERIFICATION")

    # --------------------------------------------------------
    # Shape validation
    # --------------------------------------------------------

    if len(X_train) != 800:

        print(
            f"ERROR: Expected 800 training rows, "
            f"found {len(X_train)}."
        )

        return False

    if len(X_test) != 200:

        print(
            f"ERROR: Expected 200 testing rows, "
            f"found {len(X_test)}."
        )

        return False

    if len(y_train) != 800:

        print(
            f"ERROR: Expected 800 training targets, "
            f"found {len(y_train)}."
        )

        return False

    if len(y_test) != 200:

        print(
            f"ERROR: Expected 200 testing targets, "
            f"found {len(y_test)}."
        )

        return False

    print()
    print("Training records : 800")
    print("Testing records  : 200")

    # --------------------------------------------------------
    # Feature columns
    # --------------------------------------------------------

    if list(X_train.columns) != FEATURE_COLUMNS:

        print()
        print(
            "ERROR: X_train feature order is incorrect."
        )

        return False

    if list(X_test.columns) != FEATURE_COLUMNS:

        print()
        print(
            "ERROR: X_test feature order is incorrect."
        )

        return False

    print()
    print("Feature order is correct.")

    # --------------------------------------------------------
    # Class distributions
    # --------------------------------------------------------

    train_counts = (
        y_train.value_counts()
        .sort_index()
        .to_dict()
    )

    test_counts = (
        y_test.value_counts()
        .sort_index()
        .to_dict()
    )

    expected_train = {
        0: 200,
        1: 200,
        2: 200,
        3: 200,
    }

    expected_test = {
        0: 50,
        1: 50,
        2: 50,
        3: 50,
    }

    if train_counts != expected_train:

        print()
        print(
            "ERROR: Training class distribution is incorrect."
        )

        print(
            f"Expected: {expected_train}"
        )

        print(
            f"Actual: {train_counts}"
        )

        return False

    if test_counts != expected_test:

        print()
        print(
            "ERROR: Testing class distribution is incorrect."
        )

        print(
            f"Expected: {expected_test}"
        )

        print(
            f"Actual: {test_counts}"
        )

        return False

    print()
    print("Training distribution: 200 / 200 / 200 / 200")
    print("Testing distribution : 50 / 50 / 50 / 50")

    # --------------------------------------------------------
    # Final
    # --------------------------------------------------------

    print()
    print("All split verification checks passed.")

    return True


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print("#" * 70)
    print("# SHADOW IT AI")
    print("# MODULE 4 - TRAIN / TEST SPLIT")
    print("#" * 70)

    # --------------------------------------------------------
    # 1. Load
    # --------------------------------------------------------

    df = load_dataset()

    if df is None:

        return False

    # --------------------------------------------------------
    # 2. Validate
    # --------------------------------------------------------

    if not validate_dataset(df):

        return False

    # --------------------------------------------------------
    # 3. Separate X and y
    # --------------------------------------------------------

    print_section(
        "3. SEPARATING FEATURES AND TARGET"
    )

    X = df[
        FEATURE_COLUMNS
    ].copy()

    y = df[
        TARGET_COLUMN
    ].copy()

    print()
    print(
        f"X shape: {X.shape}"
    )

    print(
        f"y shape: {y.shape}"
    )

    print()
    print("Features:")

    for index, feature in enumerate(
        FEATURE_COLUMNS,
        start=1
    ):

        print(
            f"   {index}. {feature}"
        )

    print()
    print(
        f"Target: {TARGET_COLUMN}"
    )

    # --------------------------------------------------------
    # 4. Original distribution
    # --------------------------------------------------------

    display_distribution(
        y,
        "4. ORIGINAL CLASS DISTRIBUTION"
    )

    # --------------------------------------------------------
    # 5. Train/test split
    # --------------------------------------------------------

    print_section(
        "5. CREATING STRATIFIED TRAIN / TEST SPLIT"
    )

    print()
    print("Test size    : 20%")
    print("Train size   : 80%")
    print("Random state : 42")
    print("Stratify     : Enabled")

    try:

        (
            X_train,
            X_test,
            y_train,
            y_test
        ) = train_test_split(
            X,
            y,
            test_size=TEST_SIZE,
            random_state=RANDOM_STATE,
            stratify=y
        )

    except Exception as error:

        print()
        print("ERROR: Train/test split failed.")
        print(f"Error: {error}")

        return False

    print()
    print("Train/test split created successfully.")

    # --------------------------------------------------------
    # 6. Shapes
    # --------------------------------------------------------

    print_section(
        "6. SPLIT SHAPES"
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

    # --------------------------------------------------------
    # 7. Training distribution
    # --------------------------------------------------------

    display_distribution(
        y_train,
        "7. TRAINING CLASS DISTRIBUTION"
    )

    # --------------------------------------------------------
    # 8. Testing distribution
    # --------------------------------------------------------

    display_distribution(
        y_test,
        "8. TESTING CLASS DISTRIBUTION"
    )

    # --------------------------------------------------------
    # 9. Output directory
    # --------------------------------------------------------

    create_output_directory()

    # --------------------------------------------------------
    # 10. Save
    # --------------------------------------------------------

    if not save_datasets(
        X_train,
        X_test,
        y_train,
        y_test
    ):

        return False

    # --------------------------------------------------------
    # 11. Verify
    # --------------------------------------------------------

    if not verify_split(
        X_train,
        X_test,
        y_train,
        y_test
    ):

        return False

    # --------------------------------------------------------
    # SUCCESS
    # --------------------------------------------------------

    print()
    print("#" * 70)
    print("# MODULE 4 TRAIN / TEST SPLIT COMPLETED SUCCESSFULLY")
    print("#" * 70)

    print()
    print("Output files:")

    print(
        f"   {OUTPUT_DIR / 'X_train.csv'}"
    )

    print(
        f"   {OUTPUT_DIR / 'X_test.csv'}"
    )

    print(
        f"   {OUTPUT_DIR / 'y_train.csv'}"
    )

    print(
        f"   {OUTPUT_DIR / 'y_test.csv'}"
    )

    print()
    print("STATUS: PASS")

    return True


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":

    success = main()

    if not success:

        raise SystemExit(1)