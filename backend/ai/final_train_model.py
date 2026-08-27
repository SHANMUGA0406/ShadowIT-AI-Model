from pathlib import Path
import json

import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder


# ============================================================
# MODULE 10
# SHADOW IT — FINAL MODEL TRAINING
# ============================================================


# ============================================================
# PROJECT PATHS
# ============================================================

BACKEND_DIR = Path(__file__).resolve().parent.parent

AI_DIR = BACKEND_DIR / "ai"

DATASET_DIR = BACKEND_DIR / "dataset"

MODELS_DIR = AI_DIR / "models"

DATASET_PATH = DATASET_DIR / "devices.csv"

MODELS_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# AUTHORITATIVE FEATURES
# ============================================================

FEATURES = [
    "unknown_device",
    "open_port_count",
    "critical_cve_count",
    "patch_status",
    "os_outdated",
    "sensitive_network_access"
]

TARGET = "risk"


# ============================================================
# EXPECTED RISK ORDER
# ============================================================

RISK_ORDER = [
    "Low",
    "Medium",
    "High",
    "Critical"
]


# ============================================================
# HELPER — NORMALIZE BINARY VALUES
# ============================================================

def normalize_binary_column(
    df,
    column
):

    print()
    print(f"Normalizing column: {column}")

    if column not in df.columns:

        raise ValueError(
            f"Required column '{column}' is missing."
        )

    normalized_values = []

    for value in df[column]:

        # ----------------------------------------------------
        # Handle missing values
        # ----------------------------------------------------

        if pd.isna(value):

            raise ValueError(
                f"Missing value found in column '{column}'."
            )

        # ----------------------------------------------------
        # Boolean
        # ----------------------------------------------------

        if isinstance(value, bool):

            normalized_values.append(
                int(value)
            )

            continue

        # ----------------------------------------------------
        # Numeric
        # ----------------------------------------------------

        if isinstance(
            value,
            (int, float)
        ):

            if value in [0, 1]:

                normalized_values.append(
                    int(value)
                )

                continue

            raise ValueError(
                f"Invalid numeric value '{value}' "
                f"found in column '{column}'. "
                f"Expected 0 or 1."
            )

        # ----------------------------------------------------
        # String
        # ----------------------------------------------------

        text = str(value).strip().lower()

        # Yes / True
        if text in [
            "yes",
            "true",
            "y",
            "1"
        ]:

            normalized_values.append(1)

        # No / False
        elif text in [
            "no",
            "false",
            "n",
            "0"
        ]:

            normalized_values.append(0)

        # Updated / Current
        elif column == "patch_status" and text in [
            "updated",
            "up-to-date",
            "up to date",
            "current",
            "patched"
        ]:

            normalized_values.append(1)

        # Outdated / Unpatched
        elif column == "patch_status" and text in [
            "outdated",
            "old",
            "unpatched",
            "not patched",
            "vulnerable"
        ]:

            normalized_values.append(0)

        else:

            raise ValueError(
                f"Invalid value '{value}' found "
                f"in column '{column}'."
            )

    df[column] = normalized_values

    print(
        f"   Unique values: "
        f"{sorted(df[column].unique().tolist())}"
    )

    return df


# ============================================================
# HELPER — CREATE OS_OUTDATED
# ============================================================

def create_os_outdated(df):

    print()
    print("=" * 70)
    print("2. STANDARDIZING OS FEATURE")
    print("=" * 70)

    # --------------------------------------------------------
    # Already available
    # --------------------------------------------------------

    if "os_outdated" in df.columns:

        print(
            "✅ 'os_outdated' already exists."
        )

        return df

    # --------------------------------------------------------
    # Create from os_version
    # --------------------------------------------------------

    if "os_version" not in df.columns:

        raise ValueError(
            "Neither 'os_outdated' nor "
            "'os_version' exists in the dataset."
        )

    print(
        "⚠️ 'os_outdated' not found."
    )

    print(
        "Creating 'os_outdated' "
        "from 'os_version'..."
    )

    def determine_os_status(value):

        if pd.isna(value):

            raise ValueError(
                "Missing OS version found."
            )

        text = str(value).strip().lower()

        # ----------------------------------------------------
        # Explicit outdated operating systems
        # ----------------------------------------------------

        outdated_keywords = [
            "windows 7",
            "windows7",
            "windows vista",
            "windows xp",
            "windows xp",
            "windows 8",
            "windows server 2008",
            "windows server 2012",
            "ubuntu 16",
            "ubuntu 18",
            "centos 7",
            "debian 9",
            "debian 10",
            "old",
            "outdated",
            "legacy"
        ]

        for keyword in outdated_keywords:

            if keyword in text:

                return 1

        # ----------------------------------------------------
        # Current/newer operating systems
        # ----------------------------------------------------

        current_keywords = [
            "windows 10",
            "windows 11",
            "windows server 2019",
            "windows server 2022",
            "ubuntu 20",
            "ubuntu 22",
            "ubuntu 24",
            "debian 11",
            "debian 12",
            "centos stream",
            "fedora",
            "macos",
            "linux"
        ]

        for keyword in current_keywords:

            if keyword in text:

                return 0

        # ----------------------------------------------------
        # Unknown OS
        # ----------------------------------------------------
        # We conservatively treat unknown OS information
        # as outdated for cybersecurity risk modeling.

        return 1

    df["os_outdated"] = df[
        "os_version"
    ].apply(
        determine_os_status
    )

    print()
    print(
        "os_outdated values:"
    )

    print(
        df["os_outdated"].value_counts()
    )

    return df


