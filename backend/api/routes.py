from fastapi import APIRouter

from scanner.scan import scan_network
from shadow_it.detect import detect_shadow_it

from ai.feature_extractor import extract_features
from ai.predict import predict_risk

from impact.impact_analyzer import analyze_impact

from decision.decision_engine import generate_decision

from database.storage import save_devices, get_devices, get_device


router = APIRouter()


@router.post("/scan")
def scan():

    devices = scan_network()

    devices = detect_shadow_it(devices)


    for device in devices:

        features = extract_features(device)

        prediction = predict_risk(features)


        device["risk"] = prediction["risk"]

        device["confidence"] = prediction["confidence"]

        device["reasons"] = prediction["reasons"]


        device["possible_impacts"] = analyze_impact(device)


        decision = generate_decision(device)


        device["priority"] = decision["priority"]

        device["recommendations"] = decision["recommendations"]



    save_devices(devices)


    return devices



@router.get("/devices")
def devices():

    return get_devices()



@router.get("/device/{id}")
def device_details(id: int):

    device = get_device(id)


    if device is None:

        return {
            "message": "Device not found"
        }


    return device



@router.get("/dashboard")
def dashboard():

    devices = get_devices()


    total = len(devices)


    critical = 0
    high = 0
    medium = 0
    low = 0


    for device in devices:

        if device["risk"] == "Critical":

            critical += 1

        elif device["risk"] == "High":

            high += 1

        elif device["risk"] == "Medium":

            medium += 1

        else:

            low += 1



    return {

        "total_devices": total,

        "critical": critical,

        "high": high,

        "medium": medium,

        "low": low

    }