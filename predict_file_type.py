import numpy as np
import joblib

# Function to convert hex data to numeric features
def hex_to_features(hex_data):
    byte_data = [int(hex_data[i:i+2], 16) for i in range(0, len(hex_data), 2)]
    byte_data = byte_data[:256]  # Truncate or pad
    return byte_data + [0] * (256 - len(byte_data))  # Pad with zeros if needed

# Load the trained model
try:
    clf = joblib.load('file_type_classifier.pkl')
    label_encoder = joblib.load('label_encoder.pkl')  # Load the label encoder
    print("Model loaded successfully.")
except FileNotFoundError as e:
    print(f"Error loading the model: {e}")
    exit()

# Take user input for hex data
hex_input = input("Enter Hex Data: ").strip()

# Convert input to features
features = np.array([hex_to_features(hex_input)])

# Make prediction
predicted_label_encoded = clf.predict(features)[0]

# Decode predicted label
predicted_label = label_encoder.inverse_transform([predicted_label_encoded])[0]

print(f"Predicted File Type: {predicted_label}")
