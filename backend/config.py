import os

# ======================================================
# CHANGE THIS PATH ONLY IF YOU MOVE YOUR PROJECT
# ======================================================

PROJECT_ROOT = r"C:\WEATHERMLOPS"

MODEL_REGISTRY = os.path.join(
    PROJECT_ROOT,
    "model_registry"
)

VALIDATION_DATASET = os.path.join(
    PROJECT_ROOT,
    "validation_dataset"
)

ARTIFACTS_DIR = os.path.join(
    MODEL_REGISTRY,
    "artifacts"
)