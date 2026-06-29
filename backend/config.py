import os

# ======================================================
# MODEL REGISTRY
# ======================================================

MODEL_REGISTRY = os.getenv(
    "MODEL_REGISTRY",
    r"C:\WEATHERMLOPS\model_registry"
)

# ======================================================
# VALIDATION DATASET
# ======================================================

VALIDATION_DATASET = os.getenv(
    "VALIDATION_DATASET",
    r"C:\WEATHERMLOPS\validation_dataset"
)

# ======================================================
# ARTIFACTS DIRECTORY
# ======================================================

ARTIFACTS_DIR = os.path.join(
    MODEL_REGISTRY,
    "artifacts"
)