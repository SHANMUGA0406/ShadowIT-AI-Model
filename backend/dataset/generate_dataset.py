# ============================================================
# SHADOW IT AI
# MODULE 1 - DATASET GENERATION
# ============================================================

import random
from pathlib import Path

import pandas as pd


# ============================================================
# CONFIGURATION
# ============================================================

TOTAL_ROWS = 1000
ROWS_PER_CLASS = 250
RANDOM_STATE = 42

random.seed(RANDOM_STATE)


# ============================================================
# PROJECT PATH
# ============================================================

BACKEND_DIR = Path(__file__).resolve().parent.parent
DATASET_DIR = BACKEND_DIR / "dataset"
OUTPUT_FILE = DATASET_DIR / "devices.csv"


# ============================================================
# FINAL COLUMNS
# ============================================================

FINAL_COLUMNS = [
    "unknown_device",
    "open_port_count",
    "critical_cve_count",
    "patch_status",
    "os_outdated",
    "sensitive_network_access",
    "risk"
]


RISK_LEVELS = [
    "Low",
    "Medium",
    "High",
    "Critical"
]


# ============================================================
# GENERATE ONE ROW
# ============================================================

def generate_row(risk):

    if risk == "Low":

        unknown_device = random.choices(
            ["No", "Yes"],
            weights=[85, 15]
        )[0]

        open_port_count = random.randint(0, 8)

        critical_cve_count = random.randint(0, 2)

        patch_status = random.choices(
            ["Updated", "Outdated"],
            weights=[90, 10]
        )[0]

        os_outdated = random.choices(
            [0, 1],
            weights=[90, 10]
        )[0]

        sensitive_network_access = random.choices(
            ["No", "Yes"],
            weights=[90, 10]
        )[0]


    elif risk == "Medium":

        unknown_device = random.choices(
            ["No", "Yes"],
            weights=[60, 40]
        )[0]

        open_port_count = random.randint(2, 12)

        critical_cve_count = random.randint(0, 4)

        patch_status = random.choices(
            ["Updated", "Outdated"],
            weights=[75, 25]
        )[0]

        os_outdated = random.choices(
            [0, 1],
            weights=[75, 25]
        )[0]

        sensitive_network_access = random.choices(
            ["No", "Yes"],
            weights=[65, 35]
        )[0]


    elif risk == "High":

        unknown_device = random.choices(
            ["Yes", "No"],
            weights=[80, 20]
        )[0]

        open_port_count = random.randint(4, 20)

        critical_cve_count = random.randint(1, 6)

        patch_status = random.choices(
            ["Updated", "Outdated"],
            weights=[40, 60]
        )[0]

        os_outdated = random.choices(
            [0, 1],
            weights=[30, 70]
        )[0]

        sensitive_network_access = random.choices(
            ["Yes", "No"],
            weights=[70, 30]
        )[0]


    else:

        unknown_device = random.choices(
            ["Yes", "No"],
            weights=[95, 5]
        )[0]

        open_port_count = random.randint(8, 30)

        critical_cve_count = random.randint(3, 10)

        patch_status = "Outdated"

        os_outdated = 1

        sensitive_network_access = random.choices(
            ["Yes", "No"],
            weights=[90, 10]
        )[0]


    return {
        "unknown_device": unknown_device,
        "open_port_count": open_port_count,
        "critical_cve_count": critical_cve_count,
        "patch_status": patch_status,
        "os_outdated": os_outdated,
        "sensitive_network_access": sensitive_network_access,
        "risk": risk
    }


# ============================================================
# GENERATE UNIQUE CLASS DATA
# ============================================================

def generate_class_rows(risk, count):

    unique_rows = set()
    rows = []

    while len(rows) < count:

        row = generate_row(risk)

        key = tuple(
            row[column]
            for column in FINAL_COLUMNS
        )

        if key not in unique_rows:

            unique_rows.add(key)
            rows.append(row)

    return rows


# ============================================================
# MAIN DATASET GENERATION
# ============================================================

def generate_dataset():

    DATASET_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    print()
    print("#" * 70)
    print("# SHADOW IT AI")
    print("# MODULE 1 - DATASET GENERATION")
    print("#" * 70)

    print()
    print("Generating unique dataset...")
    print()

    rows = []

    for risk in RISK_LEVELS:

        print(
            f"Generating {risk} rows..."
        )

        class_rows = generate_class_rows(
            risk,
            ROWS_PER_CLASS
        )

        rows.extend(class_rows)

        print(
            f"   {risk}: {len(class_rows)} unique rows"
        )


    # ========================================================
    # CREATE DATAFRAME
    # ========================================================

    df = pd.DataFrame(rows)

    # ========================================================
    # SHUFFLE
    # ========================================================

    df = df.sample(
        frac=1,
        random_state=RANDOM_STATE
    ).reset_index(drop=True)

    # ========================================================
    # FORCE COLUMN ORDER
    # ========================================================

    df = df[FINAL_COLUMNS]

    # ========================================================
    # VALIDATION BEFORE SAVE
    # ========================================================

    if len(df) != TOTAL_ROWS:

        raise RuntimeError(
            f"Expected {TOTAL_ROWS} rows, got {len(df)}"
        )

    duplicate_count = int(
        df.duplicated().sum()
    )

    if duplicate_count != 0:

        raise RuntimeError(
            f"Duplicate rows found: {duplicate_count}"
        )

    class_counts = df["risk"].value_counts()

    for risk in RISK_LEVELS:

        count = int(
            class_counts.get(risk, 0)
        )

        if count != ROWS_PER_CLASS:

            raise RuntimeError(
                f"{risk} has {count} rows. "
                f"Expected {ROWS_PER_CLASS}."
            )

    # ========================================================
    # SAVE
    # ========================================================

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    # ========================================================
    # FINAL REPORT
    # ========================================================

    print()
    print("=" * 70)
    print("DATASET GENERATED SUCCESSFULLY")
    print("=" * 70)

    print()
    print("Output:")
    print(
        f"   {OUTPUT_FILE}"
    )

    print()
    print("Rows:")
    print(
        f"   {len(df)}"
    )

    print()
    print("Columns:")
    print(
        f"   {len(df.columns)}"
    )

    print()
    print("Duplicate rows:")
    print(
        f"   {df.duplicated().sum()}"
    )

    print()
    print("Class distribution:")

    for risk in RISK_LEVELS:

        count = int(
            class_counts.get(risk, 0)
        )

        percentage = (
            count / len(df)
        ) * 100

        print(
            f"   {risk:<10}: "
            f"{count:4d} "
            f"({percentage:.2f}%)"
        )

    print()
    print("Final columns:")

    for index, column in enumerate(
        df.columns,
        start=1
    ):

        print(
            f"   {index}. {column}"
        )

    print()
    print("=" * 70)
    print("MODULE 1 DATASET GENERATION COMPLETED")
    print("=" * 70)


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    generate_dataset()