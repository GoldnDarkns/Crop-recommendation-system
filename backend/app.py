import joblib
import os
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify

# --------------------------------------------------
# 1. Initialize Flask app
# --------------------------------------------------
app = Flask("Crop Recommendation API")

# --------------------------------------------------
# 2. Load trained model + label encoder
# --------------------------------------------------
artifacts = joblib.load("crop_recommendation_model.joblib")

model = artifacts["model"]            # XGBoost pipeline (preprocessor + model)
label_encoder = artifacts["label_encoder"]

# Features expected by the model
FEATURE_COLUMNS = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]


# --------------------------------------------------
# 3. Home route
# --------------------------------------------------
@app.get("/")
def home():
    return "Welcome to the Crop Recommendation API"


# --------------------------------------------------
# 4. Single prediction endpoint (JSON)
# --------------------------------------------------
@app.route("/predict", methods=["GET","POST"])
def predict_single():
    if request.method == "GET":
        return "Use POST with JSON body to get predictions.", 200
    """
    Single crop recommendation.

    Expects JSON like:
    {
        "N": 50,
        "P": 40,
        "K": 40,
        "temperature": 25.0,
        "humidity": 80.0,
        "ph": 6.5,
        "rainfall": 120.0
    }
    """

    try:
        data = request.get_json()

        if data is None:
            return jsonify({"error": "Request body must be JSON"}), 400

        # Check for missing fields
        missing = [col for col in FEATURE_COLUMNS if col not in data]
        if missing:
            return jsonify({
                "error": "Missing required fields",
                "missing_fields": missing
            }), 400

        # Build input DataFrame in correct feature order
        values = [[data[col] for col in FEATURE_COLUMNS]]
        input_df = pd.DataFrame(values, columns=FEATURE_COLUMNS)

        # Predict (encoded)
        encoded_pred = model.predict(input_df)
        crop_name = label_encoder.inverse_transform(encoded_pred)[0]

        return jsonify({
            "input": data,
            "recommended_crop": crop_name
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# --------------------------------------------------
# 5. Batch prediction endpoint (CSV upload)
# --------------------------------------------------
@app.route("/batch_predict", methods=["POST"])
def batch_predict():
    """
    Batch crop recommendation via CSV upload.

    Expects a form-data request with a file field called 'file'.

    The CSV must contain the following columns:
    N, P, K, temperature, humidity, ph, rainfall
    """

    try:
        # 1. Check if file is present
        if "file" not in request.files:
            return jsonify({
                "error": "No file part in the request. Please upload a CSV with key 'file'."
            }), 400

        file = request.files["file"]

        # 2. Check file name
        if file.filename == "":
            return jsonify({"error": "No file selected."}), 400

        # 3. Read CSV into DataFrame
        df = pd.read_csv(file)

        # 4. Validate required columns
        missing_cols = [col for col in FEATURE_COLUMNS if col not in df.columns]
        if missing_cols:
            return jsonify({
                "error": "Missing required columns in CSV.",
                "missing_columns": missing_cols
            }), 400

        # 5. Predict using the model
        encoded_preds = model.predict(df[FEATURE_COLUMNS])
        crop_names = label_encoder.inverse_transform(encoded_preds)

        # 6. Add predictions to DataFrame
        df["recommended_crop"] = crop_names

        # 7. Convert to list of dicts for JSON response
        result = df.to_dict(orient="records")
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# --------------------------------------------------
# 6. Run app locally (for development)
# --------------------------------------------------
if __name__ == "__main__":
     
     port = int(os.environ.get("PORT", 8000))  # use PORT env var if set, else 8000
     app.run(host="0.0.0.0", port=port, debug=True)
