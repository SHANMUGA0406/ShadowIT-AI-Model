import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
import joblib

# -----------------------------
# Load the dataset
# -----------------------------
data = pd.read_csv("dataset/devices.csv")

print("Dataset Preview:")
print(data.head())

# -----------------------------
# Encode categorical columns
# -----------------------------
label_encoder = LabelEncoder()

categorical_columns = [
    "unknown_device",
    "patch_status",
    "os_version",
    "sensitive_network_access",
    "risk"
]

for column in categorical_columns:
    data[column] = label_encoder.fit_transform(data[column])

# -----------------------------
# Split features and target
# -----------------------------
X = data.drop("risk", axis=1)
y = data["risk"]

# -----------------------------
# Split training and testing data
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# -----------------------------
# Train Random Forest model
# -----------------------------
model = RandomForestClassifier(random_state=42)

model.fit(X_train, y_train)

# -----------------------------
# Evaluate the model
# -----------------------------
predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print("\nModel Accuracy:", round(accuracy * 100, 2), "%")

# -----------------------------
# Save the trained model
# -----------------------------
joblib.dump(model, "ai/risk_model.pkl")

print("Model saved successfully!")