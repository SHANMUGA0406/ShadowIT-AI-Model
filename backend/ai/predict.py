import joblib
import pandas as pd

from ai.shap_explainer import explain_prediction, generate_explanation


# Load model
model = joblib.load("ai/risk_model.pkl")


def predict_risk(features):

    feature_names = [
        "unknown_device",
        "open_port_count",
        "critical_cve_count",
        "patch_status",
        "os_version",
        "sensitive_network_access"
    ]


    # Convert dictionary to DataFrame
    data = pd.DataFrame(
        [features],
        columns=feature_names
    )


    # Prediction
    prediction = model.predict(data)[0]


    # Confidence
    confidence = model.predict_proba(data).max() * 100


    # Risk label mapping
    risk_labels = {
        0: "Critical",
        1: "High",
        2: "Low",
        3: "Medium"
    }


    # SHAP explanation
    shap_values = explain_prediction(features)

    reasons = generate_explanation(
        features,
        shap_values
    )


    return {
        "risk": risk_labels[prediction],
        "confidence": f"{confidence:.2f}%",
        "reasons": reasons
    }