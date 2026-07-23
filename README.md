# 🔗 URL Shortener API

A production-ready URL Shortener built with **FastAPI**, **PostgreSQL**, **Redis**, **Docker**, and **JWT Authentication**.

This project is designed to simulate how URL shortening services like Bitly or TinyURL work while following industry-standard backend architecture and best practices.

---

## 🚀 Project Overview

The URL Shortener API allows users to:

- Create short URLs
- Redirect short URLs to original URLs
- Manage their own shortened links
- Track analytics
- Secure APIs using JWT Authentication
- Handle high traffic using Redis caching
- Prevent abuse using Rate Limiting

This project is built to learn **production-level backend development**, **system design concepts**, and **scalable API architecture**.

---
# 📚 Topics Covered

### Backend
- FastAPI
- REST API Development
- Pydantic V2
- Dependency Injection
- Middleware
- Background Tasks
- Exception Handling

### Database
- PostgreSQL
- SQLAlchemy 2.0
- Alembic Migrations
- ORM Relationships
- CRUD Operations
- Transactions
- Connection Pooling

### Authentication & Security
- JWT Authentication
- Authorization
- Password Hashing (bcrypt)
- OAuth2 Password Flow
- Protected Routes
- Environment Variables

### Caching
- Redis
- Cache-Aside Pattern
- TTL (Time To Live)
- Cache Invalidation

### URL Shortener
- URL Shortening
- Base62 Encoding
- Short Code Generation
- URL Redirection
- Custom Short URLs
- URL Expiration
- Click Tracking

### Performance
- Rate Limiting
- Database Indexing
- Query Optimization

# 📂 Project Structure

```
src/
│
├── auth/
├── users/
├── urls/
├── analytics/
├── middleware/
├── database/
├── utils/
├── core/
├── models/
├── schemas/
├── services/
├── repositories/
└── main.py
```

- Error Handling

### Testing
- Unit Testing
- Integration Testing
