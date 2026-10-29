# AI-Assisted Support Ticket Triage & Log Analyzer

A Python-based tool that analyzes API and application error logs, groups failures by endpoint and status code, stores them in PostgreSQL, and uses an LLM to generate probable root causes and customer-facing response drafts.

Every AI-generated analysis goes through a human review step before it is saved.

## Project Goals

This project is designed to reduce repetitive investigation work for support and engineering teams by:

- Parsing API error logs
- Grouping failures by endpoint and HTTP status code
- Storing logs in PostgreSQL
- Running SQL-based investigations
- Generating probable root causes using an LLM
- Drafting customer-facing responses
- Requiring human approval, editing, or rejection of AI output
- Running the application with Docker

## Tech Stack

- **Language:** Python 3.13
- **Database:** PostgreSQL 16
- **Database Access:** psycopg2
- **Configuration:** python-dotenv
- **AI/LLM:** OpenAI or Anthropic API
- **Testing:** pytest
- **Containerization:** Docker and Docker Compose
- **Version Control:** Git and GitHub

## Project Structure

```text
support-log-analyzer/
├── app/
│   ├── config.py
│   ├── db.py
│   ├── parser.py
│   ├── llm.py
│   ├── review.py
│   └── main.py
├── sample_logs/
│   └── generate_logs.py
├── sql/
│   ├── schema.sql
│   └── queries.sql
├── tests/
│   └── test_parser.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
└── pytest.ini
```

## How It Works

1. Generate sample API and application logs.
2. Parse the logs into structured data.
3. Store the logs in PostgreSQL.
4. Run SQL queries to investigate failures.
5. Group high-severity errors by endpoint and status code.
6. Generate an AI-assisted root cause and customer response.
7. Review the AI output manually.
8. Approve, edit, or reject the analysis.
9. Save approved or edited analyses to PostgreSQL.

## Commands

### Generate sample logs

```bash
python sample_logs/generate_logs.py
```

### Load logs into PostgreSQL

```bash
python -m app.main load sample_logs/api_logs.txt
```

### View error summary

```bash
python -m app.main summary
```

### Analyze errors

```bash
python -m app.main analyze
```

### View reviewed reports

```bash
python -m app.main report
```

## Running with Docker

Make sure Docker Desktop is running.

Start the application and PostgreSQL:

```bash
docker compose up --build
```

Stop the containers:

```bash
docker compose down
```

The application container connects to PostgreSQL using the Docker Compose service name `db`.

## Database

The project uses PostgreSQL with two main tables.

### api_logs

Stores parsed API and application logs.

Important fields:

- `logged_at`
- `method`
- `endpoint`
- `status_code`
- `response_ms`
- `message`

### analyses

Stores reviewed AI-assisted analyses.

Important fields:

- `endpoint`
- `status_code`
- `error_count`
- `root_cause`
- `draft_reply`
- `review_status`
- `reviewed_at`

## SQL Investigation

The project includes SQL queries for:

- Counting failures by endpoint and status code
- Counting failures by HTTP status code
- Finding the slowest failed requests

The queries are available in:

```text
sql/queries.sql
```

## AI-Assisted Analysis

The LLM generates:

1. A probable root cause
2. A customer-facing response draft

The project supports mock mode so the application can be tested without an API key.

LLM configuration is kept outside the source code using environment variables.

## Human Review

AI output is not automatically treated as the final answer.

For every analysis, the reviewer can:

- Approve the AI output
- Edit the root cause and customer response
- Reject the analysis

Only approved or edited analyses are saved as reviewed results.

## Testing

Run the parser tests with:

```bash
pytest
```

The tests verify that log lines are correctly converted into structured data.

## Environment Variables

Create a `.env` file for local configuration.

Example:

```text
DB_HOST=127.0.0.1
DB_PORT=5432
DB_NAME=support_logs
DB_USER=support_user
DB_PASSWORD=support_password
LLM_MOCK_MODE=true
```

Do not commit `.env` or API keys to Git.

## Future Improvements

Possible future improvements include:

- More robust log validation
- Additional automated tests
- Better error-rate calculations
- Support for more log formats
- Real LLM integration with stronger validation
- Structured LLM responses
- More detailed reporting
- Web-based dashboard
- Integration with real support ticket systems

## Project Status

This project demonstrates:

- Python application development
- API and application log analysis
- PostgreSQL and SQL investigation
- LLM integration
- Human-in-the-loop AI workflows
- Automated testing
- Docker containerization
- Git and GitHub workflow

---
