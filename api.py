from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse
import os
import joblib
import numpy as np
import requests

# Load the trained model, label encoder, and scaler
model = joblib.load("file_type_model.joblib")
label_encoder = joblib.load("label_encoder.joblib")
scaler = joblib.load("scaler.joblib")

API_KEY = "your_virustotal_api_key"
VIRUSTOTAL_URL = "https://www.virustotal.com/api/v3/files"

app = FastAPI()

# Helper function: Read the first N bytes of the file and return as a hex string
def file_to_hex(file_obj, num_bytes=100):
    file_bytes = file_obj.read(num_bytes)
    return file_bytes.hex()

# Helper function: Convert hex string to a feature vector
def hex_to_int_list(hex_str, fixed_length):
    int_list = [int(hex_str[i:i+2], 16) for i in range(0, len(hex_str), 2)]
    int_list = int_list[:fixed_length] + [0] * (fixed_length - len(int_list))
    return np.array(int_list).reshape(1, -1)

@app.post("/identify/")
async def identify_file(file: UploadFile = File(...)):
    file_bytes = await file.read()
    hex_str = file_to_hex(file_bytes, 100)
    features = hex_to_int_list(hex_str, scaler.mean_.shape[0])
    features_scaled = scaler.transform(features)
    pred_encoded = model.predict(features_scaled)
    predicted_category = label_encoder.inverse_transform(pred_encoded)[0]
    return {"filename": file.filename, "predicted_type": predicted_category}

@app.post("/scan/")
async def scan_file(file: UploadFile = File(...)):
    headers = {"x-apikey": API_KEY}
    files = {"file": (file.filename, file.file, file.content_type)}
    response = requests.post(VIRUSTOTAL_URL, headers=headers, files=files)
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=400, detail="VirusTotal scan failed")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
