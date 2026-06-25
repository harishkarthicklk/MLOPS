import os
import requests
import time
import subprocess

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

ROLLBACK_SCRIPT = os.path.join(
    BASE_DIR,
    "backend",
    "rollback.py"
)

ROLLBACK_TRIGGERED = False

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

        else:

            print(
                f"{time.ctime()} -> Unhealthy"
            )

            if not ROLLBACK_TRIGGERED:

                result = subprocess.run(
                    ["python", ROLLBACK_SCRIPT]
                )

                if result.returncode == 0:

                    print(
                        "Automatic Rollback Completed"
                    )

                    ROLLBACK_TRIGGERED = True

                else:

                    print(
                        "Rollback Failed"
                    )

    except Exception as e:

        print(
            f"{time.ctime()} -> Health Check Failed: {e}"
        )

        if not ROLLBACK_TRIGGERED:

            result = subprocess.run(
                ["python", ROLLBACK_SCRIPT]
            )

            if result.returncode == 0:

                print(
                    "Automatic Rollback Completed"
                )

                ROLLBACK_TRIGGERED = True

            else:

                print(
                    "Rollback Failed"
                )

    time.sleep(30)