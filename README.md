# URL Shortener API

A production-oriented URL Shortener backend built with **FastAPI, PostgreSQL, SQLAlchemy, Redis, JWT Authentication, Rate Limiting, and Docker**.

The project demonstrates how a real-world backend service can be designed with authentication, database persistence, caching, API validation, rate limiting, security, and containerization.

## Features

* User registration and authentication
* JWT-based authentication
* Password hashing
* Create short URLs
* Redirect short URLs to original URLs
* Update URLs
* Delete URLs
* Get user's URLs
* URL ownership validation
* Redis caching
* Redis-based rate limiting
* Short-code generation
* Database indexing
* Pagination
* URL analytics
* API validation with Pydantic
* PostgreSQL database
* SQLAlchemy ORM
* Alembic migrations
* Docker support
* Production-oriented configuration
* Swagger/OpenAPI documentation
* Security-focused API design

## Tech Stack

| Technology | Purpose                   |
| ---------- | ------------------------- |
| Python     | Programming language      |
| FastAPI    | Backend API framework     |
| PostgreSQL | Primary database          |
| SQLAlchemy | ORM                       |
| Alembic    | Database migrations       |
| Redis      | Caching and rate limiting |
| Pydantic   | Data validation           |
| JWT        | Authentication            |
| Docker     | Containerization          |
| Uvicorn    | ASGI server               |

## Architecture

```text
                    Client
                      |
                      v
                FastAPI API
                      |
          +-----------+-----------+
          |                       |
          v                       v
      PostgreSQL                Redis
          |                       |
          |              +--------+--------+
          |              |                 |
          |            Cache           Rate Limit
          |
       SQLAlchemy
          |
       Alembic
```

## Project Structure

```text
URL_Shortener/
│
├── app/
│   ├── main.py
│   │
│   ├── api/
│   │   └── routes/
│   │
│   ├── models/
│   │
│   ├── schemas/
│   │
│   ├── services/
│   │
│   ├── repositories/
│   │
│   ├── core/
│   │
│   ├── db/
│   │
│   └── utils/
│
├── alembic/
│
├── tests/
│
├── .env
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

> The exact structure may differ depending on the current implementation.

## Authentication

The API uses JWT-based authentication.

Typical authentication flow:

```text
Register
   |
   v
Login
   |
   v
JWT Access Token
   |
   v
Protected API
```

Protected endpoints require:

```text
Authorization: Bearer <access_token>
```

Passwords are never stored as plain text. They are securely hashed before being stored in PostgreSQL.

## URL Shortening Flow

When a user creates a short URL:

```text
Client
  |
  | POST /urls
  v
FastAPI
  |
  v
Validate URL
  |
  v
Generate short code
  |
  v
Store in PostgreSQL
  |
  v
Return short URL
```

Example:

```text
Original:
https://example.com/very/long/url

Short:
https://your-domain.com/Ab12X
```

## Redirect Flow

When a user opens the short URL:

```text
Client
  |
  v
GET /{short_code}
  |
  v
Check Redis
  |
  +---- Cache HIT ----> Original URL
  |
  +---- Cache MISS
            |
            v
       PostgreSQL
            |
            v
       Store in Redis
            |
            v
       Redirect
```

Redis reduces repeated database queries for frequently accessed short URLs.

## Redis Caching

Redis is used as a cache for URL lookup.

Conceptually:

```text
short_code -> original_url
```

Example:

```text
Ab12X -> https://example.com
```

The redirect process first checks Redis.

If the URL exists in Redis, the database does not need to be queried.

If Redis does not contain the URL, PostgreSQL is queried and the result can be cached.

## Rate Limiting

Rate limiting protects the API from excessive requests.

Conceptually:

```text
Client
  |
  v
Rate Limiter
  |
  +---- Limit exceeded ---> 429 Too Many Requests
  |
  +---- Allowed ----------> FastAPI endpoint
```

Redis can maintain request counters with expiration windows.

This helps protect the service from:

* Abuse
* Excessive API requests
* Brute-force attempts
* Accidental request floods

## Database

PostgreSQL is the primary persistent database.

SQLAlchemy is used for ORM operations.

Alembic is used to manage database schema migrations.

Typical workflow:

```bash
alembic revision --autogenerate -m "create urls table"
alembic upgrade head
```

## Analytics

The system can track URL-related analytics such as:

* Click count
* Creation time
* Last accessed time
* Other request metadata depending on implementation

Analytics can be used to understand how frequently shortened URLs are accessed.

**Axit**

Backend Developer | Python | FastAPI | PostgreSQL | Redis | Docker
