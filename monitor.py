import requests
import time
import subprocess

ROLLBACK_TRIGGERED = False

while True:

    try:

        response = requests.get(
            "http://localhost:5000/health",
            timeout=5
        )

        if response.status_code == 200:

            print("Healthy")

        else:

            print("Unhealthy")

            if not ROLLBACK_TRIGGERED:

                subprocess.run(
                    ["python", "rollback.py"]
                )

                print(
                    "Automatic Rollback Completed"
                )

                ROLLBACK_TRIGGERED = True

    except Exception as e:

        print(
            f"Health Check Failed: {e}"
        )

        if not ROLLBACK_TRIGGERED:

            subprocess.run(
                ["python", "rollback.py"]
            )

            print(
                "Automatic Rollback Completed"
            )

            ROLLBACK_TRIGGERED = True

    time.sleep(30)