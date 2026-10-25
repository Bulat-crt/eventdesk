# EventDesk

EventDesk is a backend API for managing events and participant registrations. It is being built as a learning project to practise Python backend development, FastAPI, SQLAlchemy, PostgreSQL, Alembic migrations, testing, and Git.

> **Project status:** Backend MVP in progress. Docker-based deployment and a frontend are planned for later stages.

## Features

- Create and list events.
- Retrieve an event by ID.
- Delete an event.
- Register participants for an event.
- Prevent the same email address from registering for the same event more than once.
- Enforce positive event capacity at the database level.
- Prevent registrations when an event has reached its capacity.
- Retrieve registration statistics, including registered participants and remaining places.
- Return meaningful HTTP errors for missing events, duplicate registrations, and full events.

## Tech Stack

- **Python 3.13**
- **FastAPI** — REST API
- **SQLAlchemy** — ORM and database access
- **PostgreSQL** — relational database
- **Alembic** — database migrations
- **Pydantic** — request and response validation
- **pytest** — automated tests

## API Endpoints

| Method | Endpoint | Description | Expected success status |
|---|---|---|---|
| `POST` | `/events` | Create an event | `201 Created` |
| `GET` | `/events` | List events | `200 OK` |
| `GET` | `/events/{event_id}` | Retrieve an event | `200 OK` |
| `DELETE` | `/events/{event_id}` | Delete an event | `204 No Content` |
| `POST` | `/events/{event_id}/registrations` | Register a participant | `201 Created` |
| `GET` | `/events/{event_id}/registrations/stats` | Get registration and capacity statistics | `200 OK` |

Typical error responses include `404 Not Found` for missing events and `409 Conflict` for duplicate registrations or events that have reached capacity.

Interactive API documentation is available through FastAPI's Swagger UI at `/docs` when the application is running.

## Data Model

### Event

An event stores its title, optional description, location, start date and time, capacity, and creation timestamp.

### Registration

A registration stores the associated event, attendee name, attendee email, and registration timestamp.

The database enforces uniqueness for the pair `(event_id, attendee_email)`, so an email can register for different events but cannot register twice for the same event. Event capacity must be positive. Registration logic uses a transaction and row locking to protect capacity checks when requests overlap.

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/Bulat-crt/eventdesk.git
cd eventdesk
```

### 2. Create and activate a virtual environment

macOS / Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Create a PostgreSQL database

Create a local PostgreSQL database for the application, for example `eventdesk`.

### 5. Configure environment variables

Create a `.env` file in the project root. Set `DATABASE_URL` to your local PostgreSQL connection string:

```dotenv
DATABASE_URL=postgresql+psycopg2://<username>:<password>@localhost:5432/eventdesk
```

Replace the placeholders with your local PostgreSQL credentials. Do not commit `.env` or real credentials to Git.

If you use a separate test database, configure `TEST_DATABASE_URL` to point to that database, for example:

```dotenv
TEST_DATABASE_URL=postgresql+psycopg2://<username>:<password>@localhost:5432/eventdesk_test
```

Make sure the test database is separate from the development database: test fixtures may clear its tables.

### 6. Apply database migrations

```bash
alembic upgrade head
```

### 7. Run the API

```bash
uvicorn main:app --reload
```

Open the interactive documentation at <http://127.0.0.1:8000/docs>.

## Running Tests

Ensure the test database exists and that `TEST_DATABASE_URL` points to it, then run:

```bash
python -m pytest -v
```

Do not point `TEST_DATABASE_URL` at the development database. The test setup may clear data between tests.

## Roadmap

- [x] Event and registration API foundations
- [x] Database models and Alembic migrations
- [x] Registration validation and capacity checks
- [x] Registration statistics endpoint
- [x] Automated tests for core API behaviour
- [ ] Dockerfile and Docker Compose setup
- [ ] Frontend
- [ ] GitHub Actions workflow for automated tests

## Learning Goals

EventDesk is an evolving project. Its goal is to build practical backend skills step by step: API design, relational data modelling, transactions, concurrency, error handling, testing, Git workflows, containerisation, and continuous integration.
