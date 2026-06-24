import joblib
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

prod_path = os.path.join(
    BASE_DIR,
    "model_registry",
    "production_model.pkl"
)

prev_path = os.path.join(
    BASE_DIR,
    "model_registry",
    "previous_model.pkl"
)

prod = joblib.load(prod_path)
prev = joblib.load(prev_path)

print("Production:", type(prod))
print("Previous:", type(prev))