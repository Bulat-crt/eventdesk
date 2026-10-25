# EventDesk

**EventDesk** is a full-stack event management application built with Python. It provides a REST API for managing events and participant registrations, with a web interface for interacting with the application.

This project is developed as a practical learning project focused on backend engineering, database design, testing, containerization, and API development.

## Features

- Create, list, retrieve, and delete events.
- Register participants for events using their name and email.
- Prevent duplicate registrations for the same event and email address.
- Enforce event capacity and prevent registrations when all places are taken.
- Protect capacity checks against concurrent registration requests using PostgreSQL transactions and row-level locking.
- Retrieve registration statistics, including registered participants and available places.
- Validate request data and return meaningful HTTP error responses.
- Provide a web interface for managing events and registering participants.
- Run the API, frontend, and PostgreSQL using Docker Compose.
- Automatically run tests through GitHub Actions.

## Tech Stack

- **Python 3.13**
- **FastAPI** — REST API framework
- **SQLAlchemy** — ORM and database access
- **PostgreSQL** — relational database
- **Alembic** — database migrations
- **Pydantic** — request validation and response schemas
- **pytest** — automated testing
- **Docker and Docker Compose** — containerization and local environment
- **Nginx** — serving the frontend and proxying API requests
- **HTML, CSS, JavaScript** — frontend

## Project Structure

```text
eventdesk/
├── app/
│   ├── models.py
│   ├── schemas.py
│   ├── database.py
│   ├── exceptions.py
│   ├── repositories/
│   ├── services/
│   └── routers/
├── alembic/
│   └── versions/
├── frontend/
│   ├── Dockerfile
│   ├── nginx.conf
│   ├── index.html
│   ├── styles.css
│   └── app.js
├── tests/
│   ├── conftest.py
│   ├── test_events.py
│   └── test_registrations.py
├── .github/
│   └── workflows/
│       └── tests.yml
├── alembic.ini
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── requirements-dev.txt
├── main.py
└── README.md
```

## Getting Started

### Prerequisites

- Git
- Docker Desktop or Docker Engine with Docker Compose
- Python 3.13 and PostgreSQL for running the application outside Docker

### Run with Docker Compose

Clone the repository:

```bash
git clone https://github.com/Bulat-crt/eventdesk.git
cd eventdesk
```

Create a `.env` file in the project root:

```dotenv
POSTGRES_DB=eventdesk
POSTGRES_USER=postgres
POSTGRES_PASSWORD=change-this-password
```

Replace the example password with your own local development password.

Build and start the application:

```bash
docker compose up --build
```

Docker Compose starts PostgreSQL, waits for the database health check, applies Alembic migrations, and starts the FastAPI application and frontend.

Once the containers are running, open the following addresses:

- **Frontend:** http://localhost:8080
- **API documentation (Swagger UI):** http://localhost:8000/docs
- **API schema:** http://localhost:8000/openapi.json

To stop the application:

```bash
docker compose down
```

The PostgreSQL data is stored in a named Docker volume and is preserved when the containers are stopped. To remove the database volume as well, use `docker compose down -v`. This permanently deletes the data stored in that volume.

## Running Locally Without Docker

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

Configure `DATABASE_URL` in `.env` to point to your local development database:

```dotenv
DATABASE_URL=postgresql+psycopg2://postgres:your-password@localhost:5432/eventdesk
TEST_DATABASE_URL=postgresql+psycopg2://postgres:your-password@localhost:5432/eventdesk_test
```

Create the development and test databases in PostgreSQL before proceeding.

Apply migrations to the development database:

```bash
alembic upgrade head
```

Run the API:

```bash
uvicorn main:app --reload
```

Open the API documentation at http://127.0.0.1:8000/docs.

### Running Tests

Install development and testing dependencies:

```bash
python -m pip install -r requirements-dev.txt
```

Ensure that the test database has the current schema. If necessary, apply migrations to it:

```bash
DATABASE_URL="$TEST_DATABASE_URL" alembic upgrade head
```

Run the test suite:

```bash
python -m pytest -v
```

**Important:** `TEST_DATABASE_URL` must point to a separate test database. The test fixtures clear its event and registration data, so never point it at a database containing data you need to preserve.

## API Endpoints

| Method | Endpoint | Description | Success status |
|---|---|---|---|
| `POST` | `/events` | Create an event | `201 Created` |
| `GET` | `/events` | List events | `200 OK` |
| `GET` | `/events/{event_id}` | Retrieve an event by ID | `200 OK` |
| `DELETE` | `/events/{event_id}` | Delete an event | `204 No Content` |
| `POST` | `/events/{event_id}/registrations` | Register a participant | `201 Created` |
| `GET` | `/events/{event_id}/registrations/stats` | Retrieve registration and capacity statistics | `200 OK` |

Typical error responses include:

- `404 Not Found` — the event does not exist.
- `409 Conflict` — the email is already registered for the event or the event has reached capacity.
- `422 Unprocessable Entity` — request data fails validation.

## Data Model

### Event

An event stores its title, optional description, location, start date and time, capacity, and creation timestamp.

### Registration

A registration stores its associated event, attendee name, attendee email, and registration timestamp.

PostgreSQL enforces uniqueness for the pair `(event_id, attendee_email)`, allowing the same email to register for different events while preventing duplicate registrations for the same event. Event capacity must be positive.

Registration logic uses a transaction and row-level locking to protect capacity checks when multiple requests arrive concurrently.

## Architecture

The application follows a layered structure:

- **Routers** handle HTTP requests and responses.
- **Schemas** validate incoming data and define response formats.
- **Services** implement business rules and coordinate transactional operations.
- **Repositories** perform database queries and persistence.
- **Models** define the SQLAlchemy database schema.
- **Alembic** manages database schema changes through migrations.

The frontend is served by Nginx in its own container. API requests are proxied to FastAPI, while PostgreSQL runs as a separate service managed by Docker Compose.

## Continuous Integration

GitHub Actions automatically runs the test workflow on pushes and pull requests.

The workflow starts a PostgreSQL service, installs the application and testing dependencies, applies database migrations, and runs pytest.

## Learning Goals

EventDesk is a practical project for developing skills in:

- REST API design with FastAPI
- Relational database modelling
- SQLAlchemy and Alembic
- Transaction management and concurrent access
- Input validation and error handling
- Automated testing with pytest
- Docker and Docker Compose
- Git, GitHub, and continuous integration
- Frontend-to-backend integration

## Project Status

The core EventDesk MVP is implemented, including the event API, participant registrations, capacity checks, registration statistics, automated tests, Docker configuration, and web frontend.

The project serves as a foundation for further improvements in testing, deployment, user experience, and backend architecture.
