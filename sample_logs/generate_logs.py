import random
from datetime import datetime, timedelta, timezone


ENDPOINTS = [
    ("GET", "/api/v1/users"),
    ("POST", "/api/v1/users"),
    ("GET", "/api/v1/orders"),
    ("POST", "/api/v1/orders"),
    ("GET", "/api/v1/products"),
    ("POST", "/api/v1/payments"),
]

ERROR_MESSAGES = {
    400: "Invalid request payload",
    401: "Authentication failed",
    404: "Resource not found",
    500: "Internal server error",
    503: "Service temporarily unavailable",
}


def generate_log():
    method, endpoint = random.choice(ENDPOINTS)

    # Most requests should succeed.
    status_code = random.choices(
        [200, 400, 401, 404, 500, 503],
        weights=[80, 4, 3, 4, 6, 3],
        k=1,
    )[0]

    response_ms = random.randint(50, 1500)

    logged_at = datetime.now(timezone.utc) - timedelta(
        minutes=random.randint(0, 60 * 24 * 7)
    )

    if status_code == 200:
        message = "OK"
    else:
        message = ERROR_MESSAGES[status_code]

    return (
        f"{logged_at.strftime('%Y-%m-%dT%H:%M:%SZ')} | "
        f"{method} {endpoint} | "
        f"{status_code} | "
        f"{response_ms}ms | "
        f"{message}"
    )


def main():
    number_of_logs = 500

    with open("sample_logs/api_logs.txt", "w", encoding="utf-8") as file:
        for _ in range(number_of_logs):
            file.write(generate_log() + "\n")

    print(f"Generated {number_of_logs} log entries.")


if __name__ == "__main__":
    main()