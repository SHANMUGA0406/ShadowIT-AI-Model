import shap
import joblib
import pandas as pd


# Load trained Random Forest model
model = joblib.load("ai/risk_model.pkl")


def explain_prediction(features):

    feature_names = [
        "unknown_device",
        "open_port_count",
        "critical_cve_count",
        "patch_status",
        "os_version",
        "sensitive_network_access"
    ]


    data = pd.DataFrame(
        [features],
        columns=feature_names
    )


    explainer = shap.TreeExplainer(model)

    shap_values = explainer.shap_values(data)


    return shap_values



def generate_explanation(features, shap_values):

    reasons = []

    if features["unknown_device"] == 1:
        reasons.append("Unknown Device")

    if features["open_port_count"] > 3:
        reasons.append("Multiple Open Ports")

    if features["critical_cve_count"] > 0:
        reasons.append("Critical CVE Found")

    if features["patch_status"] == 0:
        reasons.append("Outdated Patch Status")

    return reasons



# Temporary Testing

test_features = {
    "unknown_device": 1,
    "open_port_count": 5,
    "critical_cve_count": 2,
    "patch_status": 0,
    "os_version": 1,
    "sensitive_network_access": 1
}


shap_result = explain_prediction(test_features)

print(shap_result)


reasons = generate_explanation(
    test_features,
    shap_result
)

print(reasons)