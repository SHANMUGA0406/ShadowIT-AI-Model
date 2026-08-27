# Shadow IT AI

## Explainable AI-Based Shadow IT Detection and Decision Intelligence Platform

### 1. Project Overview

**Shadow IT AI** is a cybersecurity platform that detects devices connected to a network, identifies unauthorized/unknown devices, predicts their security risk using Machine Learning, explains the prediction, analyzes security impacts, and provides recommended actions.

The project is developed for **SIH 2026**.

---

## 2. Problem Statement

Organizations may have unauthorized or unmanaged devices connected to their network.

These devices can introduce:

* Unknown devices
* Open ports
* Outdated operating systems
* Unpatched systems
* Critical vulnerabilities
* Sensitive network access
* Increased attack surface

Traditional monitoring can identify devices, but our system goes further by using **AI to classify risk and provide an actionable security decision**.

---

## 3. Our Unique Solution

The main uniqueness of Shadow IT AI is that it combines multiple security capabilities into one pipeline:

**Discover → Detect → Predict → Explain → Analyze → Decide**

Instead of only showing:

> "Unknown device detected"

the system provides:

> **What is the risk? Why is it risky? What impact can it cause? What should the security team do?**

---

## 4. Main Features

* Network device discovery using Nmap
* Shadow IT / unauthorized device detection
* Machine Learning risk classification
* Four-level risk prediction
* Prediction confidence and probabilities
* SHAP-based Explainable AI
* Security impact analysis
* Rule-based Decision Engine
* Recommended security actions
* FastAPI backend
* React dashboard integration
* Dataset validation and preprocessing
* Model evaluation
* Deployment and integration testing

---

# 5. Technology Stack

| Component        | Technology               |
| ---------------- | ------------------------ |
| Frontend         | React                    |
| Backend          | FastAPI                  |
| Programming      | Python                   |
| Network Scanner  | Nmap                     |
| Machine Learning | Scikit-learn             |
| ML Models        | Random Forest, XGBoost   |
| Explainable AI   | SHAP                     |
| Data Processing  | Pandas, NumPy            |
| Model Storage    | Joblib / PKL             |
| API Testing      | FastAPI / Python testing |
| Version Control  | Git + GitHub             |

---

# 6. Machine Learning

The model classifies devices into four risk levels:

| Risk     | Meaning                   |
| -------- | ------------------------- |
| Low      | Limited security risk     |
| Medium   | Moderate security concern |
| High     | Significant security risk |
| Critical | Severe security risk      |

### Model Features

The final model uses:

```text
unknown_device
open_port_count
critical_cve_count
patch_status
os_outdated
sensitive_network_access
```

### Label Mapping

```text
Low      → 0
Medium   → 1
High     → 2
Critical → 3
```

---

# 7. Dataset

The training dataset is stored in:

```text
backend/dataset/devices.csv
```

The dataset contains device security characteristics and corresponding risk labels.

The dataset is used for **training and evaluating the ML model**.

The trained model is then used to predict the risk of newly scanned devices.

---

# 8. Real-World Data Flow

The model can work with real network scan information.

Nmap discovers real devices:

```text
Real Network
     ↓
Nmap Scanner
     ↓
Device Information
     ↓
Feature Extraction
     ↓
ML Model
     ↓
Risk Prediction
```

For example:

```text
Device:
localhost
IP: 127.0.0.1
Open Ports: 135, 445, 8000
```

The system converts the information into features:

```text
unknown_device = 0
open_port_count = 3
critical_cve_count = 0
patch_status = 1
os_outdated = 0
sensitive_network_access = 0
```

The trained model then predicts the device's risk.

### Important

The training dataset and real-time scanning are different.

```text
Training Dataset
      ↓
Train ML Model
      ↓
Final Model
      ↓
Real Network Scan
      ↓
Feature Extraction
      ↓
Risk Prediction
```

The model does **not** retrain every time a scan is performed.

---

# 9. Complete Workflow

```text
                Network
                   ↓
              Nmap Scanner
                   ↓
           Device Discovery
                   ↓
          Shadow IT Detection
                   ↓
           Feature Extraction
                   ↓
            ML Risk Prediction
                   ↓
          ┌────────┴────────┐
          ↓                 ↓
       Risk            Confidence
          ↓
       SHAP
   Explainability
          ↓
 Security Impact Analysis
          ↓
      Decision Engine
          ↓
     Recommended Action
          ↓
      FastAPI Backend
          ↓
      React Dashboard
```

---

# 10. Shadow IT Detection

The discovered device is compared with the approved device list.

```text
              Device Found
                   ↓
          Is it approved?
             ↙         ↘
           YES          NO
            ↓            ↓
       Authorized     Shadow IT
```

---

# 11. Explainable AI

The system uses **SHAP** to explain the ML prediction.

Instead of only displaying:

```text
Risk: High
```

the system can explain which features contributed to the prediction.

Example:

```text
Open Port Count       → Risk contribution
Unknown Device        → Risk contribution
Outdated OS           → Risk contribution
Critical CVEs         → Risk contribution
```

This makes the AI decision more understandable to security teams.

---

# 12. Security Impact Analysis

After predicting risk, the system analyzes possible security impacts.

Examples:

```text
Network Attack Risk
Unauthorized Access Risk
Vulnerability Risk
Data Exposure Risk
```

