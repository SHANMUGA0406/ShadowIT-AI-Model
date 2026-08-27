import pandas as pd
from pathlib import Path


# ============================================================
# CONFIGURATION
# ============================================================

DATASET_PATH = Path(__file__).resolve().parent / "devices.csv"

REQUIRED_COLUMNS = [
    "unknown_device",
    "open_port_count",
    "critical_cve_count",
    "patch_status",
    "os_outdated",
    "sensitive_network_access",
    "risk",
]

ALLOWED_UNKNOWN_DEVICE = {"Yes", "No"}
ALLOWED_PATCH_STATUS = {"Updated", "Outdated"}
ALLOWED_SENSITIVE_ACCESS = {"Yes", "No"}
ALLOWED_OS_OUTDATED = {0, 1}
ALLOWED_RISK = {"Low", "Medium", "High", "Critical"}

NUMERIC_COLUMNS = [
    "open_port_count",
    "critical_cve_count",
    "os_outdated",
]


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def print_section(title):
    """Print a formatted section heading."""
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def validate_required_columns(df):
    """Check whether all required columns exist."""

    print_section("1. COLUMN VALIDATION")

    missing_columns = [
        column for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        print("❌ Missing columns:")
        for column in missing_columns:
            print(f"   - {column}")

        return False

    print("✅ All required columns are present.")

    extra_columns = [
        column for column in df.columns
        if column not in REQUIRED_COLUMNS
    ]

    if extra_columns:
        print("\n⚠️ Extra columns detected:")
        for column in extra_columns:
            print(f"   - {column}")

    return True


def validate_missing_values(df):
    """Check for missing/null values."""

    print_section("2. MISSING VALUE VALIDATION")

    missing = df[REQUIRED_COLUMNS].isnull().sum()

    total_missing = missing.sum()

    if total_missing == 0:
        print("✅ No missing values found.")
        return True

    print("❌ Missing values detected:")

    for column, count in missing.items():
        if count > 0:
            print(f"   - {column}: {count}")

    return False


def validate_duplicates(df):
    """Check for duplicate rows."""

    print_section("3. DUPLICATE VALIDATION")

    duplicate_count = df.duplicated().sum()

    print(f"Total duplicate rows: {duplicate_count}")

    if duplicate_count == 0:
        print("✅ No duplicate rows found.")
        return True

    print("⚠️ Duplicate rows detected.")

    return False


def validate_numeric_columns(df):
    """Validate numeric feature columns."""

    print_section("4. NUMERIC FEATURE VALIDATION")

    validation_passed = True

    for column in NUMERIC_COLUMNS:

        numeric_values = pd.to_numeric(
            df[column],
            errors="coerce"
        )

        invalid_type_count = numeric_values.isnull().sum()

        if invalid_type_count > 0:

            print(
                f"❌ {column}: "
                f"{invalid_type_count} non-numeric value(s)"
            )

            validation_passed = False

        else:
            print(f"✅ {column}: numeric values are valid.")

        negative_count = (numeric_values < 0).sum()

        if negative_count > 0:

            print(
                f"❌ {column}: "
                f"{negative_count} negative value(s)"
            )

            validation_passed = False

    return validation_passed


def validate_categorical_columns(df):
    """Validate categorical feature values."""

    print_section("5. CATEGORICAL FEATURE VALIDATION")

    validation_passed = True

    # --------------------------------------------------------
    # unknown_device
    # --------------------------------------------------------

    unknown_values = set(
        df["unknown_device"]
        .dropna()
        .astype(str)
        .str.strip()
    )

    invalid_unknown = unknown_values - ALLOWED_UNKNOWN_DEVICE

    if invalid_unknown:
        print(
            "❌ unknown_device contains invalid values:"
        )

        for value in invalid_unknown:
            print(f"   - {value}")

        validation_passed = False

    else:
        print("✅ unknown_device values are valid.")

    # --------------------------------------------------------
    # patch_status
    # --------------------------------------------------------

    patch_values = set(
        df["patch_status"]
        .dropna()
        .astype(str)
        .str.strip()
    )

    invalid_patch = patch_values - ALLOWED_PATCH_STATUS

    if invalid_patch:
        print(
            "❌ patch_status contains invalid values:"
        )

        for value in invalid_patch:
            print(f"   - {value}")

        validation_passed = False

    else:
        print("✅ patch_status values are valid.")

    # --------------------------------------------------------
    # sensitive_network_access
    # --------------------------------------------------------

    sensitive_values = set(
        df["sensitive_network_access"]
        .dropna()
        .astype(str)
        .str.strip()
    )

    invalid_sensitive = (
        sensitive_values - ALLOWED_SENSITIVE_ACCESS
    )

    if invalid_sensitive:
        print(
            "❌ sensitive_network_access "
            "contains invalid values:"
        )

        for value in invalid_sensitive:
            print(f"   - {value}")

        validation_passed = False

    else:
        print(
            "✅ sensitive_network_access "
            "values are valid."
        )

    # --------------------------------------------------------
    # os_outdated
    # --------------------------------------------------------

    os_values = set(
        pd.to_numeric(
            df["os_outdated"],
            errors="coerce"
        )
        .dropna()
        .astype(int)
    )

    invalid_os = os_values - ALLOWED_OS_OUTDATED

    if invalid_os:
        print(
            "❌ os_outdated contains invalid values:"
        )

        for value in invalid_os:
            print(f"   - {value}")

        validation_passed = False

    else:
        print("✅ os_outdated values are valid.")

    return validation_passed


def validate_risk_labels(df):
    """Validate target risk labels."""

    print_section("6. RISK LABEL VALIDATION")

    risk_values = set(
        df["risk"]
        .dropna()
        .astype(str)
        .str.strip()
    )

    invalid_risk = risk_values - ALLOWED_RISK

    if invalid_risk:

        print("❌ Invalid risk labels detected:")

        for value in invalid_risk:
            print(f"   - {value}")

        return False

    print("✅ All risk labels are valid.")

    return True


def display_class_distribution(df):
    """Display distribution of risk classes."""

    print_section("7. RISK CLASS DISTRIBUTION")

    distribution = df["risk"].value_counts()

    for risk in ["Low", "Medium", "High", "Critical"]:

        count = distribution.get(risk, 0)

        percentage = (
            count / len(df) * 100
            if len(df) > 0
            else 0
        )

        print(
            f"{risk:<10} : "
            f"{count:>5} records "
            f"({percentage:.2f}%)"
        )


def display_dataset_summary(df):
    """Display general dataset information."""

    print_section("8. DATASET SUMMARY")

    print(f"Dataset path : {DATASET_PATH}")
    print(f"Rows         : {len(df)}")
    print(f"Columns      : {len(df.columns)}")

    print("\nColumn names:")

    for column in df.columns:
        print(f"   - {column}")


# ============================================================
# MAIN VALIDATION FUNCTION
# ============================================================

def validate_dataset():

    print("\n" + "#" * 60)
    print("# SHADOW IT DATASET VALIDATION")
    print("#" * 60)

    # --------------------------------------------------------
    # Check dataset existence
    # --------------------------------------------------------

    if not DATASET_PATH.exists():

        print(
            f"\n❌ Dataset not found:\n"
            f"{DATASET_PATH}"
        )

        return False

    print(
        f"\nDataset found:\n"
        f"{DATASET_PATH}"
    )

    # --------------------------------------------------------
    # Load dataset
    # --------------------------------------------------------

    try:

        df = pd.read_csv(DATASET_PATH)

    except Exception as error:

        print(
            "\n❌ Failed to read dataset."
        )

        print(f"Error: {error}")

        return False

    # --------------------------------------------------------
    # Basic check
    # --------------------------------------------------------

    if df.empty:

        print("\n❌ Dataset is empty.")

        return False

    display_dataset_summary(df)

    # --------------------------------------------------------
    # Run validations
    # --------------------------------------------------------

    results = []

    results.append(
        validate_required_columns(df)
    )

    # If required columns are missing, stop further
    # column-dependent validation.

    if not results[0]:

        print_section("FINAL VALIDATION RESULT")

        print(
            "❌ Dataset validation failed "
            "because required columns are missing."
        )

        return False

    results.append(
        validate_missing_values(df)
    )

    results.append(
        validate_duplicates(df)
    )

    results.append(
        validate_numeric_columns(df)
    )

    results.append(
        validate_categorical_columns(df)
    )

    results.append(
        validate_risk_labels(df)
    )

    display_class_distribution(df)

    # --------------------------------------------------------
    # Final result
    # --------------------------------------------------------

    print_section("FINAL VALIDATION RESULT")

    if all(results):

        print(
            "✅ DATASET VALIDATION PASSED"
        )

        print(
            "\nThe dataset is structurally valid "
            "for the next ML stage."
        )

        return True

    else:

        print(
            "❌ DATASET VALIDATION FAILED"
        )

        print(
            "\nFix the reported issues before "
            "continuing to Module 3."
        )

        return False


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":

    success = validate_dataset()

    if not success:
        raise SystemExit(1)