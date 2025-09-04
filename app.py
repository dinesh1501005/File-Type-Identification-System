import streamlit as st
import numpy as np
import joblib

# Load the trained model, label encoder, and scaler
model = joblib.load("file_type_model.joblib")
label_encoder = joblib.load("label_encoder.joblib")
scaler = joblib.load("scaler.joblib")

# Supported file types to display on the page
supported_types = ["exe", "PNG", "JPG", "PDF", "ZIP", "BMP", "DOC", "DOCX", "GIF", "MP3", "MP4", "RAR", "WAV", "etc"]

# Helper function: Read the first N bytes of the file and return as a hex string
def file_to_hex(file_obj, num_bytes=100):
    file_obj.seek(0)  # ensure starting at the beginning
    file_bytes = file_obj.read(num_bytes)
    return file_bytes.hex()

# Helper function: Convert hex string to a list of integers, then pad/truncate to fixed_length
def hex_to_int_list(hex_str, fixed_length):
    int_list = [int(hex_str[i:i+2], 16) for i in range(0, len(hex_str), 2)]
    if len(int_list) < fixed_length:
        int_list += [0] * (fixed_length - len(int_list))
    else:
        int_list = int_list[:fixed_length]
    return int_list

# Initialize session state for prediction history if not already present
if "history" not in st.session_state:
    st.session_state.history = []

# Page configuration and header
st.set_page_config(page_title="File Type Identifier", page_icon="📂", layout="centered")
st.markdown("<h1 style='text-align: center; color: #4A90E2;'>File Type Identifier</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Supported file types: " + ", ".join(supported_types) + "</p>", unsafe_allow_html=True)

st.write("Upload a file to predict its type based on its content.")

# File uploader widget
uploaded_file = st.file_uploader("Choose a file", type=supported_types)

if uploaded_file is not None:
    st.markdown(f"<h4 style='text-align: center;'>Uploaded File: {uploaded_file.name}</h4>", unsafe_allow_html=True)
    
    # Extract hex signature from the file (first 100 bytes)
    num_bytes = 100  # adjust as needed
    hex_str = file_to_hex(uploaded_file, num_bytes)
    
    # Display the hex signature on the webpage
    st.markdown(f"<p style='text-align: center;'><strong>Hex Signature:</strong> {hex_str}</p>", unsafe_allow_html=True)
    
    # Convert hex signature to feature vector using the same fixed length used in training
    fixed_length = scaler.mean_.shape[0]  # Assuming this is the fixed length used during training
    features = hex_to_int_list(hex_str, fixed_length)
    features = np.array(features).reshape(1, -1)
    
    # Scale the features using the saved scaler
    features_scaled = scaler.transform(features)
    
    # Make prediction using the loaded model
    pred_encoded = model.predict(features_scaled)
    predicted_category = label_encoder.inverse_transform(pred_encoded)[0]
    
    # Display prediction
    st.markdown(f"<h2 style='text-align: center; color: #28A745;'>Predicted File Type: {predicted_category}</h2>", unsafe_allow_html=True)
    
    # Add prediction to history
    st.session_state.history.append({"filename": uploaded_file.name, "prediction": predicted_category})

# Display prediction history
if st.session_state.history:
    st.markdown("<h3>Prediction History</h3>", unsafe_allow_html=True)
    for idx, record in enumerate(st.session_state.history, start=1):
        st.write(f"{idx}. File: **{record['filename']}** - Prediction: **{record['prediction']}**")

# Button to clear history
if st.button("Clear History"):
    st.session_state.history = []
    st.success("Prediction history cleared!")
