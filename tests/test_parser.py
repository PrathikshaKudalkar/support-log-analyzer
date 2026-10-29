from app.parser import parse_log_line


def test_parse_log_line():
    line = (
        "2026-10-20T10:15:32Z | "
        "POST /api/v1/users | "
        "500 | "
        "842ms | "
        "NullPointerException in UserService.create"
    )

    result = parse_log_line(line)

    assert result["method"] == "POST"
    assert result["endpoint"] == "/api/v1/users"
    assert result["status_code"] == 500
    assert result["response_ms"] == 842
    assert result["message"] == "NullPointerException in UserService.create"