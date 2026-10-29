from datetime import datetime


def parse_log_line(line):
    parts = [part.strip() for part in line.split("|")]

    if len(parts) != 5:
        raise ValueError("Invalid log format")

    timestamp, request, status_code, response_time, message = parts

    method, endpoint = request.split(" ", 1)

    logged_at = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))

    status_code = int(status_code)
    response_ms = int(response_time.replace("ms", ""))

    return {
        "logged_at": logged_at,
        "method": method,
        "endpoint": endpoint,
        "status_code": status_code,
        "response_ms": response_ms,
        "message": message,
    }