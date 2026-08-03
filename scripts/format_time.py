from datetime import datetime, timedelta

ts = "$exec.timestamp"

try:
    dt = datetime.strptime(
        ts,
        "%Y-%m-%dT%H:%M:%S.%f%z"
    )

    vn_time = (
        dt + timedelta(hours=7)
    ).strftime("%Y-%m-%d %H:%M:%S")

except Exception:
    vn_time = ts

print(vn_time)