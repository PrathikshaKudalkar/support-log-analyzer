import sys

from app.db import get_connection
from app.llm import analyze_error
from app.parser import parse_log_line
from app.review import review_analysis


def load_logs(file_path):
    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            with open(file_path, "r", encoding="utf-8") as file:
                for line in file:
                    line = line.strip()

                    if not line:
                        continue

                    log = parse_log_line(line)

                    cursor.execute(
                        """
                        INSERT INTO api_logs (
                            logged_at,
                            method,
                            endpoint,
                            status_code,
                            response_ms,
                            message
                        )
                        VALUES (%s, %s, %s, %s, %s, %s)
                        """,
                        (
                            log["logged_at"],
                            log["method"],
                            log["endpoint"],
                            log["status_code"],
                            log["response_ms"],
                            log["message"],
                        ),
                    )

        conn.commit()
        print("Logs loaded successfully.")

    finally:
        conn.close()


def show_summary():
    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    endpoint,
                    status_code,
                    COUNT(*) AS error_count
                FROM api_logs
                WHERE status_code >= 400
                GROUP BY endpoint, status_code
                ORDER BY error_count DESC;
                """
            )

            rows = cursor.fetchall()

            print("\nError Summary")
            print("-" * 50)

            for endpoint, status_code, error_count in rows:
                print(
                    f"{endpoint} | "
                    f"{status_code} | "
                    f"{error_count} errors"
                )

    finally:
        conn.close()


def analyze_errors():
    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    endpoint,
                    status_code,
                    COUNT(*) AS error_count
                FROM api_logs
                WHERE status_code >= 500
                GROUP BY endpoint, status_code
                ORDER BY error_count DESC
                LIMIT 3;
                """
            )

            groups = cursor.fetchall()

            for endpoint, status_code, error_count in groups:
                cursor.execute(
                    """
                    SELECT message
                    FROM api_logs
                    WHERE endpoint = %s
                      AND status_code = %s
                    ORDER BY logged_at DESC
                    LIMIT 5;
                    """,
                    (endpoint, status_code),
                )

                messages = [row[0] for row in cursor.fetchall()]

                result = analyze_error(
                    endpoint,
                    status_code,
                    error_count,
                    messages,
                )

                print("\n" + "=" * 60)
                print(f"Endpoint: {endpoint}")
                print(f"Status: {status_code}")
                print(f"Error count: {error_count}")

                reviewed = review_analysis(
                    result["root_cause"],
                    result["draft_reply"],
                )

                if reviewed["review_status"] == "rejected":
                    print("Analysis rejected. Nothing was saved.")
                    continue

                cursor.execute(
                    """
                    INSERT INTO analyses (
                        endpoint,
                        status_code,
                        error_count,
                        root_cause,
                        draft_reply,
                        review_status
                    )
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (
                        endpoint,
                        status_code,
                        error_count,
                        reviewed["root_cause"],
                        reviewed["draft_reply"],
                        reviewed["review_status"],
                    ),
                )

                conn.commit()

                print(
                    f"Analysis {reviewed['review_status']} "
                    "and saved successfully."
                )

    finally:
        conn.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(
            "Usage: python -m app.main "
            "load <file> OR summary OR analyze"
        )
        sys.exit(1)

    command = sys.argv[1]

    if command == "load":
        if len(sys.argv) < 3:
            print("Please provide a log file path.")
            sys.exit(1)

        load_logs(sys.argv[2])

    elif command == "summary":
        show_summary()

    elif command == "analyze":
        analyze_errors()

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)