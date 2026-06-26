import os
import shutil
import json
import pandas as pd
import joblib

from sklearn.metrics import r2_score

# ==========================
# Base Directory
# ==========================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_REGISTRY = os.path.join(
    BASE_DIR,
    "..",
    "model_registry"
)

VALIDATION_DIR = os.path.join(
    BASE_DIR,
    "..",
    "validation_dataset"
)

# ==========================
# File Paths
# ==========================

PRODUCTION_MODEL = os.path.join(
    MODEL_REGISTRY,
    "production_model.pkl"
)

CANDIDATE_MODEL = os.path.join(
    MODEL_REGISTRY,
    "candidate_model.pkl"
)

CANDIDATE_VERSION_FILE = os.path.join(
    MODEL_REGISTRY,
    "candidate_version.txt"
)

VALIDATION_DATA = os.path.join(
    VALIDATION_DIR,
    "validation_data.csv"
)

REPORT_FILE = os.path.join(
    MODEL_REGISTRY,
    "model_report.txt"
)

METADATA_FILE = os.path.join(
    MODEL_REGISTRY,
    "metadata.json"
)
print("\n==============================")
print("BASE_DIR:", BASE_DIR)
print("MODEL_REGISTRY:", MODEL_REGISTRY)
print("METADATA_FILE:", METADATA_FILE)
print("==============================\n")
# ==========================
# Check Required Files
# ==========================

required_files = [
    PRODUCTION_MODEL,
    CANDIDATE_MODEL,
    CANDIDATE_VERSION_FILE,
    VALIDATION_DATA,
    METADATA_FILE
]

for file in required_files:

    if not os.path.exists(file):

        print(f"File Not Found: {file}")
        exit()

# ==========================
# Load Validation Dataset
# ==========================

validation_df = pd.read_csv(
    VALIDATION_DATA
)

X = validation_df[
    [
        "windspeed",
        "cloudcover",
        "humidity",
        "pressure"
    ]
]

y = validation_df["temperature"]

# ==========================
# Load Models
# ==========================

production_model = joblib.load(
    PRODUCTION_MODEL
)

candidate_model = joblib.load(
    CANDIDATE_MODEL
)

# ==========================
# Predictions
# ==========================

prod_pred = production_model.predict(X)

cand_pred = candidate_model.predict(X)

# ==========================
# Scores
# ==========================

prod_score = r2_score(
    y,
    prod_pred
)

cand_score = r2_score(
    y,
    cand_pred
)

# ==========================
# Display Scores
# ==========================

print("\n==============================")
print("MODEL COMPARISON")
print("==============================")

print(f"Production Score : {prod_score:.4f}")
print(f"Candidate Score  : {cand_score:.4f}")

# ==========================
# Load Metadata
# ==========================

with open(METADATA_FILE, "r") as f:

    metadata = json.load(f)

# ==========================
# Read Candidate Version
# ==========================

with open(CANDIDATE_VERSION_FILE, "r") as f:

    candidate_version = f.read().strip()

# ==========================
# Save Report
# ==========================

with open(REPORT_FILE, "w") as f:

    f.write("MODEL EVALUATION REPORT\n")
    f.write("=======================\n\n")

    f.write(
        f"Production Score : {prod_score:.4f}\n"
    )

    f.write(
        f"Candidate Score  : {cand_score:.4f}\n"
    )

# ==========================
# Promotion Logic
# ==========================

if cand_score > prod_score:

    print("\nCandidate Outperforms Production")

    old_production = metadata["current_version"]

    metadata["previous_version"] = old_production

    metadata["current_version"] = candidate_version

    metadata["rollback_version"] = None

    with open(METADATA_FILE, "w") as f:

        json.dump(
            metadata,
            f,
            indent=4
        )

    shutil.copy(
        CANDIDATE_MODEL,
        PRODUCTION_MODEL
    )

    print(
        f"\nCandidate Promoted -> {candidate_version}"
    )

    with open(REPORT_FILE, "a") as f:

        f.write(
            "\nResult : Candidate Promoted\n"
        )

        f.write(
            f"Promoted Version : {candidate_version}\n"
        )

else:

    print("\nCandidate Rejected")

    with open(REPORT_FILE, "a") as f:

        f.write(
            "\nResult : Candidate Rejected\n"
        )

print("\nProcess Completed")