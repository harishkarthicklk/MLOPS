import os
import json
import time
import requests
import subprocess

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

ROLLBACK_SCRIPT = os.path.join(
    BASE_DIR,
    "backend",
    "rollback.py"
)

METADATA_FILE = os.path.join(
    BASE_DIR,
    "model_registry",
    "metadata.json"
)

FAILURE_COUNT = 0

FAILURE_THRESHOLD = 3

while True:

    try:

        response = requests.get(
            "http://localhost:5000/health",
            timeout=5
        )

        if response.status_code == 200:

            print(
                f"{time.ctime()} -> Healthy"
            )

            FAILURE_COUNT = 0

        else:

            print(
                f"{time.ctime()} -> Unhealthy"
            )

            FAILURE_COUNT += 1

    except Exception as e:

        print(
            f"{time.ctime()} -> Health Check Failed: {e}"
        )

        FAILURE_COUNT += 1

    # ==========================
    # Auto Rollback
    # ==========================

    if FAILURE_COUNT >= FAILURE_THRESHOLD:

        with open(
            METADATA_FILE,
            "r"
        ) as f:

            metadata = json.load(f)

        if metadata["rollback_version"] is None:

            print(
                "\nFailure Threshold Reached"
            )

            result = subprocess.run(
                ["python", ROLLBACK_SCRIPT]
            )

            if result.returncode == 0:

                print(
                    "Automatic Rollback Completed"
                )

            else:

                print(
                    "Rollback Failed"
                )

        else:

            print(
                "Rollback Already Active"
            )

        FAILURE_COUNT = 0

    time.sleep(30)