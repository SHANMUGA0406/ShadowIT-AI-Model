# ============================================================
# SHADOW IT AI
# API ROUTES
# ============================================================

from fastapi import APIRouter, HTTPException
from typing import Any, Dict

# ------------------------------------------------------------
# SCANNER
# ------------------------------------------------------------

from scanner.scan import scan_network

# ------------------------------------------------------------
# SHADOW IT DETECTION
# ------------------------------------------------------------

from shadow_it.detect import detect_shadow_it

# ------------------------------------------------------------
# FEATURE EXTRACTION
# ------------------------------------------------------------

from ai.feature_extractor import extract_features

# ------------------------------------------------------------
# AI PREDICTION
# ------------------------------------------------------------

from ai.predict import predict_risk

# ------------------------------------------------------------
# SECURITY IMPACT ANALYZER
# ------------------------------------------------------------

from impact.impact_analyzer import analyze_impact

# ------------------------------------------------------------
# DECISION ENGINE
# ------------------------------------------------------------

from decision.decision_engine import generate_decision


# ============================================================
# ROUTER
# ============================================================

router = APIRouter()


# ============================================================
# TEMPORARY IN-MEMORY DEVICE STORAGE
# ============================================================

devices_database = []


# ============================================================
# HOME / API STATUS
# ============================================================

@router.get("/api/status")
def api_status():

    return {
        "status": "running",
        "service": "Shadow IT AI API",
        "version": "0.1.0"
    }


# ============================================================
# SCAN NETWORK
# ============================================================

