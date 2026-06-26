import os
import json
import shutil

from config import MODEL_REGISTRY, ARTIFACTS_DIR

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

rollback_version = metadata["rollback_version"]

if rollback_version is None:

    print(
        "No Rollback Version Available"
    )

    exit()

# ==========================
# Restore Rolled Back Model
# ==========================

rollback_model_path = os.path.join(
    ARTIFACTS_DIR,
    rollback_version
)

if not os.path.exists(
    rollback_model_path
):

    print(
        f"Model Not Found: {rollback_model_path}"
    )

    exit()

shutil.copy(
    rollback_model_path,
    PRODUCTION_MODEL
)

# ==========================
# Update Metadata
# ==========================

current_version = metadata["current_version"]

metadata["previous_version"] = current_version

metadata["current_version"] = rollback_version

metadata["rollback_version"] = None

with open(
    METADATA_FILE,
    "w"
) as f:

    json.dump(
        metadata,
        f,
        indent=4
    )

print(
    f"Unrollback Successful -> {rollback_version}"
)