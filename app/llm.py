import os


def analyze_error(endpoint, status_code, error_count, messages):
    mock_mode = os.getenv("LLM_MOCK_MODE", "true").lower() == "true"

    if mock_mode:
        return {
            "root_cause": (
                f"Repeated HTTP {status_code} errors on {endpoint}. "
                "The application should be checked for the underlying "
                "exception shown in the API logs."
            ),
            "draft_reply": (
                f"We are investigating an issue affecting {endpoint}. "
                "Our engineering team is reviewing the error logs and "
                "working to identify the cause."
            ),
        }

    raise NotImplementedError("Real LLM mode will be added later.")