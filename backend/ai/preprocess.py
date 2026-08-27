import pandas as pd
from pathlib import Path


# ============================================================
# MODULE 3
# SHADOW IT AI - DATA PREPROCESSING
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATASET_PATH = BASE_DIR / "dataset" / "devices.csv"

OUTPUT_PATH = BASE_DIR / "dataset" / "processed_devices.csv"


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
# AUTHORITATIVE RISK MAPPING
# ============================================================

RISK_MAPPING = {
    "Low": 0,
    "Medium": 1,
    "High": 2,
    "Critical": 3,
}


# ============================================================
# BINARY MAPPING
# ============================================================

BINARY_MAPPING = {
    "yes": 1,
    "true": 1,
    "1": 1,
    "updated": 1,

    "no": 0,
    "false": 0,
    "0": 0,
    "outdated": 0,
}


# ============================================================
# NORMALIZE BINARY VALUE
# ============================================================

def normalize_binary(value):

    if pd.isna(value):
        return None

    value = str(value).strip().lower()

    return BINARY_MAPPING.get(value)


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print("=" * 70)
    print("SHADOW IT AI")
    print("MODULE 3 - DATA PREPROCESSING")
    print("=" * 70)

    # ========================================================
    # 1. CHECK DATASET
    # ========================================================

    print()
    print("=" * 70)
    print("1. LOADING VALIDATED DATASET")
    print("=" * 70)

    if not DATASET_PATH.exists():

        print()
        print("ERROR: Dataset not found.")
        print(DATASET_PATH)

        return False

    df = pd.read_csv(DATASET_PATH)

    print()
    print("Dataset:")
    print(DATASET_PATH)

    print()
    print(f"Rows    : {len(df)}")
    print(f"Columns : {len(df.columns)}")

    # ========================================================
    # 2. CHECK INPUT COLUMNS
    # ========================================================

    print()
    print("=" * 70)
    print("2. VALIDATING INPUT COLUMNS")
    print("=" * 70)

    required_columns = FEATURE_COLUMNS + [TARGET_COLUMN]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:

        print()
        print("ERROR: Missing required columns:")

        for column in missing_columns:
            print(f"   - {column}")

        return False

    print()
    print("All required columns are present.")

    # ========================================================
    # 3. CHECK FOR OLD OS_VERSION
    # ========================================================

    print()
    print("=" * 70)
    print("3. CHECKING OS FEATURE")
    print("=" * 70)

    if "os_version" in df.columns:

        print()
        print("ERROR: 'os_version' is still present.")
        print("The final dataset must use 'os_outdated'.")

        return False

    if "os_outdated" not in df.columns:

        print()
        print("ERROR: 'os_outdated' is missing.")

        return False

    print()
    print("'os_outdated' is present.")
    print("'os_version' is not present.")

    # ========================================================
    # 4. CHECK MISSING VALUES
    # ========================================================

    print()
    print("=" * 70)
    print("4. CHECKING MISSING VALUES")
    print("=" * 70)

    missing_count = df[required_columns].isna().sum().sum()

    if missing_count > 0:

        print()
        print(
            f"ERROR: {missing_count} missing values found."
        )

        print()
        print(df[required_columns].isna().sum())

        return False

    print()
    print("No missing values found.")

    # ========================================================
    # 5. NORMALIZE BINARY FEATURES
    # ========================================================

    print()
    print("=" * 70)
    print("5. NORMALIZING BINARY FEATURES")
    print("=" * 70)

    binary_columns = [
        "unknown_device",
        "patch_status",
        "os_outdated",
        "sensitive_network_access",
    ]

    for column in binary_columns:

        print()
        print(f"Processing: {column}")

        original_values = sorted(
            df[column]
            .astype(str)
            .str.strip()
            .unique()
        )

        print(
            f"   Original values: {original_values}"
        )

        df[column] = (
            df[column]
            .apply(normalize_binary)
        )

        if df[column].isna().any():

            print()
            print(
                f"ERROR: Invalid values found in '{column}'."
            )

            return False

        df[column] = df[column].astype(int)

        print(
            f"   Converted values: "
            f"{sorted(df[column].unique())}"
        )

    print()
    print("Binary feature normalization completed.")

    # ========================================================
    # 6. VALIDATE NUMERIC FEATURES
    # ========================================================

    print()
    print("=" * 70)
    print("6. VALIDATING NUMERIC FEATURES")
    print("=" * 70)

    numeric_columns = [
        "open_port_count",
        "critical_cve_count",
    ]

    for column in numeric_columns:

        print()
        print(f"Processing: {column}")

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

        if df[column].isna().any():

            print()
            print(
                f"ERROR: Invalid numeric values in '{column}'."
            )

            return False

        if (df[column] < 0).any():

            print()
            print(
                f"ERROR: Negative values found in '{column}'."
            )

            return False

        df[column] = df[column].astype(int)

        print("   Numeric values are valid.")

    # ========================================================
    # 7. NORMALIZE RISK TARGET
    # ========================================================

    print()
    print("=" * 70)
    print("7. ENCODING RISK TARGET")
    print("=" * 70)

    print()
    print("Risk mapping:")

    for risk, number in RISK_MAPPING.items():

        print(
            f"   {risk:<10} -> {number}"
        )

    df[TARGET_COLUMN] = (
        df[TARGET_COLUMN]
        .astype(str)
        .str.strip()
    )

    invalid_risks = set(df[TARGET_COLUMN]) - set(RISK_MAPPING)

    if invalid_risks:

        print()
        print("ERROR: Invalid risk labels found:")

        for risk in sorted(invalid_risks):
            print(f"   - {risk}")

        return False

    df[TARGET_COLUMN] = (
        df[TARGET_COLUMN]
        .map(RISK_MAPPING)
        .astype(int)
    )

    print()
    print("Risk labels successfully encoded.")

    # ========================================================
    # 8. FINAL COLUMN ORDER
    # ========================================================

    print()
    print("=" * 70)
    print("8. APPLYING FINAL FEATURE ORDER")
    print("=" * 70)

    final_columns = FEATURE_COLUMNS + [TARGET_COLUMN]

    df = df[final_columns]

    print()
    print("Final ML columns:")

    for index, column in enumerate(
        df.columns,
        start=1
    ):

        print(
            f"   {index}. {column}"
        )

    # ========================================================
    # 9. DUPLICATE CHECK
    # ========================================================

    print()
    print("=" * 70)
    print("9. DUPLICATE CHECK")
    print("=" * 70)

    duplicate_count = int(
        df.duplicated().sum()
    )

    print()
    print(
        f"Duplicate rows: {duplicate_count}"
    )

    if duplicate_count > 0:

        print()
        print(
            "ERROR: Duplicate rows detected."
        )

        print(
            "The validated source dataset should contain "
            "zero duplicates."
        )

        return False

    print()
    print("No duplicate rows found.")

    # ========================================================
    # 10. FINAL DATASET SIZE
    # ========================================================

    print()
    print("=" * 70)
    print("10. FINAL DATASET SIZE CHECK")
    print("=" * 70)

    if len(df) != 1000:

        print()
        print(
            f"ERROR: Expected 1000 rows, found {len(df)}."
        )

        return False

    if len(df.columns) != 7:

        print()
        print(
            f"ERROR: Expected 7 columns, "
            f"found {len(df.columns)}."
        )

        return False

    print()
    print("Rows    : 1000")
    print("Columns : 7")

    # ========================================================
    # 11. FINAL RISK DISTRIBUTION
    # ========================================================

    print()
    print("=" * 70)
    print("11. FINAL RISK DISTRIBUTION")
    print("=" * 70)

    expected_distribution = {
        0: 250,
        1: 250,
        2: 250,
        3: 250,
    }

    actual_distribution = (
        df[TARGET_COLUMN]
        .value_counts()
        .to_dict()
    )

    risk_names = {
        0: "Low",
        1: "Medium",
        2: "High",
        3: "Critical",
    }

    distribution_ok = True

    for number in range(4):

        actual_count = actual_distribution.get(
            number,
            0
        )

        expected_count = expected_distribution[number]

        print(
            f"{risk_names[number]:<10}: "
            f"{actual_count} records"
        )

        if actual_count != expected_count:

            distribution_ok = False

    if not distribution_ok:

        print()
        print(
            "ERROR: Risk class distribution is incorrect."
        )

        return False

    print()
    print("Risk distribution is correct.")

    # ========================================================
    # 12. SAVE PROCESSED DATASET
    # ========================================================

    print()
    print("=" * 70)
    print("12. SAVING PROCESSED DATASET")
    print("=" * 70)

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        OUTPUT_PATH,
        index=False
    )

    print()
    print("Processed dataset saved:")
    print(OUTPUT_PATH)

    # ========================================================
    # 13. RELOAD AND FINAL VERIFICATION
    # ========================================================

    print()
    print("=" * 70)
    print("13. FINAL VERIFICATION")
    print("=" * 70)

    processed_df = pd.read_csv(
        OUTPUT_PATH
    )

    if len(processed_df) != 1000:

        print()
        print("ERROR: Processed dataset row count is incorrect.")

        return False

    if list(processed_df.columns) != final_columns:

        print()
        print(
            "ERROR: Processed dataset column order is incorrect."
        )

        print()
        print(
            "Expected:"
        )

        for column in final_columns:
            print(f"   - {column}")

        print()
        print(
            "Actual:"
        )

        for column in processed_df.columns:
            print(f"   - {column}")

        return False

    if processed_df.isna().any().any():

        print()
        print(
            "ERROR: Missing values exist in processed dataset."
        )

        return False

    if processed_df.duplicated().any():

        print()
        print(
            "ERROR: Duplicate rows exist in processed dataset."
        )

        return False

    # Check all ML columns are numeric

    for column in FEATURE_COLUMNS + [TARGET_COLUMN]:

        if not pd.api.types.is_numeric_dtype(
            processed_df[column]
        ):

            print()
            print(
                f"ERROR: '{column}' is not numeric."
            )

            return False

    print()
    print("Processed dataset verification passed.")

    # ========================================================
    # 14. SUCCESS
    # ========================================================

    print()
    print("=" * 70)
    print("MODULE 3 PREPROCESSING COMPLETED SUCCESSFULLY")
    print("=" * 70)

    print()
    print("Output:")
    print(OUTPUT_PATH)

    print()
    print("Final shape:")
    print(
        f"Rows    : {len(processed_df)}"
    )
    print(
        f"Columns : {len(processed_df.columns)}"
    )

    print()
    print("Final features:")

    for index, column in enumerate(
        FEATURE_COLUMNS,
        start=1
    ):

        print(
            f"   {index}. {column}"
        )

    print()
    print("Risk mapping:")

    for risk, number in RISK_MAPPING.items():

        print(
            f"   {risk:<10} -> {number}"
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