import os
import json
import time
import requests
import subprocess

PROJECT_ROOT = r"C:\WEATHERMLOPS"

ROLLBACK_SCRIPT = os.path.join(
    PROJECT_ROOT,
    "backend",
    "rollback.py"
)

UNROLLBACK_SCRIPT = os.path.join(
    PROJECT_ROOT,
    "backend",
    "unrollback.py"
)

METADATA_FILE = os.path.join(
    PROJECT_ROOT,
    "model_registry",
    "metadata.json"
)


print("ROLLBACK_SCRIPT =", ROLLBACK_SCRIPT)
print("UNROLLBACK_SCRIPT =", UNROLLBACK_SCRIPT)

FAILURE_COUNT = 0
FAILURE_THRESHOLD = 3

HEALTHY_COUNT = 0
HEALTHY_THRESHOLD = 3

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
            HEALTHY_COUNT += 1

        else:

            print(
                f"{time.ctime()} -> Unhealthy"
            )

            FAILURE_COUNT += 1
            HEALTHY_COUNT = 0

    except Exception as e:

        print(
            f"{time.ctime()} -> Health Check Failed: {e}"
        )

        FAILURE_COUNT += 1
        HEALTHY_COUNT = 0

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
                ["python", ROLLBACK_SCRIPT],
                capture_output=True,
                text=True
            )

            print(result.stdout)

            if result.stderr:
                print(result.stderr)

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

    # ==========================
    # Auto Rollforward
    # ==========================

    if HEALTHY_COUNT >= HEALTHY_THRESHOLD:

        with open(
            METADATA_FILE,
            "r"
        ) as f:

            metadata = json.load(f)

        if metadata["rollback_version"] is not None:

            print(
                "\nHealthy Threshold Reached"
            )

            result = subprocess.run(
                ["python", UNROLLBACK_SCRIPT],
                capture_output=True,
                text=True
            )

            print(result.stdout)

            if result.stderr:
                print(result.stderr)

            if result.returncode == 0:

                print(
                    "Automatic Rollforward Completed"
                )

            else:

                print(
                    "Rollforward Failed"
                )

        HEALTHY_COUNT = 0

    time.sleep(30)