# ============================================================
# MAIN
# ============================================================

print()
print("#" * 70)
print("# SHADOW IT — MODULE 10")
print("# FINAL MODEL TRAINING")
print("#" * 70)


# ============================================================
# 1. LOAD DATASET
# ============================================================

print()
print("=" * 70)
print("1. LOADING FINAL TRAINING DATASET")
print("=" * 70)

if not DATASET_PATH.exists():

    print(
        "❌ Dataset not found:"
    )

    print(
        DATASET_PATH
    )

    raise SystemExit(1)


df = pd.read_csv(
    DATASET_PATH
)


print(
    "Dataset loaded successfully."
)

print(
    f"Dataset path : {DATASET_PATH}"
)

print(
    f"Rows         : {len(df)}"
)

print(
    f"Columns      : {len(df.columns)}"
)


# ============================================================
# 2. STANDARDIZE OS FEATURE
# ============================================================

df = create_os_outdated(
    df
)


# ============================================================
# 3. VALIDATE REQUIRED COLUMNS
# ============================================================

print()
print("=" * 70)
print("3. VALIDATING FINAL TRAINING FEATURES")
print("=" * 70)

required_columns = FEATURES + [
    TARGET
]

missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]

if missing_columns:

    print(
        "❌ Required columns are missing:"
    )

    for column in missing_columns:

        print(
            f"   - {column}"
        )

    raise SystemExit(1)


print(
    "✅ All required columns are available."
)


# ============================================================
# 4. NORMALIZE BINARY FEATURES
# ============================================================

print()
print("=" * 70)
print("4. NORMALIZING BINARY FEATURES")
print("=" * 70)

binary_features = [
    "unknown_device",
    "patch_status",
    "os_outdated",
    "sensitive_network_access"
]

try:

    for feature in binary_features:

        df = normalize_binary_column(
            df,
            feature
        )

except Exception as error:

    print()
    print(
        "❌ Feature normalization failed."
    )

    print(
        f"Error: {error}"
    )

    raise SystemExit(1)


print()
print(
    "✅ Binary feature normalization completed."
)


# ============================================================
# 5. NORMALIZE NUMERIC FEATURES
# ============================================================

print()
print("=" * 70)
print("5. VALIDATING NUMERIC FEATURES")
print("=" * 70)

numeric_features = [
    "open_port_count",
    "critical_cve_count"
]

for feature in numeric_features:

    df[feature] = pd.to_numeric(
        df[feature],
        errors="coerce"
    )

    if df[feature].isna().any():

        print(
            f"❌ Invalid numeric values "
            f"found in '{feature}'."
        )

        raise SystemExit(1)

    if (df[feature] < 0).any():

        print(
            f"❌ Negative values found "
            f"in '{feature}'."
        )

        raise SystemExit(1)


print(
    "✅ Numeric features validated."
)


# ============================================================
# 6. VALIDATE TARGET
# ============================================================

print()
print("=" * 70)
print("6. VALIDATING RISK TARGET")
print("=" * 70)

df[TARGET] = (
    df[TARGET]
    .astype(str)
    .str.strip()
    .str.title()
)

invalid_risks = sorted(
    set(df[TARGET])
    - set(RISK_ORDER)
)

if invalid_risks:

    print(
        "❌ Invalid risk labels found:"
    )

    for value in invalid_risks:

        print(
            f"   - {value}"
        )

    print()
    print(
        "Expected labels:"
    )

    for value in RISK_ORDER:

        print(
            f"   - {value}"
        )

    raise SystemExit(1)


print(
    "✅ Risk labels are valid."
)


# ============================================================
# 7. DISPLAY CLASS DISTRIBUTION
# ============================================================

