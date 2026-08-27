import pandas as pd
from pathlib import Path


# ============================================================
# PATH CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_PATH = (
    BASE_DIR
    / "dataset"
    / "processed_devices.csv"
)

OUTPUT_PATH = (
    BASE_DIR
    / "dataset"
    / "features.csv"
)


# ============================================================
# FINAL FEATURE CONFIGURATION
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

RISK_MAPPING = {
    "Low": 0,
    "Medium": 1,
    "High": 2,
    "Critical": 3,
}


# ============================================================
# HELPER
# ============================================================

def print_section(title):

    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


# ============================================================
# LOAD DATASET
# ============================================================

def load_dataset():

    print_section(
        "1. LOADING PROCESSED DATASET"
    )

    if not INPUT_PATH.exists():

        print(
            "❌ Processed dataset not found:"
        )

        print(INPUT_PATH)

        print(
            "\nRun Module 3 first:"
        )

        print(
            "python ai\\preprocess.py"
        )

        return None

    try:

        df = pd.read_csv(INPUT_PATH)

    except Exception as error:

        print(
            "❌ Failed to load processed dataset."
        )

        print(
            f"Error: {error}"
        )

        return None

    print(
        "Dataset loaded successfully."
    )

    print(
        f"Rows    : {df.shape[0]}"
    )

    print(
        f"Columns : {df.shape[1]}"
    )

    return df


# ============================================================
# VALIDATE COLUMNS
# ============================================================

def validate_columns(df):

    print_section(
        "2. FEATURE COLUMN VALIDATION"
    )

    required_columns = (
        FEATURE_COLUMNS
        + [TARGET_COLUMN]
    )

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:

        print(
            "❌ Missing required columns:"
        )

        for column in missing_columns:

            print(
                f"   - {column}"
            )

        return False

    print(
        "✅ All required feature and target columns exist."
    )

    return True


# ============================================================
# SELECT FINAL FEATURES
# ============================================================

def select_features(df):

    print_section(
        "3. SELECTING FINAL FEATURES"
    )

    print(
        "Final feature set:"
    )

    for index, feature in enumerate(
        FEATURE_COLUMNS,
        start=1
    ):

        print(
            f"   {index}. {feature}"
        )

    print(
        f"\nTarget: {TARGET_COLUMN}"
    )

    selected_columns = (
        FEATURE_COLUMNS
        + [TARGET_COLUMN]
    )

    return df[selected_columns].copy()


# ============================================================
# VALIDATE FEATURE DATA TYPES
# ============================================================

def validate_feature_types(df):

    print_section(
        "4. DATA TYPE VALIDATION"
    )

    success = True

    # --------------------------------------------------------
    # Validate features
    # --------------------------------------------------------

    for feature in FEATURE_COLUMNS:

        if not pd.api.types.is_numeric_dtype(
            df[feature]
        ):

            print(
                f"❌ {feature} is not numeric."
            )

            success = False

        else:

            print(
                f"✅ {feature} is numeric."
            )

    # --------------------------------------------------------
    # Risk is intentionally categorical
    # --------------------------------------------------------

    print(
        "\nRisk target:"
    )

    print(
        "   risk contains categorical labels:"
    )

    print(
        "   Low, Medium, High, Critical"
    )

    print(
        "   These will be converted to numeric labels."
    )

    return success


# ============================================================
# ENCODE RISK TARGET
# ============================================================

def encode_target(df):

    print_section(
        "5. ENCODING RISK TARGET"
    )

    print(
        "Authoritative risk mapping:"
    )

    for risk_name, risk_value in RISK_MAPPING.items():

        print(
            f"   {risk_name:<10} -> {risk_value}"
        )

    # --------------------------------------------------------
    # Validate risk labels
    # --------------------------------------------------------

    invalid_labels = set(
        df[TARGET_COLUMN].dropna().unique()
    ) - set(
        RISK_MAPPING.keys()
    )

    if invalid_labels:

        print(
            "\n❌ Invalid risk labels found:"
        )

        for label in invalid_labels:

            print(
                f"   - {label}"
            )

        return None

    # --------------------------------------------------------
    # Convert labels to numeric values
    # --------------------------------------------------------

    df[TARGET_COLUMN] = (
        df[TARGET_COLUMN]
        .map(RISK_MAPPING)
        .astype(int)
    )

    print(
        "\n✅ Risk labels successfully encoded."
    )

    print(
        "\nEncoded risk distribution:"
    )

    distribution = (
        df[TARGET_COLUMN]
        .value_counts()
        .sort_index()
    )

    risk_names = {
        0: "Low",
        1: "Medium",
        2: "High",
        3: "Critical",
    }

    for risk_value in [0, 1, 2, 3]:

        count = distribution.get(
            risk_value,
            0
        )

        print(
            f"   {risk_value} "
            f"({risk_names[risk_value]}): "
            f"{count}"
        )

    return df


