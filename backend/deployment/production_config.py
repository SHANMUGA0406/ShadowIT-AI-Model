# ============================================================
# SHADOW IT AI
# MODULE 26 - PRODUCTION CONFIGURATION
# ============================================================

import os


# ============================================================
# APPLICATION CONFIGURATION
# ============================================================

APP_NAME = os.getenv(
    "SHADOW_IT_APP_NAME",
    "Shadow IT AI API"
)

APP_VERSION = os.getenv(
    "SHADOW_IT_APP_VERSION",
    "0.1.0"
)

HOST = os.getenv(
    "SHADOW_IT_HOST",
    "127.0.0.1"
)

PORT = int(
    os.getenv(
        "SHADOW_IT_PORT",
        "8000"
    )
)

# Production mode should not use auto-reload.
RELOAD = False


# ============================================================
# API CONFIGURATION
# ============================================================

API_BASE_PATH = "/"

STATUS_ENDPOINT = "/api/status"

SCAN_ENDPOINT = "/scan"

DEVICES_ENDPOINT = "/devices"

DASHBOARD_ENDPOINT = "/dashboard"


# ============================================================
# MODEL CONFIGURATION
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

MODEL_DIR = os.path.join(
    BASE_DIR,
    "ai",
    "models"
)

MODEL_PATH = os.path.join(
    MODEL_DIR,
    "risk_model.pkl"
)

LABEL_MAPPING_PATH = os.path.join(
    MODEL_DIR,
    "label_mapping.json"
)

FEATURE_CONFIG_PATH = os.path.join(
    MODEL_DIR,
    "feature_config.json"
)


# ============================================================
# DATASET CONFIGURATION
# ============================================================

DATASET_PATH = os.path.join(
    BASE_DIR,
    "dataset",
    "devices.csv"
)


# ============================================================
# SECURITY CONFIGURATION
# ============================================================

DEBUG = False

EXPOSE_ERROR_DETAILS = False

ALLOW_CREDENTIALS = True


# ============================================================
# PRODUCTION VALIDATION
# ============================================================

def validate_configuration():

    errors = []

    # --------------------------------------------------------
    # MODEL
    # --------------------------------------------------------

    if not os.path.isfile(MODEL_PATH):

        errors.append(
            f"Missing model: {MODEL_PATH}"
        )

    # --------------------------------------------------------
    # LABEL MAPPING
    # --------------------------------------------------------

    if not os.path.isfile(
        LABEL_MAPPING_PATH
    ):

        errors.append(
            f"Missing label mapping: "
            f"{LABEL_MAPPING_PATH}"
        )

    # --------------------------------------------------------
    # FEATURE CONFIG
    # --------------------------------------------------------

    if not os.path.isfile(
        FEATURE_CONFIG_PATH
    ):

        errors.append(
            f"Missing feature configuration: "
            f"{FEATURE_CONFIG_PATH}"
        )

    # --------------------------------------------------------
    # DATASET
    # --------------------------------------------------------

    if not os.path.isfile(
        DATASET_PATH
    ):

        errors.append(
            f"Missing dataset: {DATASET_PATH}"
        )

    # --------------------------------------------------------
    # PORT
    # --------------------------------------------------------

    if PORT < 1 or PORT > 65535:

        errors.append(
            f"Invalid port: {PORT}"
        )

    # --------------------------------------------------------
    # DEBUG
    # --------------------------------------------------------

    if DEBUG:

        errors.append(
            "DEBUG must be disabled in production."
        )

    # --------------------------------------------------------
    # RESULT
    # --------------------------------------------------------

    return errors


# ============================================================
# DISPLAY CONFIGURATION
# ============================================================

def print_configuration():

    print()
    print("=" * 70)
    print(
        "SHADOW IT AI - PRODUCTION CONFIGURATION"
    )
    print("=" * 70)

    print(
        f"Application : {APP_NAME}"
    )

    print(
        f"Version     : {APP_VERSION}"
    )

    print(
        f"Host        : {HOST}"
    )

    print(
        f"Port        : {PORT}"
    )

    print(
        f"Reload      : {RELOAD}"
    )

    print(
        f"Debug       : {DEBUG}"
    )

    print()

    print(
        f"Model       : {MODEL_PATH}"
    )

    print(
        f"Label Map   : {LABEL_MAPPING_PATH}"
    )

    print(
        f"Features    : {FEATURE_CONFIG_PATH}"
    )

    print(
        f"Dataset     : {DATASET_PATH}"
    )

    print("=" * 70)


# ============================================================
# STANDALONE TEST
# ============================================================

if __name__ == "__main__":

    print()
    print("#" * 70)
    print("# SHADOW IT AI")
    print("# MODULE 26 - PRODUCTION CONFIGURATION TEST")
    print("#" * 70)

    print_configuration()

    print()
    print("=" * 70)
    print("VALIDATING PRODUCTION CONFIGURATION")
    print("=" * 70)

    errors = validate_configuration()

    if errors:

        print(
            "Production configuration: FAIL"
        )

        print()

        for error in errors:

            print(
                f"   ERROR: {error}"
            )

        raise SystemExit(1)

    print(
        "Production configuration: PASS"
    )

    print()
    print("=" * 70)
    print("MODULE 26 CONFIGURATION TEST: PASSED")
    print("=" * 70)