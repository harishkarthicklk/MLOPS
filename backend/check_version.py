import json

with open("model_registry/metadata.json") as f:
    metadata = json.load(f)

print(metadata)