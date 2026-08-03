def generate_decision(device):

    priority = "Low"

    recommendations = []

    risk = device["risk"]


    if risk == "Critical":

        priority = "Immediate"

        recommendations.append(
            "Disconnect Device from Network"
        )

        recommendations.append(
            "Block suspicious ports"
        )

        recommendations.append(
            "Investigate security vulnerability"
        )


    elif risk == "High":

        priority = "High"

        recommendations.append(
            "Review Device Access"
        )

        recommendations.append(
            "Apply Security Patches"
        )


    elif risk == "Medium":

        priority = "Medium"

        recommendations.append(
            "Monitor Device Activity"
        )

        recommendations.append(
            "Update Software"
        )


    else:

        priority = "Low"

        recommendations.append(
            "Continue Monitoring"
        )


    return {
        "priority": priority,
        "recommendations": recommendations
    }



# Testing

test_device = {
    "risk": "Critical"
}


print(generate_decision(test_device))