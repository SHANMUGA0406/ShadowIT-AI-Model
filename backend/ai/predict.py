import os
import json
import joblib
import numpy as np


# ============================================================
# SHADOW IT AI
# MODULE 10 - PREDICTION
# ============================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(
    BASE_DIR,
    "ai",
    "models",
    "risk_model.pkl"
)

LABEL_MAPPING_PATH = os.path.join(
    BASE_DIR,
    "ai",
    "models",
    "label_mapping.json"
)

FEATURE_CONFIG_PATH = os.path.join(
    BASE_DIR,
    "ai",
    "models",
    "feature_config.json"
)


# ============================================================
# LOAD FINAL MODEL
# ============================================================

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(
        f"Final risk model not found: {MODEL_PATH}"
    )

model = joblib.load(MODEL_PATH)


# ============================================================
# LOAD LABEL MAPPING
# ============================================================

DEFAULT_LABEL_MAPPING = {
    0: "Low",
    1: "Medium",
    2: "High",
    3: "Critical"
}


if os.path.exists(LABEL_MAPPING_PATH):

    with open(
        LABEL_MAPPING_PATH,
        "r",
        encoding="utf-8"
    ) as f:

        raw_mapping = json.load(f)

    # --------------------------------------------------------
    # Format 1:
    #
    # {
    #     "Low": 0,
    #     "Medium": 1,
    #     "High": 2,
    #     "Critical": 3
    # }
    # --------------------------------------------------------

    if all(
        isinstance(k, str) and
        isinstance(v, (int, float))
        for k, v in raw_mapping.items()
    ):

        label_mapping = {
            int(v): k
            for k, v in raw_mapping.items()
        }

    # --------------------------------------------------------
    # Format 2:
    #
    # {
    #     "0": "Low",
    #     "1": "Medium",
    #     "2": "High",
    #     "3": "Critical"
    # }
    # --------------------------------------------------------

    elif all(
        str(k).isdigit()
        for k in raw_mapping.keys()
    ):

        label_mapping = {
            int(k): str(v)
            for k, v in raw_mapping.items()
        }

    else:

        print(
            "WARNING: Invalid label_mapping.json format."
        )

        print(
            "Using default mapping."
        )

        label_mapping = DEFAULT_LABEL_MAPPING

else:

    print(
        "WARNING: label_mapping.json not found."
    )

    print(
        "Using default mapping."
    )

    label_mapping = DEFAULT_LABEL_MAPPING


# ============================================================
# FEATURE ORDER
# ============================================================

DEFAULT_FEATURE_ORDER = [
    "unknown_device",
    "open_port_count",
    "critical_cve_count",
    "patch_status",
    "os_outdated",
    "sensitive_network_access"
]


if os.path.exists(FEATURE_CONFIG_PATH):

    with open(
        FEATURE_CONFIG_PATH,
        "r",
        encoding="utf-8"
    ) as f:

        feature_config = json.load(f)

    if isinstance(feature_config, dict):

        FEATURE_ORDER = feature_config.get(
            "features",
            DEFAULT_FEATURE_ORDER
        )

    elif isinstance(feature_config, list):

        FEATURE_ORDER = feature_config

    else:

        FEATURE_ORDER = DEFAULT_FEATURE_ORDER

else:

    print(
        "WARNING: feature_config.json not found."
    )

    print(
        "Using default feature order."
    )

    FEATURE_ORDER = DEFAULT_FEATURE_ORDER


# ============================================================
# PREDICT RISK
# ============================================================

def predict_risk(features):

    """
    Predict Shadow IT device risk.

    Input:
        features = {
            "unknown_device": 1,
            "open_port_count": 8,
            "critical_cve_count": 5,
            "patch_status": 0,
            "os_outdated": 1,
            "sensitive_network_access": 1
        }

    Output:
        {
            "risk": "Critical",
            "confidence": 86.7,
            "probabilities": {...}
        }
    """

    # --------------------------------------------------------
    # Validate features
    # --------------------------------------------------------

    missing_features = [
        feature
        for feature in FEATURE_ORDER
        if feature not in features
    ]

    if missing_features:

        raise ValueError(
            f"Missing required features: {missing_features}"
        )

    # --------------------------------------------------------
    # Create feature vector
    # --------------------------------------------------------

    feature_vector = [
        features[feature]
        for feature in FEATURE_ORDER
    ]

    # --------------------------------------------------------
    # Convert to numpy
    # --------------------------------------------------------

    X = np.array(
        feature_vector,
        dtype=float
    ).reshape(1, -1)

    # --------------------------------------------------------
    # Prediction
    # --------------------------------------------------------

    prediction = model.predict(X)[0]

    prediction = int(prediction)

    risk = label_mapping.get(
        prediction,
        "Unknown"
    )

    # --------------------------------------------------------
    # Probability
    # --------------------------------------------------------

    probabilities = model.predict_proba(X)[0]

    confidence = float(
        np.max(probabilities) * 100
    )

    probability_dict = {}

    for index, probability in enumerate(probabilities):

        label = label_mapping.get(
            index,
            str(index)
        )

        probability_dict[label] = round(
            float(probability) * 100,
            2
        )

    # --------------------------------------------------------
    # Return result
    # --------------------------------------------------------

    return {
        "risk": risk,
        "confidence": round(
            confidence,
            2
        ),
        "probabilities": probability_dict
    }


# ============================================================
# STANDALONE TEST
# ============================================================

if __name__ == "__main__":

    print("=" * 70)
    print("SHADOW IT AI - PREDICTION TEST")
    print("=" * 70)

    test_features = {

        "unknown_device": 1,

        "open_port_count": 8,

        "critical_cve_count": 5,

        "patch_status": 0,

        "os_outdated": 1,

        "sensitive_network_access": 1

    }

    print("\nTest Features:")
    print(test_features)

    result = predict_risk(
        test_features
    )

    print("\nPrediction Result:")
    print(result)

    print("\nPrediction test completed successfully.")