This gives additional security context to the prediction.

---

# 13. Decision Engine

The Decision Engine converts the AI result into an actionable security decision.

Example:

```text
Risk: Low
Priority: LOW
Decision: MONITOR DEVICE
Response: Within 7 days
```

For higher-risk devices, the system can recommend actions such as:

```text
Investigate Device
Patch Device
Restrict Access
Isolate Device
Escalate Incident
```

Therefore, the system goes beyond **risk prediction** and provides **decision support**.

---

# 14. Backend API

The FastAPI backend provides endpoints for the frontend.

Main endpoints:

```text
GET  /api/status
POST /scan
GET  /devices
GET  /dashboard
GET  /device/{device_id}
GET  /device/{device_id}/impact
GET  /device/{device_id}/decision
POST /analyze
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

---

# 15. Example Output

Example device result:

```text
Hostname: localhost
IP: 127.0.0.1

Status: Authorized

Risk: Low
Confidence: 66.35%

Security Impact:
- Network Attack Risk

Decision:
- Priority: LOW
- Action: MONITOR DEVICE
- Response Time: Within 7 days
```

---

# 16. Prototype vs Improved Model

| Prototype                      | Improved Model                          |
| ------------------------------ | --------------------------------------- |
| Small manually created dataset | Larger structured dataset               |
| Basic ML implementation        | Complete ML pipeline                    |
| Basic features                 | Standardized security features          |
| Basic prediction               | Prediction + confidence + probabilities |
| Limited validation             | Dataset validation                      |
| Single model approach          | Random Forest + XGBoost comparison      |
| Basic output                   | Risk + Impact + Decision                |
| Manual testing                 | Integration and deployment testing      |
| Prototype configuration        | Production configuration                |
| Basic backend                  | Complete FastAPI integration            |
| Basic model                    | Final trained model + configuration     |

---

# 17. Project Modules

The development process included:

```text
Dataset Generation
       ↓
Dataset Validation
       ↓
Preprocessing
       ↓
Feature Engineering
       ↓
Train/Test Split
       ↓
Random Forest
       ↓
XGBoost
       ↓
Model Evaluation
       ↓
Model Selection
       ↓
Final Model Training
       ↓
Prediction
       ↓
SHAP Explainability
       ↓
Impact Analysis
       ↓
Decision Engine
       ↓
FastAPI Integration
       ↓
Testing
       ↓
Deployment Validation
```

---

# 18. Backend / AI Responsibility

The Backend/AI part includes:

* Dataset creation and validation
* Data preprocessing
* Feature engineering
* ML model training
* Model evaluation
* Model selection
* Final model creation
* Prediction pipeline
* SHAP explainability
* Shadow IT detection
* Security impact analysis
* Decision Engine
* FastAPI APIs
* Integration testing
* Deployment validation

---

# 19. Frontend Responsibility

The Frontend part includes:

* React dashboard
* Device list
* Risk visualization
* Risk distribution
* Device details
* Security impact display
* AI explanation display
* Decision/recommendation display
* API integration
* User interface and interaction

---

# 20. Backend and Frontend Integration

```text
React Frontend
      ↓
FastAPI API
      ↓
Nmap Scanner
      ↓
Shadow IT Detection
      ↓
Feature Extraction
      ↓
ML Prediction
      ↓
SHAP Explanation
      ↓
Impact Analysis
      ↓
Decision Engine
      ↓
JSON Response
      ↓
React Dashboard
```

The frontend does not need to directly access the ML model.

It communicates with the backend through the API.

---

# 21. Testing

The completed system was tested through:

* Final system validation
* Application readiness testing
* Production configuration testing
* Deployment validation
* Deployment smoke testing
* Final deployment verification
* Final release validation

All major validation stages passed successfully.

---

# 22. Current Status

```text
Dataset                  ✓
Preprocessing            ✓
Feature Engineering      ✓
Model Training           ✓
Model Evaluation         ✓
Model Selection          ✓
Final Model              ✓
Prediction               ✓
SHAP Explainability      ✓
Shadow IT Detection      ✓
Impact Analysis          ✓
Decision Engine           ✓
FastAPI Backend          ✓
Integration Testing      ✓
Deployment Testing       ✓
Final Verification       ✓
```

### Backend + AI Model: COMPLETE

---

# 23. Future Improvements

Future versions can include:

* Real CVE database integration
* Real patch-status verification
* Advanced OS fingerprinting
* Enterprise asset inventory
* Continuous network monitoring
* Historical risk tracking
* Risk trend analysis
* Security alerts and notifications
* Database persistence
* Cloud deployment
* Advanced SHAP visualizations

---

# 24. Project Goal

The final goal of Shadow IT AI is to transform raw network discovery into intelligent security decisions:

```text
Visibility
    ↓
Detection
    ↓
Risk Prediction
    ↓
Explanation
    ↓
Security Impact
    ↓
Decision
    ↓
Action
```

**Shadow IT AI is designed to answer three important questions:**

1. **What devices are present in the network?**
2. **How risky is each device and why?**
3. **What should the security team do about it?**

---

## Team Project

**Project:** Explainable AI-Based Shadow IT Detection and Decision Intelligence Platform

**Event:** Smart India Hackathon (SIH) 2026

**Repository:** Shadow IT AI Model + Backend

**Status:** Backend and AI model development completed.