@router.post("/scan")
def scan():

    try:

        # ----------------------------------------------------
        # 1. DEVICE DISCOVERY
        # ----------------------------------------------------

        discovered_devices = scan_network()

        # ----------------------------------------------------
        # 2. SHADOW IT DETECTION
        # ----------------------------------------------------

        detected_devices = detect_shadow_it(
            discovered_devices
        )

        final_devices = []

        # ----------------------------------------------------
        # 3. PROCESS EACH DEVICE
        # ----------------------------------------------------

        for device in detected_devices:

            # ================================================
            # FEATURE EXTRACTION
            # ================================================

            features = extract_features(
                device
            )

            # ================================================
            # AI RISK PREDICTION
            # ================================================

            prediction = predict_risk(
                features
            )

            # ================================================
            # ADD FEATURES
            # ================================================

            device["features"] = features

            # ================================================
            # ADD AI RESULT
            # ================================================

            device["risk"] = prediction["risk"]

            device["confidence"] = prediction[
                "confidence"
            ]

            device["probabilities"] = prediction[
                "probabilities"
            ]

            # ================================================
            # SECURITY IMPACT ANALYSIS
            # ================================================

            impacts = analyze_impact(
                device
            )

            device["security_impacts"] = impacts

            # ================================================
            # DECISION ENGINE
            # ================================================

            # Decision engine expects the ML features
            # at the top level.

            decision_input = {
                "unknown_device":
                    features["unknown_device"],

                "open_port_count":
                    features["open_port_count"],

                "critical_cve_count":
                    features["critical_cve_count"],

                "patch_status":
                    features["patch_status"],

                "os_outdated":
                    features["os_outdated"],

                "sensitive_network_access":
                    features[
                        "sensitive_network_access"
                    ],

                "risk":
                    prediction["risk"],

                "confidence":
                    prediction["confidence"]
            }

            decision = generate_decision(
                decision_input
            )

            device["decision"] = decision

            # ================================================
            # SAVE FINAL DEVICE
            # ================================================

            final_devices.append(
                device
            )

        # ----------------------------------------------------
        # SAVE TO MEMORY
        # ----------------------------------------------------

        global devices_database

        devices_database = final_devices

        # ----------------------------------------------------
        # API RESPONSE
        # ----------------------------------------------------

        return {
            "status": "success",
            "device_count": len(
                final_devices
            ),
            "devices": final_devices
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


# ============================================================
# GET ALL DEVICES
# ============================================================

@router.get("/devices")
def get_devices():

    return {
        "status": "success",
        "device_count": len(
            devices_database
        ),
        "devices": devices_database
    }


# ============================================================
# GET DASHBOARD SUMMARY
# ============================================================

@router.get("/dashboard")
def get_dashboard():

    total_devices = len(
        devices_database
    )

    shadow_it_count = 0

    authorized_count = 0

    low_count = 0
    medium_count = 0
    high_count = 0
    critical_count = 0

    for device in devices_database:

        # ----------------------------------------------------
        # DEVICE STATUS
        # ----------------------------------------------------

        status = device.get(
            "status",
            ""
        )

        if status == "Shadow IT":

            shadow_it_count += 1

        elif status == "Authorized":

            authorized_count += 1

        # ----------------------------------------------------
        # RISK
        # ----------------------------------------------------

        risk = device.get(
            "risk",
            "Low"
        )

        if risk == "Low":

            low_count += 1

        elif risk == "Medium":

            medium_count += 1

        elif risk == "High":

            high_count += 1

        elif risk == "Critical":

            critical_count += 1

    return {

        "status": "success",

        "total_devices":
            total_devices,

        "shadow_it_devices":
            shadow_it_count,

        "authorized_devices":
            authorized_count,

        "risk_distribution": {

            "Low":
                low_count,

            "Medium":
                medium_count,

            "High":
                high_count,

            "Critical":
                critical_count
        }
    }


# ============================================================
# GET DEVICE BY INDEX
# ============================================================

@router.get("/device/{device_id}")
def get_device(
    device_id: int
):

    if device_id < 0:

        raise HTTPException(
            status_code=400,
            detail="Device ID cannot be negative."
        )

    if device_id >= len(
        devices_database
    ):

        raise HTTPException(
            status_code=404,
            detail="Device not found."
        )

    return {
        "status": "success",
        "device": devices_database[
            device_id
        ]
    }


# ============================================================
# GET SECURITY IMPACTS FOR DEVICE
# ============================================================

@router.get("/device/{device_id}/impact")
def get_device_impact(
    device_id: int
):

    if device_id < 0 or device_id >= len(
        devices_database
    ):

        raise HTTPException(
            status_code=404,
            detail="Device not found."
        )

    device = devices_database[
        device_id
    ]

    return {
        "status": "success",
        "device_id": device_id,
        "security_impacts":
            device.get(
                "security_impacts",
                []
            )
    }


# ============================================================
# GET DECISION FOR DEVICE
# ============================================================

@router.get("/device/{device_id}/decision")
def get_device_decision(
    device_id: int
):

    if device_id < 0 or device_id >= len(
        devices_database
    ):

        raise HTTPException(
            status_code=404,
            detail="Device not found."
        )

    device = devices_database[
        device_id
    ]

    return {
        "status": "success",
        "device_id": device_id,
        "decision":
            device.get(
                "decision",
                {}
            )
    }


# ============================================================
# MANUAL DEVICE ANALYSIS
# ============================================================

@router.post("/analyze")
def analyze_device(
    device: Dict[str, Any]
):

    try:

        # ----------------------------------------------------
        # FEATURE EXTRACTION
        # ----------------------------------------------------

        features = extract_features(
            device
        )

        # ----------------------------------------------------
        # PREDICTION
        # ----------------------------------------------------

        prediction = predict_risk(
            features
        )

        # ----------------------------------------------------
        # IMPACT
        # ----------------------------------------------------

        impact_device = dict(device)

        impact_device[
            "features"
        ] = features

        impacts = analyze_impact(
            impact_device
        )

        # ----------------------------------------------------
        # DECISION
        # ----------------------------------------------------

        decision_input = {
            **features,

            "risk":
                prediction["risk"],

            "confidence":
                prediction["confidence"]
        }

        decision = generate_decision(
            decision_input
        )

        # ----------------------------------------------------
        # RESULT
        # ----------------------------------------------------

        return {

            "status": "success",

            "features":
                features,

            "prediction":
                prediction,

            "security_impacts":
                impacts,

            "decision":
                decision
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )