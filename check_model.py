import joblib

model = joblib.load(
    "model_registry/production_model.pkl"
)

print(type(model))