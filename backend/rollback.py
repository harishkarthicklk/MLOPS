import os
import json
import shutil

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

MODEL_REGISTRY = os.path.join(
    BASE_DIR,
    "..",
    "model_registry"
)

ARTIFACTS_DIR = os.path.join(
    MODEL_REGISTRY,
    "artifacts"
)

METADATA_FILE = os.path.join(
    MODEL_REGISTRY,
    "metadata.json"
)

PRODUCTION_MODEL = os.path.join(
    MODEL_REGISTRY,
    "production_model.pkl"
)

# ==========================
# Load Metadata
# ==========================

with open(METADATA_FILE, "r") as f:
    metadata = json.load(f)

# ==========================
# Prevent Multiple Rollbacks
# ==========================

if metadata["rollback_version"] is not None:

    print(
        "Rollback Already Active"
    )

    exit()

current_version = metadata["current_version"]

previous_version = metadata["previous_version"]

if previous_version is None:

    print(
        "No Previous Version Available"
    )

    exit()

# ==========================
# Restore Previous Version
# ==========================

previous_model_path = os.path.join(
    ARTIFACTS_DIR,
    previous_version
)

if not os.path.exists(previous_model_path):

    print(
        "Previous Model Not Found"
    )

    exit()

shutil.copy(
    previous_model_path,
    PRODUCTION_MODEL
)

# ==========================
# Update Metadata
# ==========================

metadata["rollback_version"] = current_version

metadata["current_version"] = previous_version

with open(METADATA_FILE, "w") as f:

    json.dump(
        metadata,
        f,
        indent=4
    )

print(
    f"Rollback Successful -> {previous_version}"
)