# ============================================================
# FINAL NUMERIC VALIDATION
# ============================================================

def validate_final_dataset(df):

    print_section(
        "6. FINAL NUMERIC VALIDATION"
    )

    numeric_columns = (
        FEATURE_COLUMNS
        + [TARGET_COLUMN]
    )

    success = True

    for column in numeric_columns:

        if not pd.api.types.is_numeric_dtype(
            df[column]
        ):

            print(
                f"❌ {column} is not numeric."
            )

            success = False

        else:

            print(
                f"✅ {column} is numeric."
            )

    if not success:

        return False

    # --------------------------------------------------------
    # Check missing values
    # --------------------------------------------------------

    missing_values = (
        df[numeric_columns]
        .isnull()
        .sum()
    )

    total_missing = (
        missing_values.sum()
    )

    if total_missing > 0:

        print(
            "\n❌ Missing values detected:"
        )

        print(
            missing_values[
                missing_values > 0
            ]
        )

        return False

    print(
        "\n✅ No missing values detected."
    )

    return True


# ============================================================
# SAVE FEATURE DATASET
# ============================================================

def save_features(df):

    print_section(
        "7. SAVING FEATURE DATASET"
    )

    try:

        df.to_csv(
            OUTPUT_PATH,
            index=False
        )

    except Exception as error:

        print(
            "❌ Failed to save feature dataset."
        )

        print(
            f"Error: {error}"
        )

        return False

    print(
        "✅ Feature dataset saved:"
    )

    print(
        OUTPUT_PATH
    )

    return True


# ============================================================
# FINAL VERIFICATION
# ============================================================

def final_verification(df):

    print_section(
        "8. FINAL VERIFICATION"
    )

    print(
        f"Rows    : {df.shape[0]}"
    )

    print(
        f"Columns : {df.shape[1]}"
    )

    print(
        "\nFinal columns:"
    )

    for index, column in enumerate(
        df.columns,
        start=1
    ):

        print(
            f"   {index}. {column}"
        )

    print(
        "\nFinal dataset preview:"
    )

    print(
        df.head().to_string(
            index=False
        )
    )

    print(
        "\nRisk distribution:"
    )

    risk_names = {
        0: "Low",
        1: "Medium",
        2: "High",
        3: "Critical",
    }

    distribution = (
        df[TARGET_COLUMN]
        .value_counts()
        .sort_index()
    )

    for risk_value in [0, 1, 2, 3]:

        count = distribution.get(
            risk_value,
            0
        )

        print(
            f"   {risk_names[risk_value]:<10}: "
            f"{count}"
        )


# ============================================================
# MAIN
# ============================================================

def main():

    print("\n" + "#" * 60)
    print("# SHADOW IT FEATURE ENGINEERING")
    print("#" * 60)

    # --------------------------------------------------------
    # 1. Load
    # --------------------------------------------------------

    df = load_dataset()

    if df is None:

        return False

    # --------------------------------------------------------
    # 2. Validate columns
    # --------------------------------------------------------

    if not validate_columns(df):

        return False

    # --------------------------------------------------------
    # 3. Select features
    # --------------------------------------------------------

    df = select_features(df)

    # --------------------------------------------------------
    # 4. Validate feature types
    # --------------------------------------------------------

    if not validate_feature_types(df):

        return False

    # --------------------------------------------------------
    # 5. Encode target
    # --------------------------------------------------------

    df = encode_target(df)

    if df is None:

        return False

    # --------------------------------------------------------
    # 6. Final validation
    # --------------------------------------------------------

    if not validate_final_dataset(df):

        return False

    # --------------------------------------------------------
    # 7. Save
    # --------------------------------------------------------

    if not save_features(df):

        return False

    # --------------------------------------------------------
    # 8. Verification
    # --------------------------------------------------------

    final_verification(df)

    print_section(
        "MODULE 4 COMPLETED SUCCESSFULLY"
    )

    print(
        "\n✅ Feature engineering completed."
    )

    print(
        "\nFeature dataset:"
    )

    print(
        OUTPUT_PATH
    )

    print(
        "\nNext module:"
    )

    print(
        "python ai\\split_data.py"
    )

    return True


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":

    success = main()

    if not success:

        raise SystemExit(1)