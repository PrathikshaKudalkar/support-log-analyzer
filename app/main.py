from app.db import get_connection
from app.parser import parse_log_line


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


if __name__ == "__main__":
    load_logs("sample_logs/api_logs.txt")