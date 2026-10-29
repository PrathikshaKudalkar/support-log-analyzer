CREATE TABLE IF NOT EXISTS api_logs (
    id SERIAL PRIMARY KEY,
    logged_at TIMESTAMPTZ NOT NULL,
    method VARCHAR(10) NOT NULL,
    endpoint TEXT NOT NULL,
    status_code INT NOT NULL,
    response_ms INT,
    message TEXT
);

CREATE TABLE IF NOT EXISTS analyses (
    id SERIAL PRIMARY KEY,
    endpoint TEXT NOT NULL,
    status_code INT NOT NULL,
    error_count INT NOT NULL,
    root_cause TEXT,
    draft_reply TEXT,
    review_status VARCHAR(10) CHECK (
        review_status IN (
            'approved',
            'edited',
            'rejected'
        )
    ),
    reviewed_at TIMESTAMPTZ DEFAULT NOW()
);