# ============================================================
# SHADOW IT AI
# MODULE 16 - END-TO-END AI PIPELINE
# ============================================================

from ai.feature_extractor import extract_features
from ai.predict import predict_risk
from ai.shap_explainer import explain_risk
from ai.risk_interpreter import interpret_risk
from decision.decision_engine import determine_decision


# ============================================================
# RUN COMPLETE AI PIPELINE
# ============================================================

def analyze_device(device):

    # --------------------------------------------------------
    # 1. FEATURE EXTRACTION
    # --------------------------------------------------------

    features = extract_features(device)

    # --------------------------------------------------------
    # 2. ML RISK PREDICTION
    # --------------------------------------------------------

    prediction = predict_risk(features)

    risk = prediction["risk"]

    # --------------------------------------------------------
    # 3. SHAP EXPLANATION
    # --------------------------------------------------------

    shap_result = explain_risk(features)

    # --------------------------------------------------------
    # 4. RISK INTERPRETATION
    # --------------------------------------------------------

    interpretation = interpret_risk(
        risk,
        shap_result["top_contributors"]
    )

    # --------------------------------------------------------
    # 5. DECISION SUPPORT
    # --------------------------------------------------------

    decision = determine_decision(
        risk,
        features
    )

    # --------------------------------------------------------
    # FINAL RESULT
    # --------------------------------------------------------

    return {

        "features": features,

        "prediction": prediction,

        "explanation": shap_result,

        "interpretation": interpretation,

        "decision": decision

    }


# ============================================================
# MODULE 16 TEST
# ============================================================

def run_test():

    print()
    print("#" * 70)
    print("# MODULE 16 - END-TO-END AI PIPELINE TEST")
    print("#" * 70)

    # --------------------------------------------------------
    # TEST DEVICE
    # --------------------------------------------------------

    test_device = {

        "status": "Shadow IT",

        "ports": [
            22,
            80,
            443,
            445,
            3389,
            8080,
            8443,
            3306
        ],

        "os": "Windows 7",

        "critical_cve_count": 5,

        "patch_status": 0,

        "sensitive_network_access": 1

    }

    print()
    print("TEST DEVICE")
    print("=" * 70)

    print(
        f"Status       : {test_device['status']}"
    )

    print(
        f"Open ports   : {len(test_device['ports'])}"
    )

    print(
        f"OS           : {test_device['os']}"
    )

    print(
        f"Critical CVEs: {test_device['critical_cve_count']}"
    )

    print(
        f"Patch status : {test_device['patch_status']}"
    )

    print(
        f"Sensitive access: "
        f"{test_device['sensitive_network_access']}"
    )

    # --------------------------------------------------------
    # RUN PIPELINE
    # --------------------------------------------------------

    try:

        result = analyze_device(
            test_device
        )

    except Exception as error:

        print()
        print("❌ END-TO-END PIPELINE FAILED")
        print(
            f"Error: {error}"
        )

        return False

    # --------------------------------------------------------
    # FEATURES
    # --------------------------------------------------------

    print()
    print("=" * 70)
    print("1. FEATURE EXTRACTION")
    print("=" * 70)

    for feature, value in result[
        "features"
    ].items():

        print(
            f"{feature:<30}: {value}"
        )

    # --------------------------------------------------------
    # PREDICTION
    # --------------------------------------------------------

    prediction = result[
        "prediction"
    ]

    print()
    print("=" * 70)
    print("2. ML PREDICTION")
    print("=" * 70)

    print(
        f"Risk       : "
        f"{prediction['risk']}"
    )

    print(
        f"Confidence : "
        f"{prediction['confidence']}%"
    )

    print()
    print("Probabilities:")

    for label, probability in (
        prediction["probabilities"].items()
    ):

        print(
            f"   {label:<10}: "
            f"{probability}%"
        )

    # --------------------------------------------------------
    # SHAP
    # --------------------------------------------------------

    explanation = result[
        "explanation"
    ]

    print()
    print("=" * 70)
    print("3. SHAP EXPLANATION")
    print("=" * 70)

    print(
        explanation["explanation"]
    )

    print()
    print("Top contributors:")

    for index, item in enumerate(
        explanation["top_contributors"],
        start=1
    ):

        print(
            f"{index}. "
            f"{item['feature']} "
            f"→ "
            f"{item['impact']} "
            f"({item['shap_value']})"
        )

    # --------------------------------------------------------
    # RISK INTERPRETATION
    # --------------------------------------------------------

    interpretation = result[
        "interpretation"
    ]

    print()
    print("=" * 70)
    print("4. RISK INTERPRETATION")
    print("=" * 70)

    print(
        f"Risk: "
        f"{interpretation['risk']}"
    )

    print(
        f"Summary: "
        f"{interpretation['summary']}"
    )

    # --------------------------------------------------------
    # DECISION SUPPORT
    # --------------------------------------------------------

    decision = result[
        "decision"
    ]

    print()
    print("=" * 70)
    print("5. DECISION SUPPORT")
    print("=" * 70)

    print(
        f"Priority       : "
        f"{decision['priority']}"
    )

    print(
        f"Severity Score : "
        f"{decision['severity_score']}/100"
    )

    print(
        f"Response Time  : "
        f"{decision['response_time']}"
    )

    print(
        f"Containment    : "
        f"{decision['containment_recommended']}"
    )

    print()
    print(
        f"Decision: "
        f"{decision['decision']}"
    )

    print()
    print("Recommended actions:")

    for index, action in enumerate(
        decision["recommended_actions"],
        start=1
    ):

        print(
            f"   {index}. {action}"
        )

    # --------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------

    assert result["features"][
        "unknown_device"
    ] == 1

    assert result["features"][
        "critical_cve_count"
    ] == 5

    assert prediction[
        "risk"
    ] == "Critical"

    assert explanation[
        "risk"
    ] == "Critical"

    assert interpretation[
        "risk"
    ] == "Critical"

    assert decision[
        "risk"
    ] == "Critical"

    assert decision[
        "containment_recommended"
    ] is True

    assert len(
        decision["recommended_actions"]
    ) > 0

    # --------------------------------------------------------
    # SUCCESS
    # --------------------------------------------------------

    print()
    print("=" * 70)
    print(
        "✅ MODULE 16 END-TO-END AI PIPELINE PASSED"
    )
    print("=" * 70)

    return True


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":

    success = run_test()

    if not success:

        raise SystemExit(1)