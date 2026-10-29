-- 1. Count failures by endpoint and status code
SELECT
    endpoint,
    status_code,
    COUNT(*) AS error_count
FROM api_logs
WHERE
    status_code >= 400
GROUP BY
    endpoint,
    status_code
ORDER BY error_count DESC;

-- 2. Count failures by status code
SELECT status_code, COUNT(*) AS error_count
FROM api_logs
WHERE
    status_code >= 400
GROUP BY
    status_code
ORDER BY error_count DESC;

-- 3. Find the slowest failed requests
SELECT
    endpoint,
    status_code,
    response_ms,
    message
FROM api_logs
WHERE
    status_code >= 400
ORDER BY response_ms DESC
LIMIT 10;