print()
print("=" * 70)
print("7. RISK CLASS DISTRIBUTION")
print("=" * 70)

distribution = (
    df[TARGET]
    .value_counts()
    .reindex(
        RISK_ORDER,
        fill_value=0
    )
)

for label, count in distribution.items():

    print(
        f"   {label:<10}: {count}"
    )


# ============================================================
# 8. PREPARE X AND Y
# ============================================================

print()
print("=" * 70)
print("8. PREPARING FINAL TRAINING DATA")
print("=" * 70)

X = df[
    FEATURES
].copy()

y = df[
    TARGET
].copy()


print(
    f"Feature matrix shape: {X.shape}"
)

print(
    f"Target shape        : {y.shape}"
)


# ============================================================
# 9. CREATE AUTHORITATIVE LABEL ENCODING
# ============================================================

print()
print("=" * 70)
print("9. CREATING RISK LABEL ENCODING")
print("=" * 70)

label_encoder = LabelEncoder()

# Fit using the authoritative risk order.
# LabelEncoder itself sorts alphabetically, so we explicitly
# create the required mapping afterwards.

label_encoder.fit(
    RISK_ORDER
)

risk_mapping = {
    "Low": 0,
    "Medium": 1,
    "High": 2,
    "Critical": 3
}

reverse_mapping = {
    str(value): key
    for key, value
    in risk_mapping.items()
}


y_encoded = y.map(
    risk_mapping
)

if y_encoded.isna().any():

    print(
        "❌ Target encoding failed."
    )

    raise SystemExit(1)


y_encoded = y_encoded.astype(int)


print()
print(
    "Authoritative risk mapping:"
)

for label in RISK_ORDER:

    print(
        f"   {label:<10} -> "
        f"{risk_mapping[label]}"
    )


# ============================================================
# 10. TRAIN FINAL RANDOM FOREST
# ============================================================

print()
print("=" * 70)
print("10. TRAINING FINAL RANDOM FOREST MODEL")
print("=" * 70)

print(
    "Training using the complete finalized dataset..."
)

model = RandomForestClassifier(
    n_estimators=300,
    random_state=42,
    class_weight="balanced",
    min_samples_leaf=2,
    n_jobs=-1
)

model.fit(
    X,
    y_encoded
)


print(
    "✅ Final Random Forest training completed."
)


# ============================================================
# 11. SAVE FINAL CANDIDATE MODEL
# ============================================================

print()
print("=" * 70)
print("11. SAVING MODULE 10 OUTPUTS")
print("=" * 70)

MODEL_OUTPUT = (
    MODELS_DIR
    / "final_candidate_model.pkl"
)

LABEL_ENCODER_OUTPUT = (
    MODELS_DIR
    / "final_label_encoder.pkl"
)

FEATURES_OUTPUT = (
    MODELS_DIR
    / "final_features.json"
)

LABEL_MAPPING_OUTPUT = (
    MODELS_DIR
    / "final_label_mapping.json"
)


joblib.dump(
    model,
    MODEL_OUTPUT
)


joblib.dump(
    label_encoder,
    LABEL_ENCODER_OUTPUT
)


with open(
    FEATURES_OUTPUT,
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        {
            "features": FEATURES,
            "target": TARGET,
            "feature_count": len(FEATURES)
        },
        file,
        indent=4
    )


with open(
    LABEL_MAPPING_OUTPUT,
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        {
            "risk_mapping": risk_mapping,
            "reverse_mapping": reverse_mapping
        },
        file,
        indent=4
    )


# ============================================================
# 12. FINAL VERIFICATION
# ============================================================

print()
print("=" * 70)
print("12. FINAL OUTPUT VERIFICATION")
print("=" * 70)

output_files = [
    MODEL_OUTPUT,
    LABEL_ENCODER_OUTPUT,
    FEATURES_OUTPUT,
    LABEL_MAPPING_OUTPUT
]

all_outputs_exist = True

for output_file in output_files:

    if output_file.exists():

        print(
            f"✅ {output_file.name}"
        )

    else:

        print(
            f"❌ {output_file.name}"
        )

        all_outputs_exist = False


# ============================================================
# FINAL RESULT
# ============================================================

print()
print("=" * 70)

if all_outputs_exist:

    print(
        "✅ MODULE 10 COMPLETED SUCCESSFULLY"
    )

    print()
    print(
        "Final model:"
    )

    print(
        f"   {MODEL_OUTPUT}"
    )

    print()
    print(
        "Next module:"
    )

    print(
        "   MODULE 11 — Model Saving"
    )

else:

    print(
        "❌ MODULE 10 FAILED"
    )

print(
    "=" * 70
)