from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import os
import pandas as pd

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "model_registry",
    "production_model.pkl"
)
@app.route("/health")
def health():

    try:

        model = joblib.load(
            MODEL_PATH
        )

        return {
            "status": "healthy"
        }, 200

    except Exception as e:

        return {
            "status": "unhealthy",
            "error": str(e)
        }, 500


@app.route("/predict", methods=["POST"])
def predict():

    model = joblib.load(
        MODEL_PATH
    )

    data = request.json

    df = pd.DataFrame([{
        "windspeed": data["windspeed"],
        "cloudcover": data["cloudcover"],
        "humidity": data["humidity"],
        "pressure": data["pressure"]
    }])

    prediction = model.predict(df)[0]

    return jsonify({
        "temperature": round(
            float(prediction),
            2
        )
    })

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )